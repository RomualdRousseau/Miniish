.PHONY: burn all clean

default: all

cow.bin: data/cow.png
	python build.py

rom.bin: include/*.i cow.bin rom.s
	vasm6502_oldstyle -c02 -Fbin -dotdir -o rom.bin rom.s

burn: rom.bin
	minipro -p AT28C256 -w rom.bin
	
all: rom.bin

clean:
	rm -f *.bin
		
