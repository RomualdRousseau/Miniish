.PHONY: burn_brom burn_vrom all clean

default: burn_brom

brom.bin: include/*.inc brom.s
	vasm6502_oldstyle -Fbin -dotdir -o brom.bin brom.s

vrom.bin: vrom.py lib/ppu.py
	python2 vrom.py
	
burn_brom: brom.bin
	minipro -p AT28C256 -w brom.bin
	
burn_vrom: vrom.bin
	minipro -p AT28C256 -w vrom.bin

all: brom.bin vrom.bin

clean:
	rm -f *.bin
		
