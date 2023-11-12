#ifndef PISO_H
#define PISO_H

#define PISO_ENBL _BV(PD2)
#define PISO_LOAD _BV(PD3)
#define PISO_MOSI _BV(PD4)

extern void piso_init();

extern int piso_read();

#endif