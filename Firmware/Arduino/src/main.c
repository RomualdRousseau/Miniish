#include "common.h"
#include "clock.h"
#include "piso.h"
#include "sipo.h"
#include "intr.h"
#include "nrf24l01.h"
#include "uart.h"
#include "util.h"
#include "proto.h"

#define MESSAGE "NRF24L01 Transmitter v1.0\r\n"
#define ADDRESS "00001"

uint16_t channels[CHANNELS];
packet_t packet;

int main(void)
{
    uart_init(115200);
    uart_puts(MESSAGE);

    clock_init();
    piso_init();
    sipo_init();
    intr_init();

    nrf24l01_init();
    nrf24l01_set_pa_level(NRF24L01_RF24_PA_LOW);
    nrf24l01_open_writing_pipe(ADDRESS);
    nrf24l01_stop_listening();

    proto_init(channels);

    sei();

    while (1)
    {
        if (intr_fired)
        {
            const uint8_t val = piso_read();
            channels[0] = map(val, 0, 255, 1000, 2000);
            sipo_write(val);
            
            proto_encode_packet(channels, &packet);
            nrf24l01_write((const uint8_t *)&packet, sizeof(packet));

            intr_fired = 0;
        }
    }

    return 0;
}
