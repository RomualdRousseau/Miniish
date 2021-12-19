.PHONY: all clean

default: all

NorthBridge.jed: NorthBridge.pld
	echo "Compile with WinCUPL"
	
burn: NorthBridge.jed
	minipro -P -p "ATF22V10C(UES)" -w NorthBridge.jed
	
all: NorthBridge.jed

clean:
	rm -f *.jed
		
