.PHONY: all clean

default: all

VASM = vasm6502_oldstyle -c02 -dotdir -autoexp -Fvobj -I../include

%.o: %.s ../include/*.i
	$(VASM) -o $@ $<

all: bootstrap.o

clean:
	rm -f *.o
