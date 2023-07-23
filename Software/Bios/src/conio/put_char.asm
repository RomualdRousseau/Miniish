    .include "miniish.inc"
    .include "stdio.inc"
    .include "conio.inc"

    .global put_char

    .section kernel

put_char:
; Write a single character to the device at the cursor position.
;
; args
; ----
; r0: The device to print out
; r1: The character to write.
; 
; notes
; -----
; N/A
;
    lda r0
    clc
    adc #device.put_char
    tax
    lda r1
    jsr call_ptr
    rts
