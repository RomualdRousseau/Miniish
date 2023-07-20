SOURCE_DIR  = ./src
INCLUDE_DIR = ./include
LIB_DIR     = ./lib
CFG_LIB     = ./cfg

VASM = vasm6502_oldstyle -c02 -dotdir -Fvobj -esc -ldots -I$(INCLUDE_DIR)

INCLUDES = \
	$(INCLUDE_DIR)/miniish.inc \
	$(INCLUDE_DIR)/conio.inc

LIBS = \
	$(LIB_DIR)/runtime/rst_func.o \
	$(LIB_DIR)/runtime/irq_func.o \
	$(LIB_DIR)/runtime/call_ptr.o \
	$(LIB_DIR)/runtime/delay.o \
	$(LIB_DIR)/runtime/memset.o \
	$(LIB_DIR)/runtime/vectors.o \
	$(LIB_DIR)/runtime/devices.o \
	$(LIB_DIR)/lcd/init.o \
	$(LIB_DIR)/lcd/clear.o \
	$(LIB_DIR)/lcd/home.o \
	$(LIB_DIR)/lcd/put_char.o \
	$(LIB_DIR)/lcd/send_cmd.o \
	$(LIB_DIR)/lcd/wait.o \
	$(LIB_DIR)/uart/init.o \
	$(LIB_DIR)/uart/put_char.o \
	$(LIB_DIR)/uart/get_char.o \
	$(LIB_DIR)/uart/wait_rx.o \
	$(LIB_DIR)/uart/wait_tx.o \
	$(LIB_DIR)/conio/print.o \
	$(LIB_DIR)/conio/print_byte.o

HELP_HEADER = "Build BIOS"

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@echo
	@echo -e "\033[1;94m${HELP_HEADER}\033[0m"
	@echo
	@echo -e "\033[1;93mAvailable targets:\033[0m"
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'
	@echo

.PHONY: build
build: $(LIBS) ## Build this package

.PHONY: clean
clean: ## Clean this package
	rm -rf $(LIB_DIR)/*

$(LIB_DIR)/%.o: $(SOURCE_DIR)/%.asm $(INCLUDES)
	mkdir -p $(shell dirname $@)
	$(VASM) -o $@ $<

