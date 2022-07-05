BUILD_DIR = $(MINIISH_ROOT)/build
INCLUDE_DIR = $(BUILD_DIR)/include
LIB_DIR = $(BUILD_DIR)/lib

VASM = vasm6502_oldstyle -c02 -dotdir -Fvobj -autoexp -quiet -I$(INCLUDE_DIR)
LINK = vlink -brawbin1 -T$(LIB_DIR)/bootstrap.lnk $(LIB_DIR)/bootstrap.o
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
	cp main.bin $(MINIISH_ROOT)/rom.bin
	$(BURN) $<
	
%.o: %.s $(INCLUDES) $(DATA)
	$(VASM) -o $@ $<

%.bin: %.o
	$(LINK) -o $@ $<
