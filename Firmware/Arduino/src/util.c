
#include "common.h"
#include "util.h"

void array_set_bit(uint8_t* buf, const int off, const uint8_t val)
{
    const uint16_t p = off / 8;
    const uint8_t b = 1 << (off % 8);

    if (val == 0)
    {
        buf[p] &= ~b;
    }
    else
    {
        buf[p] |= b;
    }
}