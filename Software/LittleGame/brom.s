ZERO_START  = $0000
STCK_START	= $0100
OAM_START	= $0200

			.dsect			; BSS ==============================================
			.org ZERO_START
OAM_PTR 	.word $0000
LCD_PTR		.word $0000

STATE		  .byte $00

JOYPAD	  .byte $00

COW_X		  .byte $00
COW_Y		  .byte $00
COW_T		  .byte $00

NOTE		  .byte $00
SEQ			  .byte $00

R1			  .byte $00
R2			  .byte $00
R3			  .byte $00
R4			  .byte $00
R5			  .byte $00
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
			; INIT JOYPAD
			jsr JOYPAD_INIT
			; START AUDIO HANDLER
			cli
		 	
LOOP
			jsr JOYPAD_READ
			jsr JOYPAD_PRINT
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
			; LOAD ATTRIBUTE
			lda #$04
			sta DMA_ADDR
			lda #$E0
			sta DMA_ADDR
			lda #DMA_ATTRIBUTE
			sta DMA_DATA
			; INIT AUDIO
			jsr AUDIO_INIT
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
			
AUDIO
			pha
			bit T1CL
			lda JOYPAD
			beq AUDIO_END
			jsr AUDIO_PLAY
AUDIO_END
			pla
			rti
			
							; IMPORTS ==========================================	  	
			.include "include/sys.inc"
			.include "include/via.inc"
			.include "include/ppu.inc"
			.include "include/apu.inc"
			.include "include/lcd.inc"	
			.include "include/joypad.inc"
			.include "include/audio.inc"
			.include "include/cow.inc"
			
							; DATA =============================================
MESSAGE1
			.asciiz "I am XiaoNiuNiu     "			
MESSAGE2
			.asciiz "Hello the world ^-^ "
ANIMATIONS
			.byte 2, 3, 4, 5, 2, 3, 6, 7
BOARD
			.byte $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
			.byte $00, $0E, $0D, $0D, $0D, $0F, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
			.byte $00, $0A, $00, $00, $00, $0C, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
			.byte $00, $0A, $00, $00, $00, $0C, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
			.byte $00, $08, $00, $00, $0B, $09, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
			.byte $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
			.byte $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00
			.byte $00, $00, $0E, $00, $00, $0F, $00, $00, $00, $00, $0E, $0D, $0F, $00, $00, $00
			.byte $00, $00, $0A, $00, $00, $0C, $00, $00, $00, $00, $00, $00, $0C, $00, $00, $00
			.byte $00, $00, $0A, $00, $00, $0C, $00, $00, $00, $00, $00, $00, $0C, $00, $00, $00
			.byte $00, $00, $08, $0B, $0B, $09, $00, $00, $00, $00, $08, $0B, $09, $00, $00, $00
			.byte $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00, $00

			.org $FFFA		; INTERRUPT VECTORS ================================
			.word DRAW
			.word SETUP
			.word AUDIO

