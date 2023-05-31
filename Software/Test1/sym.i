zero_start = $0000
stck_start = $0100
code_start = $8000
inte_start = $ffea

zero_user  = $0020
bss_user   = $0300
code_user  = $9000
data_user  = $a000

io_port1 = $d000
io_port2 = $d400
io_port3 = $d800
io_cia1  = $dc00
io_cia2  = $dd00
io_usr   = $de00
io_irq   = $df00

portb = io_cia1+$00
porta = io_cia1+$01
ddrb  = io_cia1+$02
ddra  = io_cia1+$03
t1cl  = io_cia1+$04
t1ch  = io_cia1+$05
t1ll  = io_cia1+$06
t1lh  = io_cia1+$07
t2cl  = io_cia1+$08
t2ch  = io_cia1+$08
acr   = io_cia1+$0b
ifr   = io_cia1+$0d
ier   = io_cia1+$0e

; vim:syntax=asm
