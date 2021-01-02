COW_INIT
			lda #72
			sta COW_X
			lda #45
			sta COW_Y
			lda #0
			sta COW_T
			jsr COW_REFRESH
			rts
			
COW_DRAW
			; Reset
			lda PPU_STATUS
			; Set OAM to start
			lda #0
			sta OAM_ADDR
			; Load OAM
			ldx #0
COW_DRAW_LOAD_OAM
			lda COW_FG,x
			sta OAM_DATA
			inx
			cpx #16
			bne COW_DRAW_LOAD_OAM
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
			cmp #80
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
			cmp #112
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
			; Refresh X positions
			lda COW_X
			sta COW_FG+3
			sta COW_FG+11
			clc
			adc #8
			sta COW_FG+7
			sta COW_FG+15
			; Refresh Y positions
			lda COW_Y
			sta COW_FG+0
			sta COW_FG+4
			clc
			adc #8
			sta COW_FG+8
			sta COW_FG+12
			; Refresh next animations in OAM
			lda COW_T
			and #%00000010
			asl
			tax
			lda ANIMATIONS, x
			sta COW_FG+1
			inx
			lda ANIMATIONS, x
			sta COW_FG+5
			inx
			lda ANIMATIONS, x
			sta COW_FG+9
			inx
			lda ANIMATIONS, x
			sta COW_FG+13
			; Show sprite with palette 0
			lda #%00000100
			sta COW_FG+2
			sta COW_FG+6
			sta COW_FG+10
			sta COW_FG+14
			rts
			
