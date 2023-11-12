#include "common.h"
#include "clock.h"
#include "piso.h"
#include "sipo.h"
#include "intr.h"

int main(void)
{
    clock_init();
    piso_init();
    sipo_init();
    intr_init();

    while (1)
    {
        if (intr_fired) {
            const int val = piso_read();
            sipo_write(~val);
            intr_fired = 0;
        }
    }

    return 0;
}