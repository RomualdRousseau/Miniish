SOURCE_DIR = ./src
DATA_DIR   = ./data
BIN_DIR    = ./bin

INCLUDE_DIR = ../Bios/include
LIB_DIR     = ../Bios/lib
CFG_LIB     = ../Bios/cfg

INCLUDES = $(wildcard $(INCLUDE_DIR)/*.inc)
LIBS     = $(wildcard $(LIB_DIR)/*.o)
DATA     = $(wildcard $(DATA_DIR)/*.dat)

VASM  = vasm6502_oldstyle -c02 -dotdir -autoexp -Fvobj -esc -I$(INCLUDE_DIR)
VLINK = vlink -brawbin1 -T$(CFG_LIB)/miniish.lnk $(LIBS)
BURN  = minipro -p AT28C256 -w

HELP_HEADER = "Test3 - Test DigitalProtoBoard"

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@echo
	@echo -e "\033[1;94m${HELP_HEADER}\033[0m"
	@echo
	@echo -e "\033[1;93mAvailable targets:\033[0m"
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'
	@echo

.PHONY: clean
clean: ## Clean this package
	rm -f $(BIN_DIR)/*

build: $(BIN_DIR)/main.prg ## Build this package
	
burn: $(BIN_DIR)/main.prg ## Burn this package
	$(BURN) $<

$(BIN_DIR)/%.o: $(SOURCE_DIR)/%.asm $(INCLUDES) $(DATA)
	$(VASM) -o $@ $<

$(BIN_DIR)/%.prg: $(BIN_DIR)/%.o $(LIBS)
	$(VLINK) -o $@ $<
