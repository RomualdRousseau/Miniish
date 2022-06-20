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
apu_ptr   .word $0000
apu_tmr   .byte $00
ppu_retr  .byte $00
joypad    .byte $00
 .dend

 .org code_start ; code ========
rst_func
 ldx #$ff ; stack size
 txs
 jmp setup

irq_func
 phx
 ldx port_irq
 jmp (table_irq,x)

 .include "sys.i"
 .include "ppu.i"
 .include "apu.i"
 .include "lcd.i"
 .include "joypad.i"
 .include "float.i"
 .include "graphic.i"
 .include "physic.i"

setup
 ; init all libraries
 jsr ppu_init
 jsr apu_init
 jsr lcd_init
 jsr joypad_init
 ; init game
 jsr init
 ; start ppu retrace
 jsr ppu_start
 cli

loop
 ; update game states
 jsr joypad_read
 jsr update
 ; wait vertical retrace
 jsr ppu_wait_nmi
 ; call draw at 5Hz
 lda ppu_retr
 and #%00011111
 bne loop
 jsr draw
 jmp loop
 
 .org inte_start ; int vectors =
table_irq
 .word irq0_func
 .word irq1_func
 .word $0000
 .word $0000
 .word $0000
 .word $0000
 .word $0000
 .word $0000
table_vec
 .word nmi_func
 .word rst_func
 .word irq_func

; vim:syntax=asmM6502
