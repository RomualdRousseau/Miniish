JPAD_DAT	= %00000001
JPAD_CLK	= %00000010
JPAD_LAT	= %00000100
JPAD_MSK	= %00000110

JOYPAD_INIT
			lda #0
			sta JOYPAD
			rts
			
JOYPAD_READ
			lda #0
			sta R1
			; Read 8 bits
			ldx #8
JOYPAD_READ_1
			; Latch the joypad
			lda #(~JPAD_LAT & JPAD_MSK)
			sta PORTA
			lda #(~(JPAD_LAT | JPAD_CLK) & JPAD_MSK)
			sta PORTA
			; Read the joypad
			lda PORTA
			and #JPAD_DAT
			bne JOYPAD_READ_2
			; Add a bit 1 into JOYPAD
			inc R1
JOYPAD_READ_2
			; Next data
			dex
			beq JOYPAD_READ_3
			lda R1
			asl
			sta R1
			jmp JOYPAD_READ_1 
JOYPAD_READ_3		
			; Unlatch the joypad
			lda #(JPAD_LAT & JPAD_MSK)
			sta PORTA
			lda R1
			sta JOYPAD
			rts
