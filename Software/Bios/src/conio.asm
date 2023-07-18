    .include "miniish.inc"
    .include "conio.inc"

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
    adc #put_char
    tax
    ldy #0
print_loop:
    lda (r1), y
    beq print_end
    jsr call_dev_func
    iny
    jmp print_loop
print_end:
    rts
