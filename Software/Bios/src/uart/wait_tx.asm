    .include "miniish.inc"
    .include "uart.inc"

    .global uart_wait_tx
    .global uart_int_func

    .section kernel

uart_wait_tx:
    pha
    ; enable transmit interrupt 
    lda #%00000111
    sta uart_command_reg
    ; set the transmit data to not empty
    lda #0
    sta uart_status_tde
    ; wait for transmit data empty
L1: lda uart_status_tde
    beq L1
    pla
    rts

uart_int_func:
    pha
    ; reset interrupt
    lda uart_status_reg
    ; set the transmit data to empty
    lda #1
    sta uart_status_tde
    ; Disable transmit interrupt 
    lda #%00001011
    sta uart_command_reg
    pla
    plx
    rti
