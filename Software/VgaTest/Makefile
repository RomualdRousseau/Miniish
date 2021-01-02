.PHONY: clean burn

rom.bin: build.py
	python2 build.py

burn: rom.bin
	minipro -p AT28C256 -w rom.bin

clean:
	rm rom.bin
		
