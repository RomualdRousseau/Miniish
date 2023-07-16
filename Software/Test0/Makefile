INCLUDE_DIR = include
LIB_DIR = lib

VASM = vasm6502_oldstyle -c02 -dotdir -Fbin -autoexp -quiet -I$(INCLUDE_DIR)
BURN = minipro -p AT28C256 -w

INCLUDES = $(wildcard ./include/*.s)
DATA = $(wildcard ./data/*.dat)

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

.PHONY: all
all: build burn

.PHONY: clean
clean: ## Clean this package
	rm -f *.o
	rm -f *.bin

build: main.bin ## Build this package

burn: main.bin ## Burn this package
	$(BURN) $<
	
%.bin: %.s $(INCLUDES) $(DATA)
	$(VASM) -o $@ $<
