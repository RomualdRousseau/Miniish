INCLUDE_DIR = ../include

VASM = vasm6502_oldstyle -c02 -dotdir -autoexp -Fvobj -I$(INCLUDE_DIR)

INCLUDES = $(wildcard $(INCLUDE_DIR)/*.s)

HELP_HEADER = "Build bootstrap"

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
build: bootstrap.o ## Build this package

.PHONY: clean
clean: ## Clean this package
	rm -f *.o

%.o: %.s $(INCLUDE_DIR)/*.s
	$(VASM) -o $@ $<
