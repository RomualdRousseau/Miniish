ZERO_START  = $0000
STCK_START	= $0100
OAM_START	= $0200

PORTB		= $7000
PORTA		= $7001
DDRB		= $7002
DDRA		= $7003

PPU_CTRL	= $7800
PPU_STATUS	= $7802
PPU_ADDR	= $7803
PPU_DATA	= $7804

			.dsect			; BSS ==============================================
			.org ZERO_START
OAM_DATA 	.word $0000
LCD_DATA	.word $0000

JOYPAD		.byte $00

COW_X		.byte $00
COW_Y		.byte $00
COW_T		.byte $00

R1			.byte $00
R2			.byte $00
R3			.byte $00
			.dend

			.dsect			; OAM =============================================
			.org OAM_START
COW_FG		.byte $00, $00
			.byte $00, $00
			.byte $00, $00
			.byte $00, $00
COW_BG		.byte $00, $00
			.byte $00, $00
			.byte $00, $00
			.byte $00, $00
			.dend

			.org $8000		; CODE =============================================
SETUP
			ldx #$FF
			txs
			; INIT OAM_DATA
			lda #<OAM_START
			sta OAM_DATA
			lda #>OAM_START
			sta OAM_DATA + 1
			; INIT COW
			lda #9
			sta COW_X
			lda #5
			sta COW_Y
			lda #0
			sta COW_T
			jsr COW_REFRESH
		 	; INIT LCD
			jsr LCD_INIT
			jsr LCD_CLEAR
			; PRINT MESSAGE1
			lda #<MESSAGE1
			sta LCD_DATA
			lda #>MESSAGE1
			sta LCD_DATA + 1
		 	jsr LCD_PRINT
		 	; PRINT MESSAGE2
		 	lda #<MESSAGE2
			sta LCD_DATA
			lda #>MESSAGE2
			sta LCD_DATA + 1
		 	jsr LCD_PRINT
		 	
LOOP
			jsr READ_JOYPAD
			jmp LOOP
			
DRAW
			pha
			txa
			pha
			lda R1
			pha
			; Draw all
			jsr COW_DRAW
			; Update all
			jsr COW_UPDATE
			pla
			sta R1
			pla
			tax
			pla
			rti
			
							; IMPORTS ==========================================	  	
			.include "sys.inc"
			.include "lcd.inc"	
			.include "joypad.inc"
			.include "cow.inc"
			
							; DATA =============================================
MESSAGE1
			.asciiz "I am XiaoNiuNiu     "			
MESSAGE2
			.asciiz "Hello the world ^-^ "
ANIMATIONS
			.byte 4, 5, 12, 13, 4, 5, 14, 15

			.org $FFFA		; INTERRUPT VECTORS ================================
			.word DRAW
			.word SETUP
			.word $0000

