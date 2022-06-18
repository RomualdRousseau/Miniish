.PHONY: burn all clean distclean

default: all

ASM = vasm6502_oldstyle -quiet -c02 -I../include -Fbin -dotdir
BURN = minipro -p AT28C256 -w

%.bin: %.s ../include/*.i *.i *.dat
	$(ASM) -o $@ $< 

burn: main.bin
	$(BURN) $<
	
all: main.bin

clean:
	rm -f *.bin

distclean:
	rm -f *.i
	rm -f *.s
	rm -f *.dat
	rm -f *.bin
