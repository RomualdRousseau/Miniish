ARDUINO_TOOLS = /home/romuald/.arduino15/packages/arduino/tools
AVRGCC_BIN = $(ARDUINO_TOOLS)/avr-gcc/7.3.0-atmel3.6.1-arduino7/bin
AVRDUDE_BIN = $(ARDUINO_TOOLS)/avrdude/6.3.0-arduino17/bin
AVRDUDE_ETC = $(ARDUINO_TOOLS)/avrdude/6.3.0-arduino17/etc

MCU = atmega328p
F_CPU = 16000000UL
CFLAGS = -Os -mmcu=$(MCU) -DF_CPU=$(F_CPU)

CC = $(AVRGCC_BIN)/avr-gcc
OBJCOPY = $(AVRGCC_BIN)/avr-objcopy
AVRDUDE = $(AVRDUDE_BIN)/avrdude
PROGRAMMER = -C /$(AVRDUDE_ETC)/avrdude.conf -c arduino -p $(MCU) -P /dev/ttyACM0 -b 115200 -D

INCLUDES = \
	src/include/common.h \
	src/include/clock.h \
	src/include/sipo.h \
	src/include/piso.h \
	src/include/intr.h

OBJS = \
	src/clock.o \
	src/sipo.o \
	src/piso.o \
	src/intr.o \
	src/main.o

.PHONY: compile upload clean

all: compile

compile: bin/main.hex

upload: bin/main.hex
	$(AVRDUDE) $(PROGRAMMER) -U flash:w:$<:i

clean:
	rm -f $(OBJS) bin/main.elf bin/main.hex

bin/main.hex: bin/main.elf
	$(OBJCOPY) -O ihex -R .eeprom $< $@

bin/main.elf: $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS)

src/%.o: src/%.c $(INCLUDES)
	$(CC) $(CFLAGS) -Isrc/include -c -o $@ $<