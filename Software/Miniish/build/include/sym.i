zero_start = $0000
stck_start = $0100
oam_start  = $0200
code_start = $8000
inte_start = $ffea

zero_user  = $0010
bss_user   = $0300
code_user  = $9000
data_user  = $a000

port_irq = $d000
port_ppu = $d100
port_apu = $d200
port_io	 = $d300

portb = port_io+$00
porta = port_io+$01
ddrb  = port_io+$02
ddra  = port_io+$03
t1cl  = port_io+$04
t1ch  = port_io+$05
t1ll  = port_io+$06
t1lh  = port_io+$07
t2cl  = port_io+$08
t2ch  = port_io+$08
acr   = port_io+$0b
ifr   = port_io+$0d
ier   = port_io+$0e

; vim:syntax=asmM6502
