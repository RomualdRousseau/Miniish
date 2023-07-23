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
    lda #dev_uart
    sta r0
    jsr get_char

ret_key:
    cmp #'\r'
    bne del_key
    jmp print_ln

del_key:
    cmp #$7f
    bne echo
    lda buf_end
    cmp #0
    beq get_new_line
    dec buf_end
    ; delete the last on the terminal
    lda #$08
    sta r1
    jsr put_char
    lda #'\e'
    sta r1
    jsr put_char
    lda #'['
    sta r1
    jsr put_char
    lda #'K'
    sta r1
    jsr put_char
    jmp get_new_line

echo:
    ldy buf_end
    cpy #128            ; check if buffer overflow
    bne L0
    jsr print_ln        ; if overflow, cancel line and start a new one
    jmp get_new_line
L0: sta buf_data, y
    inc buf_end
    sta r1
    jsr put_char
    jmp get_new_line
