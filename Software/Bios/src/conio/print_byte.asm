    .include "miniish.inc"
    .include "stdio.inc"
    .include "conio.inc"

    .global print_byte

    .section kernel

print_byte:
; Print a byte to device at the cursor position.
;
; args
; ----
; r0: The device to print out
; r1: the byte to print
; 
; notes
; -----
; N/A
;
    lda r0
    clc
    adc #device.put_char
    tax

    lda #%10000000
    sta r2

    ; loop 8 bits
    ldy #8
L1: lda r1
    and r2
    beq L4
    lda #'1'
    jsr call_ptr
    jmp L2
L4: lda #'0'
    jsr call_ptr
L2: ; next data
    dey
    beq L3
    lsr r2
    jmp L1
L3: rts
