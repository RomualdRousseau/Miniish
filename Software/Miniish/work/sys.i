; sys.i

port_irq = $d000
port_ppu = $d100
port_apu = $d200
port_io	 = $d300

portb	= port_io + $00
porta = port_io + $01
ddrb  = port_io + $02
ddra  = port_io + $03
t1cl  = port_io + $04
t1ch  = port_io + $05
t1ll  = port_io + $06
t1lh  = port_io + $07
t2cl  = port_io + $08
t2ch  = port_io + $08
acr   = port_io + $0b
ifr   = port_io + $0d
ier   = port_io + $0e

ppu_ctrl    = port_ppu + $00
ppu_scroll  = port_ppu + $01
ppu_dmaspr  = port_ppu + $10
ppu_dmamap  = port_ppu + $11
ppu_dmaoam  = port_ppu + $12

irq_func
 phx
 ldx port_irq
 jmp (table_irq,x)

delay
 jsr delay_1ms
 sbc #1
 bne delay
 rts

delay_1ms
 pha
 lda #100
delay_1ms_loop
 nop
 nop
 nop
 sbc #1
 bne delay_1ms_loop
 pla
 rts
