SOURCE_DIR  = ./src
INCLUDE_DIR = ./include
LIB_DIR     = ./lib
CFG_LIB     = ./cfg

VASM = vasm6502_oldstyle -c02 -dotdir -autoexp -Fvobj -esc -I$(INCLUDE_DIR)

INCLUDES = \
	$(INCLUDE_DIR)/miniish.inc \
	$(INCLUDE_DIR)/conio.inc

LIBS = \
	$(LIB_DIR)/startup.o \
	$(LIB_DIR)/vectors.o \
	$(LIB_DIR)/sys.o  \
	$(LIB_DIR)/lcd.o \
	$(LIB_DIR)/uart.o \
	$(LIB_DIR)/conio.o

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
	rm -f $(LIB_DIR)/*

$(LIB_DIR)/%.o: $(SOURCE_DIR)/%.asm $(INCLUDES)
	$(VASM) -o $@ $<

