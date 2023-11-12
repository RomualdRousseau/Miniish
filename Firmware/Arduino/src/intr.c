#include "common.h"
#include "intr.h"

volatile int edge = 0;
volatile int intr_fired = 0;

void intr_init()
{
    cli();
    PCICR |= _BV(PCIE0);
    PCMSK0 |= _BV(PCINT1);
    DDRB &= ~_BV(PB1);
    sei();
}

ISR(PCINT0_vect)
{
    if (((++edge) % 2) == 0) {
        intr_fired = 1;
    }
}