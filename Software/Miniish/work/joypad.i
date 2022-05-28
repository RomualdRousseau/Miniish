; joypad.i

JPAD_DAT	= %00000100
JPAD_LAT	= %00000010
JPAD_CLK	= %00000001

JOYPAD_INIT
 ; Setup I/O
 lda DDRA
 ora #(JPAD_LAT | JPAD_CLK)
 and #~JPAD_DAT
 sta DDRA
 ; Initial state
 lda PORTA
 and #~(JPAD_LAT | JPAD_CLK)
 sta PORTA
 ; Inital value
 lda #0
 sta JOYPAD
 rts

JOYPAD_READ
 lda #0
 sta R1
 ; Latch the data
 lda PORTA
 ora #JPAD_LAT
 sta PORTA
 and #~JPAD_LAT
 sta PORTA
 ; Read 8 bits
 ldx #8
JOYPAD_READ_1
 ; Read the data
 lda PORTA
 and #JPAD_DAT
 bne JOYPAD_READ_2
 ; Add a bit 1 into JOYPAD
 inc R1
JOYPAD_READ_2
 ; Next data
 ora #JPAD_CLK
 sta PORTA
 and #~JPAD_CLK
 sta PORTA
 dex
 beq JOYPAD_READ_3
 asl R1
 jmp JOYPAD_READ_1
JOYPAD_READ_3
 ; Initial state
 lda PORTA
 and #~(JPAD_LAT | JPAD_CLK)
 sta PORTA
 lda R1
 sta JOYPAD
 rts
