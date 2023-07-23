    .include "miniish.inc"

    .global delay
    .global delay_1ms

    .section kernel

delay:
; Delay by A milliseconds
;
; args
; ----
; A : The number of milliseconds to delay.
; 
; notes
; -----
; N/A
;
    sec
    jsr delay_1ms
    sbc #1
    bne delay
    rts

delay_1ms:
; Delay by 1 millisecond.
;
; args
; ----
; N/A
; 
; notes
; -----
; This is a rough estimate based on the assertion of the CPU speed of 1MHz and 
; the number of cycles.
;
    pha
    lda #100
L1: nop
    nop
    nop
    sbc #1
    bne L1
    pla
    rts
 