    .include "miniish.inc"
    .include "stdio.inc"
    .include "lcd.inc"

    .global lcd_init

    .section kernel

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
    ; load dev vtable
    ldx #dev_lcd
    lda #<lcd_send_cmd  
    sta dev_table + 0, x
    lda #>lcd_send_cmd
    sta dev_table + 1, x
    lda #<lcd_put_char
    sta dev_table + 2, x
    lda #>lcd_put_char
    sta dev_table + 3, x
    lda #0
    sta dev_table + 4, x
    lda #0
    sta dev_table + 5, x
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
