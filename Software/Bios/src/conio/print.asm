    .include "miniish.inc"
    .include "stdio.inc"
    .include "conio.inc"

    .global print

    .section kernel

print:
; Print a message to device at the cursor position.
;
; args
; ----
; r0: The device to print out
; r1:r2: The pointer to the message in memory
; 
; notes
; -----
; N/A
;
    lda r0
    clc
    adc #device.put_char
    tax
 
    ldy #0
L1: lda (r1), y
    beq L2
    jsr call_ptr
    iny
    jmp L1
L2: rts
