.PHONY: burn all clean

default: all

main.s: *.i *.dat

rom.bin: main.s
	vasm6502_oldstyle -c02 -Fbin -dotdir -o rom.bin main.s

burn: rom.bin
	minipro -p AT28C256 -w rom.bin
	
all: rom.bin

clean:
	rm -f *.bin
