    .include "miniish.inc"
    .include "uart.inc"

    .global uart_wait_rx

    .section kernel

uart_wait_rx:
    ; disable interrupts
    sei
    lda #%00001011
    sta uart_command_reg
    ; check if receiver if full
    lda #%00001000
L1: bit uart_status_reg
    beq L1
    cli
    rts
