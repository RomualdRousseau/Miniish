    .include "miniish.inc"
    .include "conio.inc"

    .section text

main:
    jsr lcd_init
    jsr uart_init
    jsr setup
main_loop:
    jsr loop
    jmp main_loop

setup:
    ; Print lcd prompt
    lda #dev_lcd
    sta r0
    lda #<message
    sta r1
    lda #>message
    sta r2
    jsr print

    ; Print prompt
    lda #dev_uart
    sta r0
    lda #<prompt
    sta r1
    lda #>prompt
    sta r2
    jsr print
    
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

    .section data
prompt:
    .byte "\e[2J\e[H"
    .byte "\e[1;32m","*** MINIISH V1.4 ***\e[0m\r\n"
    .byte "64K RAM SYSTEM\r\n"
    .byte "READY.\r\n",0
message:
    .asciiz "Hello the world"

; vim:syntax=asm
