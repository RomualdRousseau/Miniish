AUDIO_INIT
		 	; APU_CTRL(0,SINE,ENVELOPE1,60,64);
			lda #APU_SINE
			sta APU_CTRL_WAV0
			lda #APU_ENVELOPE1
			sta APU_CTRL_ENV0
			lda #60
			sta APU_CTRL_LEN0
			lda #APU_NEUTRAL
			sta APU_CTRL_MOD0
		 	; APU_CTRL(1,RAMP,ENVELOPE3,64,64)
			lda #APU_RAMP
			sta APU_CTRL_WAV1
			lda #APU_ENVELOPE3
			sta APU_CTRL_ENV1
			lda #64
			sta APU_CTRL_LEN1
			lda #APU_NEUTRAL
			sta APU_CTRL_MOD1
			; APU_CTRL(2,TRIANGLE,ENVELOPE2,70,64);
			lda APU_TRIANGLE
			sta APU_CTRL_WAV2
			lda #APU_ENVELOPE2
			sta APU_CTRL_ENV2
			lda #70
			sta APU_CTRL_LEN2
			lda #APU_NEUTRAL
			sta APU_CTRL_MOD2
			; APU_CTRL(3,NOISE,ENVELOPE3,20,64);
			lda APU_NOISE
			sta APU_CTRL_WAV3
			lda #APU_ENVELOPE3
			sta APU_CTRL_ENV3
			lda #20
			sta APU_CTRL_LEN3
			lda #APU_NEUTRAL
			sta APU_CTRL_MOD3
			; Set first sequence
			lda #0
			sta SEQ
			; Set first note
			lda #49
			sta NOTE
			; Install AUDIO handler
			lda #%11000000
			sta IER
		 	lda #%01000000
		 	sta ACR
		 	lda #$00
		 	sta T1LL
		 	lda #$01
		 	sta T1CH
			rts
			
AUDIO_PLAY
			; Check if APU is ready
			lda APU_STATUS
			and #%00000001
			bne AUDIO_PLAY_END
			; Switch SEQ
			lda SEQ
			cmp #0
			beq AUDIO_SEQ0
			cmp #1
			beq AUDIO_SEQ1
			cmp #2
			beq AUDIO_SEQ2
			jmp AUDIO_PLAY_END
AUDIO_SEQ0			
			lda NOTE
			sta APU_NOTE0
			lda NOTE
			sta APU_NOTE1
			lda #30
			sta APU_CTRL
			lda APU_STATUS
			inc SEQ
			jmp AUDIO_PLAY_END
AUDIO_SEQ1			
			lda #30
			sta APU_CTRL_LEN3
     		lda NOTE
			sta APU_NOTE3
			lda #15
			sta APU_CTRL
			lda APU_STATUS
			inc SEQ
			jmp AUDIO_PLAY_END
AUDIO_SEQ2
     		lda NOTE
			sta APU_NOTE2
			lda #30
			sta APU_CTRL_LEN3
     		lda NOTE
			sta APU_NOTE3
			lda #15
			sta APU_CTRL
			lda APU_STATUS
			lda #0
			sta SEQ
			inc NOTE
			lda NOTE
			cmp #51
			bne AUDIO_PLAY_END
			lda #49
			sta NOTE
			jmp AUDIO_PLAY_END
AUDIO_PLAY_END
			rts
	
