    .include "miniish.inc"
    .include "stdio.inc"
    .include "conio.inc"

    .global print_byte

    .section kernel

print_byte:
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

    sta r2
    lda #%10000000
    sta r1

    ; loop 8 bits
    ldy #8
L1: lda r2
    and r1
    beq L4
    lda #'1'
    jsr call_ptr
    jmp L2
L4: lda #'0'
    jsr call_ptr
L2: ; next data
    dey
    beq L3
    lsr r1
    jmp L1
L3: rts
