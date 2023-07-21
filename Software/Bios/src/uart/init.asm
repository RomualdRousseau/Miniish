    .include "miniish.inc"
    .include "stdio.inc"
    .include "uart.inc"

    .global uart_init

    .section kernel

uart_init:
; Initialize and the uart port.
;
; args
; ----
; N/A
; 
; notes
; -----
; N/A
;
    sei
    ; load dev vtable
    ldx #dev_uart
    lda #0
    sta dev_table + 0, x
    lda #0
    sta dev_table + 1, x
    lda #<uart_put_char
    sta dev_table + 2, x
    lda #>uart_put_char
    sta dev_table + 3, x
    lda #<uart_get_char
    sta dev_table + 4, x
    lda #>uart_get_char
    sta dev_table + 5, x
    ; soft reset
    lda #0
    sta uart_status_reg
    ; 1 Stop bit, 8 bits, Baud rate 19,200
    lda #%00011111
    sta uart_control_reg
    ; no parity, no echo, no interrupts
    lda #%00001011
    sta uart_command_reg
    cli
    rts
