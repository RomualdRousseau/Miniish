    .include "miniish.inc"
    .include "lcd.inc"

    .global lcd_put_char

    .section kernel

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
