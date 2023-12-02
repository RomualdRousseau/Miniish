#include "common.h"
#include "clock.h"
#include "piso.h"
#include "sipo.h"
#include "intr.h"
#include "nrf24.h"
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
    uart_set_stdout();
    printf(MESSAGE);
    clock_init();
    piso_init();
    sipo_init();
    intr_init();
    nrf24_init(ADDRESS);
    proto_init(channels);
    
    sei();

    while (1)
    {
        if (intr_is_interrupted())
        {
            const uint8_t val = piso_read();
            sipo_write(val);

            channels[0] = map(val, 0, 255, 1000, 2000);
            proto_encode_packet(channels, &packet);
            nrf24_write((const uint8_t *)&packet, sizeof(packet));

            printf("Processed 1 byte: %02X\r\n", val);
        }
    }

    return 0;
}
