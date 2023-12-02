#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#include "nrf24.h"
#include "spi.h"
#include "nrf24l01.h"

// Utils

#define bit_set_i(port, bit) (port) |= _BV(bit)
#define bit_clear_i(port, bit) (port) &= ~_BV(bit)
#define bit_set(port, bit) ((port) | _BV(bit))
#define bit_clear(port, bit) ((port) & ~_BV(bit))

// States

#define POWERUP 1
#define POWERDOWN 2
#define TRANSMIT 3

// Pins

#define CE_DDR DDRC
#define CE_PORT PORTC
#define CE_PIN DDC3 // CE connected to A3
#define CSN_DDR DDRB
#define CSN_PORT PORTB
#define CSN_PIN DDB2 // CSN connected to SS

// PIN toggling
#define ce_low bit_clear_i(CE_PORT, CE_PIN)
#define ce_high bit_set_i(CE_PORT, CE_PIN)
#define csn_low bit_clear_i(CSN_PORT, CSN_PIN)
#define csn_high bit_set_i(CSN_PORT, CSN_PIN)

uint8_t last_status = 0;

const void nrf24_send_spi(const uint8_t register_address, const uint8_t *data, const uint8_t size)
{
    csn_low;
    last_status = spi_transfer(register_address);
    for (uint8_t i = 0; i < size; i++)
    {
        spi_transfer(data[i]);
    }
    csn_high;
}

const void nrf24_transfer_spi(const uint8_t register_address, uint8_t *data, const uint8_t size)
{
    csn_low;
    last_status = spi_transfer(register_address);
    for (uint8_t i = 0; i < size; i++)
    {
        data[i] = spi_transfer(data[i]);
    }
    csn_high;
}

void nrf24_write_reg(uint8_t register_address, const uint8_t data)
{
    nrf24_send_spi(W_REGISTER | register_address, &data, 1);
}

uint8_t nrf24_read_reg(uint8_t register_address)
{
    uint8_t data = NOP;
    nrf24_transfer_spi(R_REGISTER | register_address, &data, 1);
    return data;
}

void nrf24_write_regs(const uint8_t register_address, const uint8_t *data, const uint8_t size)
{
    nrf24_send_spi(W_REGISTER | register_address, data, size);
}

void nrf24_read_regs(const uint8_t register_address, uint8_t *data, const uint8_t size)
{
    nrf24_transfer_spi(R_REGISTER | register_address, data, size);
}

void nrf24_flush_rx() 
{
    csn_low;
    spi_transfer(FLUSH_RX);
    csn_high;
}

void nrf24_flush_tx() 
{
    csn_low;
    spi_transfer(FLUSH_TX);
    csn_high;
}

uint8_t nrf24_get_status() 
{
    nrf24_read_reg(NOP);
    return last_status;
}

void nrf24_state(const uint8_t state)
{
    uint8_t config_register = nrf24_read_reg(CONFIG);
    switch (state)
    {
    case POWERUP:
        if (bit_is_clear(config_register, PWR_UP))
        {
            nrf24_write_reg(CONFIG, bit_set(config_register, PWR_UP));
            _delay_ms(2);
        }
        break;

    case POWERDOWN:
        if (bit_is_set(config_register, PWR_UP))
        {
            nrf24_write_reg(CONFIG, bit_clear(config_register, PWR_UP));
            _delay_ms(2);
        }
        break;

    case TRANSMIT:
        nrf24_write_reg(CONFIG, bit_clear(config_register, PRIM_RX));
        _delay_us(150);
        break;
    }
}

void nrf24_init(const uint8_t *address)
{
    uint8_t data;

    // CSN and CE as outputs
    bit_set_i(CE_DDR, CE_PIN);
    bit_set_i(CSN_DDR, CSN_PIN);

    // Let's rock!
    ce_low;
    csn_high;

    // Initialize SPI
    spi_init();
    _delay_ms(100); // Power on reset 100ms

    // Set Retry: 5, 15
    nrf24_write_reg(SETUP_RETR, (0x05 << ARD) | (0x0F << ARC));

    // Set PA level: LOW
    data = nrf24_read_reg(RF_SETUP) & ~(_BV(POWER_LOW) | _BV(POWER_HIGH));
    nrf24_write_reg(RF_SETUP, data | _BV(POWER_LOW));

    // Set data rate: 1MBPS
    data = nrf24_read_reg(RF_SETUP) & ~(_BV(RF_DR_LOW) | _BV(RF_DR_HIGH));
    nrf24_write_reg(RF_SETUP, data);

    // Set CRC length: CRC16
    data = nrf24_read_reg(CONFIG) & ~(_BV(CRC0) | _BV(EN_CRC));
    nrf24_write_reg(CONFIG, data | _BV(CRC0) | _BV(EN_CRC));

    // Disable dynamic payloads
    nrf24_write_reg(DYNPD, 0);

    // Enable auto-ack on pipes 0 & 1
    nrf24_write_reg(EN_AA, _BV(ENAA_P1) | _BV(ENAA_P0));

    // Only open RX pipes 0 & 1
    nrf24_write_reg(EN_RXADDR, _BV(ERX_P1) | _BV(ERX_P0)); 

    // Reset current status
    nrf24_write_reg(STATUS, _BV(RX_DR) | _BV(TX_DS) | _BV(MAX_RT));

    // Set channel
    nrf24_write_reg(RF_CH, 76);

    nrf24_flush_rx();
    nrf24_flush_tx();

    // Set RADDR and TADDR as the transmit address since we also enable auto acknowledgement
    nrf24_write_regs(RX_ADDR_P0, address, 5);
    nrf24_write_regs(TX_ADDR, address, 5);

    // Set the payload size
    nrf24_write_reg(RX_PW_P0, 32);

    nrf24_state(POWERUP);
}

void nrf24_write_async(const uint8_t *data, const uint8_t size)
{
    // Transmit mode
    nrf24_state(TRANSMIT);

    // Start SPI, load data into TX_PAYLOAD
    csn_low;
    spi_transfer(W_TX_PAYLOAD);
    for (uint8_t i = 0; i < size; i++)
    {
        spi_transfer(data[i]);
    }
    for (uint8_t i = size; i < 32; i++)
    {
        spi_transfer(0);
    }
    csn_high;

    // Send data by pulling CE high for more than 10us
    ce_high;
    _delay_us(15);
    ce_low;
}

void nrf24_write_wait()
{
    // Wait data to be transmitted
    while (!(nrf24_get_status() & (_BV(TX_DS) | _BV(MAX_RT))))
    {
        _delay_ms(1);
    }
    
    ce_low;
    nrf24_write_reg(STATUS, _BV(RX_DR) | _BV(TX_DS) | _BV(MAX_RT));

    //Max retries exceeded
    if (last_status & _BV(MAX_RT)) {
        nrf24_flush_tx();
    }
}

void nrf24_write(const uint8_t *data, const uint8_t size)
{
    nrf24_write_async(data, size);
    nrf24_write_wait();
}
