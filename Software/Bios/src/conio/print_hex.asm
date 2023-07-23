    .include "miniish.inc"
    .include "stdio.inc"
    .include "conio.inc"

    .global print_hex

    .section kernel

print_hex:
; Print a byte as hex to device at the cursor position.
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

    ; loop 2 nibbles
    ldy #2
L0: lda r1
    lsr
    lsr
    lsr
    lsr
    
    ; convert byte in hex
    cmp #10
    bcc L1
    sec
    sbc #10
    clc
    adc #'A'
    bra L2
L1: clc
    adc #'0'
L2: jsr call_ptr

    asl r1
    asl r1
    asl r1
    asl r1

    dey
    beq L4
    jmp L0
L4: rts
