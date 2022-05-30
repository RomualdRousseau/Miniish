; lcd.i

lcd_en		= %10000000
lcd_rw		= %01000000
lcd_rs		= %00100000

lcd_init
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
 rts

lcd_clear
 lda #%00000001
 jsr lcd_send_cmd
 rts

lcd_home
 lda #%00000010
 jsr lcd_send_cmd
 rts

lcd_print
 ldy #0
lcd_print_loop
 lda (lcd_ptr), y
 beq lcd_print_end
 jsr lcd_send_char
 iny
 jmp lcd_print_loop
lcd_print_end
 rts

lcd_print_byte
 sta r2
 lda #%10000000
 sta r1
 ; loop 8 bits
 ldx #8
lcd_print_byte_1
 lda r2
 and r1
 beq lcd_print_byte_4
 lda #'1'
 jsr lcd_send_char
 jmp lcd_print_byte_2
lcd_print_byte_4
 lda #'0'
 jsr lcd_send_char
lcd_print_byte_2
 ; next data
 dex
 beq lcd_print_byte_3
 lsr r1
 jmp lcd_print_byte_1
lcd_print_byte_3
 rts

lcd_send_cmd
 jsr lcd_wait
 sta portb
 lda #0
 sta porta
 lda #lcd_en
 sta porta
 lda #0
 sta porta
 rts

lcd_send_char
 jsr lcd_wait
 sta portb
 lda #lcd_rs
 sta porta
 lda #(lcd_rs | lcd_en)
 sta porta
 lda #lcd_rs
 sta porta
 rts

lcd_wait
 pha
 lda #%00000000
 sta ddrb
lcd_wait_loop
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
