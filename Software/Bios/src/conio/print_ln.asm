    .include "miniish.inc"
    .include "stdio.inc"
    .include "conio.inc"

    .global print_ln

    .section kernel

print_ln:
; Print a new line to device at the cursor position.
;
; args
; ----
; r0: The device to print out
; 
; notes
; -----
; N/A
;
    lda #'\r'
    sta r1
    jsr put_char
    lda #'\n'
    sta r1
    jsr put_char
    rts
