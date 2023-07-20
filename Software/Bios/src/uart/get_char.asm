    .include "miniish.inc"
    .include "uart.inc"

    .global uart_get_char

    .section kernel

uart_get_char:
; Read a single character from the uart port.
;
; args
; ----
; N/A
; 
; notes
; -----
; N/A
;
; Return the character in A
;
    jsr uart_wait_rx
    ; read data
    lda uart_data_reg
    rts

