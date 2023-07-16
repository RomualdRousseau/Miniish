    .include "sym.s"

    .org code_user
setup:
    jsr lcd_init
    jsr uart_init

    ; Print prompt
    lda #<prompt
    sta r0
    lda #>prompt
    sta r1
    jsr uart_print
    rts

loop:
    jsr uart_get_char
retkey:
    cmp #$0d
    bne delkey
    jsr uart_put_char
    lda #$0a
    jmp echo
delkey:
    cmp #$7f
    bne echo
    lda #$08
    jsr uart_put_char
    lda #$1B
    jsr uart_put_char
    lda #'['
    jsr uart_put_char
    lda #'K'
echo:
    jsr uart_put_char
    rts

    .org data_user
prompt:
    .byte $1B,"[2J",$1B,"[H",$1B
    .byte "[1;32m","*** MINIISH V1.4 ***",$0D,$0A
    .byte $1B,"[0m","64K RAM SYSTEM",$0D,$0A
    .byte "READY.",$0D,$0A,0

; vim:syntax=asm
