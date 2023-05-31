.PHONY: all clean

default: all

NorthBridge2.jed: NorthBridge2.pld
	echo "Compile with WinCUPL"
	
burn: NorthBridge2.jed
	minipro -P -p "ATF22V10C" -w NorthBridge2.jed
	
all: NorthBridge2.jed

clean:
	rm -f *.jed
		
