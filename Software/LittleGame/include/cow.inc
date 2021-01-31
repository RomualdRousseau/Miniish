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
			lda COW_X
			sta R3
			lda COW_Y
			sta R4
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
			inc COW_T
			jsr COW_COLLIDE
			jsr COW_REFRESH
			rts

COW_COLLIDE
			; Check top, left corner
			lda COW_X
			sta R1
			lda COW_Y
			sta R2
			jsr COW_POINT_COLLIDE
			; Check top, middle corner
			lda R1
			clc
			adc #7
			sta R1
			lda R3
			clc
			adc #7
			sta R3
			jsr COW_POINT_COLLIDE
			; Check top, right corner
			lda R1
			clc
			adc #8
			sta R1
			lda R3
			clc
			adc #8
			sta R3
			jsr COW_POINT_COLLIDE
			; Check middle, right corner
			lda R2
			clc			
			adc #7
			sta R2
			lda R4
			clc
			adc #7
			sta R4
			jsr COW_POINT_COLLIDE
			; Check bottom, right corner
			lda R2
			clc			
			adc #8
			sta R2
			lda R4
			clc
			adc #8
			sta R4
			jsr COW_POINT_COLLIDE
			; Check bottom, middle corner
			lda R1
			clc
			adc #-8
			sta R1
			lda R3
			clc
			adc #-8
			sta R3
			jsr COW_POINT_COLLIDE
			; Check bottom, left corner
			lda R1
			clc
			adc #-7
			sta R1
			lda R3
			clc
			adc #-7
			sta R3
			jsr COW_POINT_COLLIDE
			rts
			
COW_POINT_COLLIDE
			lda R1
			lsr
			lsr
			lsr
			sta R5
			lda R2
			and #%11111000
			asl
			clc
			adc R5
			tax
			lda BOARD, X
			cmp #00
			bne COW_ADJUST_POSITION
			rts
COW_ADJUST_POSITION
			; COW_X = COW_X - (R1 / 8 - R3 / 8)
			lda R3
			lsr
			lsr
			lsr
			sta R5
			lda R1
			lsr
			lsr
			lsr
			clc
			sbc R5
			sta R5
			lda COW_X
			clc
			sbc R5
			sta COW_X
			; COW_Y = COW_Y - (R2 / 8 - R4 / 8)
			lda R4
			lsr
			lsr
			lsr
			sta R5
			lda R2
			lsr
			lsr
			lsr
			clc
			sbc R5
			sta R5
			lda COW_Y
			clc
			sbc R5
			sta COW_Y
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
			
