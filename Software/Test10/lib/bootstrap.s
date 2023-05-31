 .include "sym.i"

 .dsect
 .org zero_start ; zero ========
r0        .byte $00
r1        .byte $00
r2        .byte $00
r3        .byte $00
r4        .byte $00
r5        .byte $00
r6        .byte $00
r7        .byte $00
r8        .byte $00
r9        .byte $00
r10       .byte $00
r11       .byte $00
r12       .byte $00
r13       .byte $00
r14       .byte $00
r15       .byte $00
 .dend

 .org code_start ; code ========
rst_func
 ldx #$ff ; stack size
 txs
 jmp setup

irq_func
 phx
 ldx io_irq
 jmp (table_irq,x)

 .include "sys.i"
 .include "lcd.i"

setup
 ; init all libraries
 jsr lcd_init
 ; init game
 jsr init
 cli

loop
 ; update game states
 jsr update
 jmp loop
 
 .org inte_start ; int vectors =
table_irq
 .word irq0_func
 .word irq1_func
 .word irq2_func
 .word irq3_func
 .word irq4_func
 .word irq5_func
 .word irq6_func
 .word $0000
table_vec
 .word nmi_func
 .word rst_func
 .word irq_func
