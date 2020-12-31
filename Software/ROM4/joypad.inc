JPAD_DAT	= %00000001
JPAD_CLK	= %00000010
JPAD_LAT	= %00000100
JPAD_MSK	= %00000110

READ_JOYPAD
			lda #0
			sta R1
			; Read 8 bits
			ldx #8
READ_JOYPAD_1
			; Latch the joypad
			lda #%00000010 ;#(~JPAD_LAT & JPAD_MSK)
			sta PORTA
			lda #%00000000 ;#(~(JPAD_LAT | JPAD_CLK) & JPAD_MSK)
			sta PORTA
			; Read the joypad
			lda PORTA
			and #%00000001 ;#JPAD_DAT
			bne READ_JOYPAD_2
			; Add a bit 1 into JOYPAD
			inc R1
READ_JOYPAD_2
			; Next data
			dex
			beq READ_JOYPAD_3
			lda R1
			asl
			sta R1
			jmp READ_JOYPAD_1 
READ_JOYPAD_3		
			; Unlatch the joypad
			lda #%00000100 ;#(JPAD_LAT & JPAD_MSK)
			sta PORTA
			lda R1
			sta JOYPAD
			rts
