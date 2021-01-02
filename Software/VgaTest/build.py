from PIL import Image

image = Image.open("data/bird.png")
pixels = image.load()

out_file = open("rom.bin", "wb")
for y in range(128):
	for x in range(256):
		try:
			out_file.write(chr(pixels[x, y]))
		except IndexError:
			out_file.write(chr(0))

