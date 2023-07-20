    .include "miniish.inc"
    .include "stdio.inc"

    .global setup

    .section text

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

    .section rodata

prompt:
    .byte "\e[2J\e[H"
    .byte "\e[1;32m","*** MINIISH V1.4 ***\e[0m\r\n"
    .byte "64K RAM SYSTEM\r\n"
    .byte "READY.\r\n",0

message:
    .asciiz "Hello the world"