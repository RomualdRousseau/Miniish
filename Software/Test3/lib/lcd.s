lcd_en = %10000000
lcd_rw = %01000000
lcd_rs = %00100000

lcd_vtable:
    .word lcd_send_cmd
    .word lcd_put_char
    .word $0000
    .word $0000

lcd_init:
; Initialize and clear the LCD display.
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
    ; setup i/o
    lda ddra
    ora #(lcd_en | lcd_rw | lcd_rs)
    sta ddra
    lda #%11111111
    sta ddrb
    ; interface: 8bits, line: 2, font: 5x8
    lda #%00111000
    jsr lcd_send_cmd
    ; display: on, cursor: off, blink: off
    lda #%00001100
    jsr lcd_send_cmd
    ; shift: right
    lda #%00000110
    jsr lcd_send_cmd
    ; clear display
    lda #%00000001
    jsr lcd_send_cmd
    cli
    rts

lcd_clear:
; Clear the LCD display.
;
; args
; ----
; N/A
; 
; notes
; -----
; N/A
;
    lda #%00000001
    jsr lcd_send_cmd
    rts

lcd_home:
; Set the cursor to the home posiiton (0,0).
;
; args
; ----
; N/A
; 
; notes
; -----
; N/A
;
    lda #%00000010
    jsr lcd_send_cmd
    rts

lcd_print:
; Print a message to LCD display at the cursor position.
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
lcd_print_loop:
    lda (r0), y
    beq lcd_print_end
    jsr lcd_put_char
    iny
    jmp lcd_print_loop
lcd_print_end:
    rts

lcd_print_byte:
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
lcd_print_byte_1:
    lda r2
    and r1
    beq lcd_print_byte_4
    lda #'1'
    jsr lcd_put_char
    jmp lcd_print_byte_2
lcd_print_byte_4:
    lda #'0'
    jsr lcd_put_char
lcd_print_byte_2:
    ; next data
    dex
    beq lcd_print_byte_3
    lsr r1
    jmp lcd_print_byte_1
lcd_print_byte_3:
    rts

lcd_put_char:
; Write a single character to the LCD display.
;
; args
; ----
; A: The character to write.
; 
; notes
; -----
; N/A
;
    jsr lcd_wait
    sta portb
    lda #lcd_rs
    sta porta
    lda #(lcd_rs | lcd_en)
    sta porta
    lda #lcd_rs
    sta porta
    rts

lcd_send_cmd:
; Send a command to the LCD display.
;
; args
; ----
; A: The command to send.
; 
; notes
; -----
; N/A
;
    jsr lcd_wait
    sta portb
    lda #0
    sta porta
    lda #lcd_en
    sta porta
    lda #0
    sta porta
    rts

; private functions

lcd_wait:
    pha
    lda #%00000000
    sta ddrb
lcd_wait_loop:
    lda #lcd_rw
    sta porta
    lda #(lcd_rw | lcd_en)
    sta porta
    lda portb
    and #%10000000
    bne lcd_wait_loop
    lda #lcd_rw
    sta porta
    lda #%11111111
    sta ddrb
    pla
    rts

; vim:syntax=asm
