    .include "miniish.inc"
    .include "stdio.inc"

    .global xtob, asl_16, adc_16, inc_16, cmp_16

    .section text

xtob:
; Convert a character representing a hex to a byte
;
; args
; ----
; A: the character to convert
; 
; notes
; -----
; N/A
; 
; return the byte in A
;
    ; check if token is '0' .. '9'
    cmp #'0'
    bcs L0
    bra L1
L0: cmp #'9'
    bcc L3
    beq L3
    bra L1

    ; check if token is 'A' .. 'F'
L1: cmp #'A'
    bcs L2
    bra L5
L2: cmp #'F'
    bcc L4
    beq L4
    bra L5

    ; convert character '0' .. '9' to 0 .. 9
L3: sec 
    sbc #'0'
    bra L5

    ; convert character 'A' .. 'F' to 10 .. 15
L4: sec
    sbc #'A'
    clc
    adc #10
L5: rts

asl_16:
; Perform a Y shift left of word r0:r1
;
; args
; ----
; Y: the number of shift left
; r0:r1: the word to shift
; 
; notes
; -----
; N/A
;
L6: lda r0
    asl
    sta r0
    lda r1
    rol
    sta r1
    dey
    bne L6
    rts

adc_16:
; Add a byte to an word
;
; args
; ----
; r0:r1: the word
; r2: the byte to add
; 
; notes
; -----
; N/A
;
    clc
    lda r0
    adc r2
    sta r0
    lda r1
    adc #0
    sta r1
    rts

inc_16:
; Increment a word
;
; args
; ----
; r0:r1: the word to increment
; 
; notes
; -----
; N/A
;
    clc
    lda r0
    adc #1
    sta r0
    lda r1
    adc #0
    sta r1
    rts

cmp_16:
; Add a byte to an word
;
; args
; ----
; r0:r1: the word
; r2:r3: the byte to add
; 
; notes
; -----
; N/A
;
    lda r0
    cmp r2
    bne L7
    lda r1
    cmp r3
L7: rts