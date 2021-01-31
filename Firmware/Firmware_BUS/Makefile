.PHONY: all clean

default: all

pla.jed: pla.pld
	galasm -c -f -p -s pla.pld
	
burn: pla.jed
	minipro -P -p ATF16V8B -w pla.jed
	
all: pla.jed

clean:
	rm -f *.jed
		
