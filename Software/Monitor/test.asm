    .org $0300
loop:
    lda $D000
    sta $D000
    lda #$FF
    jsr $E01E
    lda $D000
    eor #$FF
    sta $D000
    lda #$FF
    jsr $E01E
    jmp loop

; AD 00 D0 8D 00 D0 A9 FF
; 20 1E E0 AD 00 D0 49 FF
; 8D 00 D0 A9 FF 20 1E E0
; 4C 00 03
