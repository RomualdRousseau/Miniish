    .include "miniish.inc"
    .include "stdio.inc"

    .global buf_data, buf_start, buf_end
    .global get_new_line

    .section data

buf_data:
    .rept 128
    .byte $00
    .endr
buf_start:
    .byte $00
buf_end:
    .byte $00

    .section text

get_new_line:
    jsr uart_get_char

ret_key:
    cmp #'\r'
    bne del_key
    jmp return

del_key:
    cmp #$7f
    bne echo
    lda buf_end
    cmp #0
    beq get_new_line
    dec buf_end
    lda #$08
    jsr uart_put_char
    lda #'\e'
    jsr uart_put_char
    lda #'['
    jsr uart_put_char
    lda #'K'
    jsr uart_put_char 
    jmp get_new_line

echo:
    ldy buf_end
    cpy #128            ; check if buffer overflow
    bne L0
    jsr return          ; if overflow, cancel line and start a new one
    jmp get_new_line
L0: sta buf_data, y
    inc buf_end
    jsr uart_put_char
    jmp get_new_line

return:
    lda #'\r'           
    jsr uart_put_char
    lda #'\n'
    jsr uart_put_char
    rts
