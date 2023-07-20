    .include "miniish.inc"
    .include "lcd.inc"

    .global lcd_home

    .section kernel

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