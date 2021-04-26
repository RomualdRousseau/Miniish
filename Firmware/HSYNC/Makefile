.PHONY: all clean

default: all

hsync.jed: hsync.pld
	galasm -c -f -p -s hsync.pld
	
burn: hsync.jed
	minipro -P -p ATF16V8B -w hsync.jed
	
all: hsync.jed

clean:
	rm -f *.jed
		
