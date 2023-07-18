    .include "miniish.inc"

    .section kernel

rst_func:
    ldx #$ff ; stack size
    txs
    cld
    cli
    jmp main

get_dev_func_offset:
    lda r0
    clc
    adc r1
    tax
    rts

call_dev_func:
    jmp (dev_table, x)
