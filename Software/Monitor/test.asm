    .org $0300

loop:
    lda #0
    sta $D002
    lda #2
    sta $D002
    lda #3
    sta $D002
L0: lda $D000
    bne L0
    nop
    nop
    nop
    nop
    lda #0
    sta $D002
    rts

; A9 00 8D 02 D0 A9 02 8D
; 02 D0 A9 03 8D 02 D0 AD
; 00 D0 D0 FB A9 00 8D 02
; D0 60

; loop:
;     lda $D000
;     sta $D000
;     lda #$FF
;     jsr $E01E
;     lda $D000
;     eor #$FF
;     sta $D000
;     lda #$FF
;     jsr $E01E
;     jmp loop

; AD 00 D0 8D 00 D0 A9 FF
; 20 1E E0 AD 00 D0 49 FF
; 8D 00 D0 A9 FF 20 1E E0
; 4C 00 03

