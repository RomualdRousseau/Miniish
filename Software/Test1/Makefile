.PHONY: burn all clean

default: all

rom.bin: include/*.i rom.s
	vasm6502_oldstyle -c02 -Fbin -dotdir -o rom.bin rom.s

burn: rom.bin
	minipro -p AT28C256 -w rom.bin
	
all: rom.bin

clean:
	rm -f *.bin
		
