    .include "miniish.inc"

    .global irq_func
    .global no_irq_func
    .global no_nmi_func
    
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
