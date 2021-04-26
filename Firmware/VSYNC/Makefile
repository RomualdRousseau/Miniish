.PHONY: all clean

default: all

vsync.jed: vsync.pld
	galasm -c -f -p -s vsync.pld
	
burn: vsync.jed
	minipro -P -p ATF16V8B -w vsync.jed
	
all: vsync.jed

clean:
	rm -f *.jed
		
