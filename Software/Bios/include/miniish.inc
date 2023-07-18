zero_start = $0000
stck_start = $0100
code_start = $8000
inte_start = $ffea

zero_user  = $0020
bss_user   = $0200
code_user  = $9000
data_user  = $a000

io_port1 = $d000
io_port2 = $d400
io_port3 = $d800
io_cia1  = $dc00
io_cia2  = $dd00
io_usr   = $de00
io_irq   = $df00

portb = io_cia1 + $00
porta = io_cia1 + $01
ddrb  = io_cia1 + $02
ddra  = io_cia1 + $03
t1cl  = io_cia1 + $04
t1ch  = io_cia1 + $05
t1ll  = io_cia1 + $06
t1lh  = io_cia1 + $07
t2cl  = io_cia1 + $08
t2ch  = io_cia1 + $08
acr   = io_cia1 + $0b
ifr   = io_cia1 + $0d
ier   = io_cia1 + $0e

r0  = zero_start + $00
r1  = zero_start + $01
r2  = zero_start + $02
r3  = zero_start + $03
r4  = zero_start + $04
r5  = zero_start + $05
r6  = zero_start + $06
r7  = zero_start + $07
r8  = zero_start + $08
r9  = zero_start + $09
r10 = zero_start + $0a
r11 = zero_start + $0b
r12 = zero_start + $0c
r13 = zero_start + $0d
r14 = zero_start + $0e
r15 = zero_start + $0f

dev_table = zero_start + $10
dev_lcd   = $00
dev_uart  = $08

; vim:syntax=asm
