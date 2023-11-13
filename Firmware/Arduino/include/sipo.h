#ifndef SIPO_H
#define SIPO_H

#define SIPO_SRST _BV(PD5)
#define SIPO_LTCH _BV(PD6)
#define SIPO_MISO _BV(PD7)

extern void sipo_init();

extern void sipo_write(const int val);

#endif