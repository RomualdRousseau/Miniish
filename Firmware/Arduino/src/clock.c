#include "common.h"
#include "clock.h"

void clock_init()
{
    DDRB |= CLOCK_PIN;
    PORTB &= ~CLOCK_PIN;
}
