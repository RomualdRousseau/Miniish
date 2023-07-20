    .include "miniish.inc"

    .global rst_func
    
    .section kernel

rst_func:
    ldx #$ff ; stack size
    txs
    cld
    cli
    jsr lcd_init
    jsr uart_init
    jmp main
