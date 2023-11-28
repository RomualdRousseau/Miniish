#include "common.h"
#include "clock.h"
#include "sipo.h"

void sipo_init()
{
    DDRD |= SIPO_SRST | SIPO_LTCH | SIPO_MISO;
    PORTD &= ~(SIPO_SRST | SIPO_LTCH | SIPO_MISO);
}

void sipo_write(const uint8_t val)
{

    // Enable
    PORTB &= ~CLOCK_PIN;

    // Load
    PORTD &= ~SIPO_SRST;
    _delay_us(CLOCK_SPEED);
    PORTD |= SIPO_SRST;

    // Write Value
    for (int i = 0; i < 8; i++)
    {
        if (((val >> (7 - i)) & 0x01) > 0)
        {
            PORTD |= SIPO_MISO;
        }
        else
        {
            PORTD &= ~SIPO_MISO;
        }

        PORTB |= CLOCK_PIN;
        _delay_us(CLOCK_SPEED);

        PORTB &= ~CLOCK_PIN;
        _delay_us(CLOCK_SPEED);
    }

    // Latch
    PORTD |= SIPO_LTCH;
    _delay_us(CLOCK_SPEED);
    PORTD &= ~SIPO_LTCH;
}