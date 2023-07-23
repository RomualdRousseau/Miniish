    .org $0300
loop:
    lda #$55
    sta $D000
    lda #$FF
    jsr $E01E
    lda #$AA
    sta $D000
    lda #$FF
    jsr $E01E
    rts

; A9 55 8D 00 D0 A9 FF 20 1E E0 A9 AA 8D 00 D0 A9 FF 20 1E E0 60
; A9 55 8D 00 D0 A9 FF 20 1E E0 A9 AA 8D 00 D0 A9 FF 20 1E E0 4C 00 03