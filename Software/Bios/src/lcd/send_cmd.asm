    .include "miniish.inc"
    .include "lcd.inc"

    .global lcd_send_cmd

    .section kernel

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
