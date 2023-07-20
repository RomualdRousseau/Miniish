    .include "miniish.inc"
    .include "lcd.inc"

    .global lcd_wait

    .section kernel

lcd_wait:
    pha
    lda #%00000000
    sta ddrb
L1: lda #lcd_rw
    sta porta
    lda #(lcd_rw | lcd_en)
    sta porta
    lda portb
    and #%10000000
    bne L1
    lda #lcd_rw
    sta porta
    lda #%11111111
    sta ddrb
    pla
    rts
