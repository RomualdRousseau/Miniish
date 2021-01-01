from ppu import add_palettes, add_patterns, add_bytes, fill_spaces

count = 0;

out_file = open("rom.bin", "wb")

print "0x{:04x}".format(count)
count += add_palettes([
	'#40c040', '#c0c0c0', '#c040c0', '#8040c0',
	'#000000', '#000000', '#000000', '#000000',
	'#000000', '#000000', '#000000', '#000000',
	'#000000', '#000000', '#000000', '#000000',
	'#40c040', '#c0c0c0', '#404040', '#000000',
	'#000000', '#000000', '#000000', '#000000',
	'#000000', '#000000', '#000000', '#000000',
	'#000000', '#000000', '#000000', '#000000'
], out_file)

print "0x{:04x}".format(count)
count += add_patterns("cow.png", out_file)

print "0x{:04x}".format(count)
count += add_bytes([
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x0E, 0x0D, 0x0D, 0x0D, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x0A, 0x00, 0x00, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x0A, 0x00, 0x00, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x08, 0x00, 0x00, 0x0B, 0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x0E, 0x00, 0x00, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0E, 0x0F, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x0A, 0x00, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x09, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x0A, 0x00, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x08, 0x0B, 0x0B, 0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
], out_file)

fill_spaces(count, out_file)

