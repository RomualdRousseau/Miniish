    .include "miniish.inc"
    .include "stdio.inc"
    .include "conio.inc"

    .global get_char

    .section kernel

get_char:
; Read a single character from the device.
;
; args
; ----
; r0: The device to read in
; 
; notes
; -----
; N/A
;
    lda r0
    clc
    adc #device.get_char
    tax
    jsr call_ptr
    rts
