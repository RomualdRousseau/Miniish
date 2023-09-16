BUILD_DIR = $(MINIISH_ROOT)/hardware/asm6502
INCLUDE_DIR = $(BUILD_DIR)/include
LIB_DIR = $(BUILD_DIR)/lib

VASM = vasm6502_oldstyle -c02 -dotdir -Fvobj -autoexp -quiet -I$(INCLUDE_DIR)
LINK = vlink -brawbin1

.PHONY: verify upload build clean

default: clean verify

verify: clean build

upload: clean build
	cp main.bin $(MINIISH_ROOT)/target/rom.bin

build: main.bin

clean:
	rm -f *.o
	rm -f *.bin
	
%.o: %.s
	$(VASM) -o $@ $<

%.bin: %.o
	$(LINK) -o $@ $<
