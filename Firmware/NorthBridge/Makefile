.PHONY: all clean

default: all

pla.jed: NorthBridge.pld
	galasm -c -f -p -s NorthBridge.pld
	
burn: NorthBridge.jed
	minipro -P -p ATF16V8B -w NorthBridge.jed
	
all: NorthBridge.jed

clean:
	rm -f *.jed
		
