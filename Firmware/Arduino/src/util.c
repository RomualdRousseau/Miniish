
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

const int16_t map(const int16_t x, const int16_t in_min, const int16_t in_max, const int16_t out_min, const int16_t out_max)
{
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}