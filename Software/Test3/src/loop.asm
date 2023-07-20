    .include "miniish.inc"

    .global loop

    .section text

loop:
    jsr uart_get_char
retkey:
    cmp #'\r'
    bne delkey
    jsr uart_put_char
    lda #'\n'
    jmp echo
delkey:
    cmp #$7f
    bne echo
    lda #$08
    jsr uart_put_char
    lda #'\e'
    jsr uart_put_char
    lda #'['
    jsr uart_put_char
    lda #'K'
echo:
    jsr uart_put_char
    rts
