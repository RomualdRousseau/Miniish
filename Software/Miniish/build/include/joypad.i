jpad_dat = %00000100
jpad_lat = %00000010
jpad_clk = %00000001

joypad_init
 ; setup i/o
 lda ddra
 ora #(jpad_lat | jpad_clk)
 and #~jpad_dat
 sta ddra
 ; initial state
 lda porta
 and #~(jpad_lat | jpad_clk)
 sta porta
 ; inital value
 lda #0
 sta joypad
 rts

joypad_read
 lda #0
 sta r1
 ; latch the data
 lda porta
 ora #jpad_lat
 sta porta
 and #~jpad_lat
 sta porta
 ; read 8 bits
 ldx #8
joypad_read_1
 ; read the data
 lda porta
 and #jpad_dat
 bne joypad_read_2
 ; add a bit 1 into joypad
 inc r1
joypad_read_2
 ; next data
 ora #jpad_clk
 sta porta
 and #~jpad_clk
 sta porta
 dex
 beq joypad_read_3
 asl r1
 jmp joypad_read_1
joypad_read_3
 ; initial state
 lda porta
 and #~(jpad_lat | jpad_clk)
 sta porta
 lda r1
 sta joypad
 rts

; vim:syntax=asmM6502
