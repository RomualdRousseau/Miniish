PORTB		= $7000
PORTA		= $7001
DDRB		= $7002
DDRA		= $7003

LCD_EN		= %10000000
LCD_RW		= %01000000
LCD_RS		= %00100000
LCD_DATA	= $0000

			.org $E000		; DATA ============================================
MESSAGE1
			.asciiz "I am XiaoNiuNiu     "			
MESSAGE2
			.asciiz "Hello the world ^-^ "
 
			.org $8000		; CODE ============================================
SETUP
			ldx #$FF
			txs
			lda #10
			jsr DELAY
		   
		   	; INIT LCD
		   
			jsr LCD_INIT
			
			jsr LCD_CLEAR
			
			; PRINT MESSAGE1
			
			lda #MESSAGE1 & 0xFF
			sta LCD_DATA
			lda #MESSAGE1 >> 8 & 0xFF
			sta LCD_DATA + 1
		 	jsr LCD_PRINT
		 	
		 	; PRINT MESSAGE2
		 	
		 	lda #MESSAGE2 & 0xFF
			sta LCD_DATA
			lda #MESSAGE2 >> 8 & 0xFF
			sta LCD_DATA + 1
		 	jsr LCD_PRINT
 
LOOP
		  	jmp LOOP

LCD_INIT
			lda #%11100000
			sta DDRA
			lda #%11111111
			sta DDRB
			lda #%00111000		; Interface: 8bits, Line: 2, Font: 5x8 
			jsr LCD_SEND_CMD
			lda #%00001100		; Display: On, Cursor: Off, Blink: Off
			jsr LCD_SEND_CMD
			lda #%00000110		; Shift: Right 
			jsr LCD_SEND_CMD
			rts

LCD_CLEAR
			lda #%00000001
			jsr LCD_SEND_CMD
			rts

LCD_PRINT
			ldy #0
LCD_PRINT_LOOP
			lda (LCD_DATA), y
			beq LCD_PRINT_END
			jsr LCD_SEND_CHAR
			iny
			jmp LCD_PRINT_LOOP
LCD_PRINT_END
			rts

LCD_SEND_CMD
			jsr LCD_WAIT
			sta PORTB 
			lda #0
			sta PORTA 
			lda #LCD_EN
			sta PORTA
			lda #0
			sta PORTA
			rts
			
LCD_SEND_CHAR
			jsr LCD_WAIT
			sta PORTB 
			lda #LCD_RS
			sta PORTA
			lda #(LCD_RS | LCD_EN)
			sta PORTA
			lda #LCD_RS
			sta PORTA
			rts
			
LCD_WAIT
			pha
			lda #%00000000
			sta DDRB
LCD_WAIT_LOOP
			lda #LCD_RW
			sta PORTA
			lda #(LCD_RW | LCD_EN)
			sta PORTA 
			lda PORTB
			and #%10000000
			bne LCD_WAIT_LOOP
			lda #LCD_RW
			sta PORTA
			lda #%11111111
			sta DDRB
			pla
			rts
  
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
			
NMI
			rti
   
			.org $FFFA		; TABLE ===========================================
			.word NMI
			.word SETUP
			.word $0000

