from PIL import Image

image = Image.open("data/cow2.png")
pixels = image.load()

out_file = open("rom.bin", "wb")
		
for y in range(128):
	for x in range(256):
		if x < 200 and y >= 22:
			out_file.write(chr(pixels[x, y - 22]))
		else:
			out_file.write(chr(0))

