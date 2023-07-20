    .include "miniish.inc"
    .include "uart.inc"

    .global uart_put_char

    .section kernel

uart_put_char:
; Write a single character to the uart port.
;
; args
; ----
; A: The character to write.
; 
; notes
; -----
; N/A
;
    jsr uart_wait_tx
    ; transmit data
    sta uart_data_reg
    rts
