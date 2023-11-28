#include "common.h"
#include "intr.h"

volatile uint8_t edge = 0;
volatile uint8_t intr_fired = 0;

void intr_init()
{
    PCICR |= _BV(PCIE0);
    PCMSK0 |= _BV(PCINT1);
    DDRB &= ~_BV(PB1);
}

ISR(PCINT0_vect)
{
    if (((++edge) % 2) == 0) {
        intr_fired = 1;
    }
}