#include "common.h"
#include "intr.h"

volatile uint8_t edge = 0;

void intr_init()
{
    PCICR |= _BV(PCIE0);
    PCMSK0 |= _BV(PCINT1);
    DDRB &= ~_BV(PB1);
}

const uint8_t intr_is_interrupted()
{
    cli();
    const uint8_t ret = edge;
    edge = 0;
    sei();
    return ret;
}

ISR(PCINT0_vect)
{
    edge = 1;
}