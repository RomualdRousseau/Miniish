from PIL import Image

base_64colors = {
	'#000000': 0,
	'#000040': 1,
	'#000080': 2,
	'#0000c0': 3,
	'#004000': 4,
	'#004040': 5,
	'#004080': 6,
	'#0040c0': 7,
	'#008000': 8,
	'#008040': 9,
	'#008080': 10,
	'#0080c0': 11,
	'#00c000': 12,
	'#00c040': 13,
	'#00c080': 14,
	'#00c0c0': 15,
	'#400000': 16,
	'#400040': 17,
	'#400080': 18,
	'#4000c0': 19,
	'#404000': 20,
	'#404040': 21,
	'#404080': 22,
	'#4040c0': 23,
	'#408000': 24,
	'#408040': 25,
	'#408080': 26,
	'#4080c0': 27,
	'#40c000': 28,
	'#40c040': 29,
	'#40c080': 30,
	'#40c0c0': 31,
	'#800000': 32,
	'#800040': 33,
	'#800080': 34,
	'#8000c0': 35,
	'#804000': 36,
	'#804040': 37,
	'#804080': 38,
	'#8040c0': 39,
	'#808000': 40,
	'#808040': 41,
	'#808080': 42,
	'#8080c0': 43,
	'#80c000': 44,
	'#80c040': 45,
	'#80c080': 46,
	'#80c0c0': 47,
	'#c00000': 48,
	'#c00040': 49,
	'#c00080': 50,
	'#c000c0': 51,
	'#c04000': 52,
	'#c04040': 53,
	'#c04080': 54,
	'#c040c0': 55,
	'#c08000': 56,
	'#c08040': 57,
	'#c08080': 58,
	'#c080c0': 59,
	'#c0c000': 60,
	'#c0c040': 61,
	'#c0c080': 62,
	'#c0c0c0': 63
}

def add_palettes(palettes, out_file):
	for palette in palettes:
		out_file.write(chr(base_64colors[palette]))
	return 32

def add_patterns(patterns, out_file):
	image = Image.open(patterns)
	pixels = image.load()
	for sy in range(8):
		for y in range(8):
			for x in range(8):
				acc = 0
				for sx in range(8):
					p = pixels[x * 8 + sx, y * 8 + sy]
					if p & 0b01 == 0b01:
						acc = (acc << 1) + 1
					else:
						acc = acc << 1
				out_file.write(chr(acc))
	for sy in range(8):
		for y in range(8):
			for x in range(8):
				acc = 0
				for sx in range(8):
					p = pixels[x * 8 + sx, y * 8 + sy]
					if p & 0b10 == 0b10:
						acc = (acc << 1) + 1
					else:
						acc = acc << 1
				out_file.write(chr(acc))
	return 1024

def add_bytes(bytes, out_file):
	for byte in bytes:
		out_file.write(chr(byte))
	return len(bytes)
	
def fill_spaces(count, out_file):
	for i in range(32768 - count):
		out_file.write(chr(0))
	
				
