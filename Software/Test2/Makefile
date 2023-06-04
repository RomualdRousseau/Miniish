INCLUDE_DIR = include
LIB_DIR = lib

VASM = vasm6502_oldstyle -c02 -dotdir -Fbin -autoexp -quiet -I$(INCLUDE_DIR)
BURN = minipro -p AT28C256 -w

INCLUDES = $(wildcard ./*.i)
DATA = $(wildcard ./*.dat)

.PHONY: all clean burn

default: all

all: main.bin

clean:
	rm -f *.o
	rm -f *.bin
	
burn: main.bin
	$(BURN) $<
	
%.bin: %.s $(INCLUDES) $(DATA)
	$(VASM) -o $@ $<
