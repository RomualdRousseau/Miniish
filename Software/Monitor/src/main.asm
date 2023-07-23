    .include "miniish.inc"
    .include "stdio.inc"

    .global main

    .section text

main:
    ; lda #0
    ; sta mem_start
    ; sta mem_start + 1
    ; sta mem_end
    ; sta mem_end + 1

    lda #dev_uart
    sta r0
    lda #<greeting
    sta r1
    lda #>greeting
    sta r2
    jsr print

main_loop:
    lda #dev_uart
    sta r0
    lda #<prompt
    sta r1
    lda #>prompt
    sta r2
    jsr print

    lda #0
    sta buf_start
    sta buf_end
    jsr get_new_line

    lda #0
    sta state
    jsr on_new_line

    jmp main_loop

    .section rodata

greeting:
    .byte "\e[2J\e[H"
    .byte "\e[1;32m","*** MINIISH V1.4 ***\e[0m\r\n"
    .byte "64K MEMORY SYSTEM    32K FREE RAM\r\n"
    .byte "READY.\r\n",0

prompt:
    .byte "\\ ",0
