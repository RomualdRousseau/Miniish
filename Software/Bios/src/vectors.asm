    .include "miniish.inc"

    .section kernel
    
irq_func:
    phx
    ldx io_irq
    cpx #14
    beq no_irq_func
    jmp (table_irq, x)
no_irq_func:
    plx
no_nmi_func:
    rti

    .section vectors

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