

PORT_IRQ = $D000
PORT_PPU = $D100
PORT_APU = $D200
PORT_IO	 = $D300

PORTB		= PORT_IO + $00
PORTA		= PORT_IO + $01
DDRB		= PORT_IO + $02
DDRA		= PORT_IO + $03
T1CL		= PORT_IO + $04
T1CH		= PORT_IO + $05
T1LL		= PORT_IO + $06
T1LH		= PORT_IO + $07
T2CL		= PORT_IO + $08
T2CH		= PORT_IO + $08
ACR			= PORT_IO + $0B
IFR			= PORT_IO + $0D
IER			= PORT_IO + $0E

IRQ_FUNC:
			phx
			ldx PORT_IRQ
      jmp (TABLE_IRQ,X)
      
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
