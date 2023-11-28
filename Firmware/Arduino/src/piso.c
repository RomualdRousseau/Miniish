#include "common.h"
#include "clock.h"
#include "piso.h"

void piso_init()
{
    DDRD |= PISO_LOAD | PISO_ENBL;
    DDRD &= ~PISO_MOSI;
    PORTD |= PISO_LOAD | PISO_ENBL;
}

const uint8_t piso_read()
{
    uint8_t val = 0;

    // Enable
    PORTB |= CLOCK_PIN;
    PORTD &= ~PISO_ENBL;

    // Load
    PORTD &= ~PISO_LOAD;
    _delay_us(CLOCK_SPEED);
    PORTD |= PISO_LOAD;

    // Read on failing clock

    for (int i = 0; i < 8; i++)
    {
        PORTB &= ~CLOCK_PIN;

        if ((PIND & PISO_MOSI) > 0)
        {
            val = (val << 1) | 0x01;
        }
        else
        {
            val = (val << 1);
        }
        _delay_us(CLOCK_SPEED);

        PORTB |= CLOCK_PIN;
        _delay_us(CLOCK_SPEED);
    }

    // Disable
    PORTD |= PISO_ENBL;

    return val;
}