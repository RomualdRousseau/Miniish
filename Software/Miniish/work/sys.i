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
ppu_status  = port_ppu + $01
ppu_scroll  = port_ppu + $04
ppu_dmaspr  = port_ppu + $10
ppu_dmamap  = port_ppu + $11
ppu_dmaoam  = port_ppu + $12

apu_ctrl   = port_apu + $0a
apu_status = port_apu + $00
apu_wav0   = port_apu + $01
apu_env0   = port_apu + $02
apu_len0   = port_apu + $03
apu_mod0   = port_apu + $04
apu_not0   = port_apu + $05
apu_wav1   = port_apu + $11
apu_env1   = port_apu + $12
apu_len1   = port_apu + $13
apu_mod1   = port_apu + $14
apu_not1   = port_apu + $15
apu_wav2   = port_apu + $21
apu_env2   = port_apu + $22
apu_len2   = port_apu + $23
apu_mod2   = port_apu + $24
apu_not2   = port_apu + $25
apu_wav3   = port_apu + $31
apu_env3   = port_apu + $32
apu_len3   = port_apu + $33
apu_mod3   = port_apu + $34
apu_not3   = port_apu + $35

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
