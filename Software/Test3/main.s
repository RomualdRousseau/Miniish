    .include "sym.s"
    .include "io.s"

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

    ; Print lcd prompt
    lda #<lcd_vtable
    sta r0
    lda #>lcd_vtable
    sta r1
    lda #put_char
    sta r2
    jsr get_func_ptr

    lda #'['
    jsr call_func_ptr
    rts

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

    .org data_user
prompt:
    .byte "\e[2J\e[H"
    .byte "\e[1;32m","*** MINIISH V1.4 ***\e[0m\r\n"
    .byte "64K RAM SYSTEM\r\n"
    .byte "READY.\r\n",0

; vim:syntax=asm
