COW_DRAW
			lda PPU_STATUS
			; Draw COW BG
			lda #0
			sta PPU_ADDR
			lda COW_BG+0
			sta PPU_ADDR
			lda #0
			sta PPU_DATA
			sta PPU_DATA
			lda #0
			sta PPU_ADDR
			lda COW_BG+4
			sta PPU_ADDR
			lda #0
			sta PPU_DATA
			sta PPU_DATA
			; Draw COW FG
			lda #0
			sta PPU_ADDR
			lda COW_FG+0
			sta PPU_ADDR
			lda COW_FG+1
			sta PPU_DATA
			lda COW_FG+3
			sta PPU_DATA
			lda #0
			sta PPU_ADDR
			lda COW_FG+4
			sta PPU_ADDR
			lda COW_FG+5
			sta PPU_DATA
			lda COW_FG+7
			sta PPU_DATA
			rts
			
COW_UPDATE
			lda JOYPAD
			cmp #0
			bne COW_UPDATE_TEST_KEY_DOWN
			rts
COW_UPDATE_TEST_KEY_DOWN
			lda JOYPAD
			and #%00000010
			beq COW_UPDATE_TEST_KEY_UP
			lda COW_Y
			cmp #0
			beq COW_UPDATE_TEST_KEY_UP
			dec	COW_Y
COW_UPDATE_TEST_KEY_UP
			lda JOYPAD
			and #%00000100
			beq COW_UPDATE_TEST_KEY_LEFT
			lda COW_Y
			cmp #10
			beq COW_UPDATE_TEST_KEY_LEFT
			inc	COW_Y
COW_UPDATE_TEST_KEY_LEFT
			lda JOYPAD
			and #%00001000
			beq COW_UPDATE_TEST_KEY_RIGHT
			lda COW_X
			cmp #0
			beq COW_UPDATE_TEST_KEY_RIGHT
			dec	COW_X
COW_UPDATE_TEST_KEY_RIGHT
			lda JOYPAD
			and #%00000001
			beq COW_UPDATE_INC_TIME
			lda COW_X
			cmp #18
			beq COW_UPDATE_INC_TIME
			inc	COW_X
COW_UPDATE_INC_TIME
			lda COW_T
			clc
			adc #1
			sta COW_T
			jsr COW_REFRESH
			rts
			
COW_REFRESH			
			; Save COW_FG -> COW_BG
			lda COW_FG+0
			sta COW_BG+0
			lda COW_FG+2
			sta COW_BG+2
			lda COW_FG+4
			sta COW_BG+4
			lda COW_FG+6
			sta COW_BG+6
			; Calculate position = COW_X + COW_Y * 20
			lda COW_X
			ldx #20
			clc	
COW_REFRESH_CALC_POS			
			adc COW_Y
			dex
			bne COW_REFRESH_CALC_POS
			; Refresh next positions in OAM
			sta COW_FG+0
			adc #1
			sta COW_FG+2
			adc #19
			sta COW_FG+4
			adc #1
			sta COW_FG+6
			; Refresh next animations in OAM
			lda COW_T
			and #%00000010
			asl
			tax
			lda ANIMATIONS, x
			sta COW_FG+1
			inx
			lda ANIMATIONS, x
			sta COW_FG+3
			inx
			lda ANIMATIONS, x
			sta COW_FG+5
			inx
			lda ANIMATIONS, x
			sta COW_FG+7
			rts
			
