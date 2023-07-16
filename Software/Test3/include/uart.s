uart_port        = io_port3
uart_data_reg    = uart_port + $00
uart_status_reg  = uart_port + $01
uart_command_reg = uart_port + $02
uart_control_reg = uart_port + $03
uart_status_tde  = zero_start + $10

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

uart_print:
; Print a message to the uart port.
;
; args
; ----
; r0:r1: The pointer to the message in memory
; 
; notes
; -----
; N/A
;
    ldy #0
uart_print_loop:
    lda (r0), y
    beq uart_print_end
    jsr uart_put_char
    iny
    jmp uart_print_loop
uart_print_end:
    rts

uart_print_byte:
; Print a byte contained in A as a binary of 8 bits.
;
; args
; ----
; A: The byte to print.
; 
; notes
; -----
; N/A
;
    sta r2
    lda #%10000000
    sta r1
    ; loop 8 bits
    ldx #8
uart_print_byte_1:
    lda r2
    and r1
    beq uart_print_byte_4
    lda #'1'
    jsr uart_put_char
    jmp uart_print_byte_2
uart_print_byte_4:
    lda #'0'
    jsr uart_put_char
uart_print_byte_2:
    ; next data
    dex
    beq uart_print_byte_3
    lsr r1
    jmp uart_print_byte_1
uart_print_byte_3:
    rts

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

; private functions

uart_wait_rx:
    ; disable interrupts
    sei
    lda #%00001011
    sta uart_command_reg
    ; check if receiver if full
    lda #%00001000
uart_wait_rx_not_full:
    bit uart_status_reg
    beq uart_wait_rx_not_full
    cli
    rts

uart_wait_tx:
    pha
    ; enable transmit interrupt 
    lda #%00000111
    sta uart_command_reg
    ; set the transmit data to not empty
    lda #0
    sta uart_status_tde
    ; wait for transmit data empty
uart_wait_tx_not_empty:
    lda uart_status_tde
    beq uart_wait_tx_not_empty
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

; vim:syntax=asm
