    .include "sym.s"

    .org code_start
rst_func:
    ldx #$ff ; stack size
    txs
    cld
    cli
    jsr setup
main_loop:
    jsr loop
    jmp main_loop

irq_func:
    phx
    ldx io_irq
    cpx #14
    beq no_irq_func
    jmp (table_irq,x)
no_irq_func:
    plx
no_nmi_func:
    rti

get_func_ptr:
    ldy r2
    lda (r0), y
    sta r4
    iny
    lda (r0), y
    sta r5
    rts

call_func_ptr:
    jmp (r4)

    .include "sys.s"
    .include "lcd.s"
    .include "uart.s"

    .org inte_start
table_irq:
    .word no_irq_func
    .word no_irq_func
    .word no_irq_func
    .word no_irq_func
    .word no_irq_func
    .word uart_int_func
    .word no_irq_func
    .word $0000
table_vec:
    .word no_nmi_func
    .word rst_func
    .word irq_func
