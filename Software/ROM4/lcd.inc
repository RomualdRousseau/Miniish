LCD_EN		= %10000000
LCD_RW		= %01000000
LCD_RS		= %00100000

LCD_INIT
			lda #%11100110
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
			
LCD_HOME
			lda #%00000010
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
