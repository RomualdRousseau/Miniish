neg .macro 
 eor #$ff
 clc
 adc #1
 .endm

div2
 bpl div2_1
 neg 
 lsr
 neg
 rts
div2_1
 lsr
 rts

div4
 bpl div4_1
 neg 
 lsr
 lsr
 neg
 rts
div4_1
 lsr
 lsr
 rts

; vim:syntax=asmM6502
