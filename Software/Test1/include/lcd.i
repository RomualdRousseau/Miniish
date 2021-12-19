LCD_EN		= %10000000
LCD_RW		= %01000000
LCD_RS		= %00100000

LCD_INIT
			; Setup I/O
			lda DDRA
			ora #(LCD_EN | LCD_RW | LCD_RS)
			sta DDRA
			lda #%11111111
			sta DDRB
			; Interface: 8bits, Line: 2, Font: 5x8 
			lda #%00111000		
			jsr LCD_SEND_CMD
			; Display: On, Cursor: Off, Blink: Off
			lda #%00001100		
			jsr LCD_SEND_CMD
			; Shift: Right 
			lda #%00000110		
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
			lda (LCD_PTR), y
			beq LCD_PRINT_END
			jsr LCD_SEND_CHAR
			iny
			jmp LCD_PRINT_LOOP
LCD_PRINT_END
			rts
			
LCD_PRINT_BYTE
			sta R2
      lda #%10000000
			sta R1
      ; Loop 8 bits
			ldx #8
LCD_PRINT_BYTE_1
      lda R2
      and R1
      beq LCD_PRINT_BYTE_4
      lda #'1'
      jsr LCD_SEND_CHAR
      jmp LCD_PRINT_BYTE_2
LCD_PRINT_BYTE_4
      lda #'0'
      jsr LCD_SEND_CHAR
LCD_PRINT_BYTE_2
      ; Next data
			dex
			beq LCD_PRINT_BYTE_3
			lsr R1
			jmp LCD_PRINT_BYTE_1 
LCD_PRINT_BYTE_3
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
