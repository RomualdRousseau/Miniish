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
OAM_ADDR	= $7806
OAM_DATA	= $7807
DMA_ADDR	= $7808
DMA_DATA	= $7809

DMA_NAMETABLE = $00
DMA_ATTRIBUTE = $01
DMA_PALETTE	  = $02
DMA_PATTERN	  = $03

			.dsect			; BSS ==============================================
			.org ZERO_START
OAM_PTR 	.word $0000
LCD_PTR		.word $0000

STATE		.byte $00

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
COW_FG		.byte $00, $00, $00, $00
			.byte $00, $00, $00, $00
			.byte $00, $00, $00, $00
			.byte $00, $00, $00, $00
			.dend

			.org $8000		; CODE =============================================
SETUP
			; INIT STACK
			ldx #$FF
			txs
			; INIT OAM_DATA
			lda #<OAM_START
			sta OAM_PTR
			lda #>OAM_START
			sta OAM_PTR + 1
			; INIT GAME STATE
			lda #0
			sta STATE
			; INIT JOYPAD
			jsr JOYPAD_INIT
		 	; INIT LCD
			jsr LCD_INIT
			jsr LCD_CLEAR
			; PRINT MESSAGE1
			lda #<MESSAGE1
			sta LCD_PTR
			lda #>MESSAGE1
			sta LCD_PTR + 1
		 	jsr LCD_PRINT
		 	; PRINT MESSAGE2
		 	lda #<MESSAGE2
			sta LCD_PTR
			lda #>MESSAGE2
			sta LCD_PTR + 1
		 	jsr LCD_PRINT
		 	
LOOP
			jsr JOYPAD_READ
			jmp LOOP
			
DRAW
			pha
			txa
			pha
			lda R1
			pha
			; RUN STATE MACHINE
			lda STATE
			cmp #0
			beq STATE_INIT
			cmp #1
			beq STATE_GAME
			jmp STATE_END
STATE_INIT
			; RESET
			lda PPU_STATUS
			; LOAD PALETTES
			lda #$00
			sta DMA_ADDR
			lda #$00
			sta DMA_ADDR
			lda #DMA_PALETTE
			sta DMA_DATA
			; LOAD PATTERNS
			lda #$00
			sta DMA_ADDR
			lda #$20
			sta DMA_ADDR
			lda #DMA_PATTERN
			sta DMA_DATA
			; LOAD NAMETABLE
			lda #$04
			sta DMA_ADDR
			lda #$20
			sta DMA_ADDR
			lda #DMA_NAMETABLE
			sta DMA_DATA
			; INIT COW
			jsr COW_INIT
			lda #1
			sta STATE
			jmp STATE_END
STATE_GAME
			; Draw all
			jsr COW_DRAW
			; Update all
			jsr COW_UPDATE
			jmp STATE_END
STATE_END
			pla
			sta R1
			pla
			tax
			pla
			rti
			
							; IMPORTS ==========================================	  	
			.include "include/sys.inc"
			.include "include/lcd.inc"	
			.include "include/joypad.inc"
			.include "include/cow.inc"
			
							; DATA =============================================
MESSAGE1
			.asciiz "I am XiaoNiuNiu     "			
MESSAGE2
			.asciiz "Hello the world ^-^ "
ANIMATIONS
			.byte 2, 3, 4, 5, 2, 3, 6, 7

			.org $FFFA		; INTERRUPT VECTORS ================================
			.word DRAW
			.word SETUP
			.word $0000

