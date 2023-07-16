    .include "sym.s"

    .dsect
    .org zero_start
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

    .org code_start
init:

loop:
    lda #%10101010
    sta r0
    lda r0
    sta io_port1
    jmp loop

    .org inte_start
    .word $0000
    .word $0000
    .word $0000
    .word $0000
    .word $0000
    .word $0000
    .word $0000
    .word $0000
    .word $0000
    .word code_start
    .word $0000

; vim:syntax=asm
