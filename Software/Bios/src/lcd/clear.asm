    .include "miniish.inc"
    .include "lcd.inc"

    .global lcd_clear

    .section kernel

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