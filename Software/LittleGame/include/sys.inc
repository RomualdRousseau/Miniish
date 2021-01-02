DELAY
			jsr DELAY_1ms
			sbc #1
			bne DELAY
			rts
  
DELAY_1ms
			pha
			lda #100
DELAY_1ms_LOOP
			nop
			nop
			nop
			sbc #1
			bne DELAY_1ms_LOOP
			pla
			rts
