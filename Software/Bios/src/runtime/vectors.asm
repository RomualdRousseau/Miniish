    .include "miniish.inc"

    .global table_irq

    .section vectors,"adr"

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