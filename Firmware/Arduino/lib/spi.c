
#include <avr/common.h>
#include <avr/io.h>
#include <avr/interrupt.h>

#include "spi.h"

#define DDR_SPI DDRB
#define DD_SS DDB2
#define DD_MOSI DDB3
#define DD_MISO DDB4
#define DD_SCK DDB5

void spi_init(void)
{
    DDR_SPI &= ~_BV(DD_MISO);
    DDR_SPI |= (_BV(DD_MOSI) | _BV(DD_SCK) | _BV(DD_SS));

    SPCR = (1 << MSTR) |
           (1 << SPE) |
           (0 << SPIE) |
           (0 << DORD) |
           (0 << CPOL) |
           (0 << SPR1) | (0 << SPR0);

    SPSR |= _BV(SPI2X);
}

const uint8_t spi_transfer(const uint8_t data)
{
    SPDR = data;
    asm volatile("nop");
    while (!(SPSR & _BV(SPIF)));
    return SPDR;
}
