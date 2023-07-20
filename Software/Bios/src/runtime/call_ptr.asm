    .include "miniish.inc"

    .global call_ptr

    .section kernel

call_ptr:
    jmp (dev_table, x)
