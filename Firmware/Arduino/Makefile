###############################################################################
# Project Directories

SRC_DIR							= src
BIN_DIR							= bin
LIB_DIR							= lib

BINARY = $(BIN_DIR)/main

###############################################################################
# AVR Directories

ARDUINO_TOOLS_DIR = /home/romuald/.arduino15/packages/arduino/tools
AVRGCC_BIN_DIR = $(ARDUINO_TOOLS_DIR)/avr-gcc/7.3.0-atmel3.6.1-arduino7/bin
AVRDUDE_BIN_DIR = $(ARDUINO_TOOLS_DIR)/avrdude/6.3.0-arduino17/bin
AVRDUDE_ETC_DIR = $(ARDUINO_TOOLS_DIR)/avrdude/6.3.0-arduino17/etc

###############################################################################
# Basic Device Setup

MCU = atmega328p
F_CPU = 16000000UL

###############################################################################
# Executables

CC = $(AVRGCC_BIN_DIR)/avr-gcc
OBJCOPY = $(AVRGCC_BIN_DIR)/avr-objcopy
AVRDUDE = $(AVRDUDE_BIN_DIR)/avrdude
PROGRAMMER = -C /$(AVRDUDE_ETC_DIR)/avrdude.conf -c arduino -p $(MCU) -P /dev/ttyACM1 -b 115200 -D

###############################################################################
# C Flags

CFLAGS = -Os -mmcu=$(MCU) -DF_CPU=$(F_CPU) -Wno-misspelled-isr

###############################################################################
# Source Files

INCLUDES = \
    -I$(LIB_DIR) \
    -I$(SRC_DIR)

LIBS = \
    $(LIB_DIR)/spi.o \
    $(LIB_DIR)/uart.o \
    $(LIB_DIR)/nrf24.o \

OBJS = \
	$(SRC_DIR)/clock.o \
	$(SRC_DIR)/sipo.o \
	$(SRC_DIR)/piso.o \
	$(SRC_DIR)/intr.o \
    $(SRC_DIR)/util.o \
    $(SRC_DIR)/proto.o \
	$(SRC_DIR)/main.o

###############################################################################
###############################################################################
###############################################################################

HELP_HEADER = "Arduino Makefile"

help: ## Show this help
	@echo
	@echo -e "\033[1;94m${HELP_HEADER}\033[0m"
	@echo
	@echo -e "\033[1;93mAvailable targets:\033[0m"
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'
	@echo

all: $(BIN_DIR) $(BINARY).hex ## Compile this package

flash: $(BIN_DIR) $(BINARY).hex ## Flash this package to the Arduino board
	$(AVRDUDE) $(PROGRAMMER) -U flash:w:$(BINARY).hex:i

clean: ## Clean this package
	rm -f $(LIBS) $(OBJS) $(BINARY).elf $(BINARY).hex
	rm -fd $(BIN_DIR)

###############################################################################
# Rules

%.hex: %.elf
	$(OBJCOPY) -O ihex -R .eeprom $< $@

%.elf: $(LIBS) $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(LIBS) $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) $(INCLUDES) -c -o $@ $<

$(BIN_DIR):
	mkdir $@

.PHONY: help init all flash clean