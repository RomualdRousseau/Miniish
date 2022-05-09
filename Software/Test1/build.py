from PIL import Image

image = Image.open("data/cow.png")
pixels = image.load()

out_file = open("cow.bin", "wb")

for y in range(128):
    for x in range(128):
        i = pixels[x, y] & 0xF
        if x % 2 == 0:
            acc = pixels[x, y] << 4
        else:
            acc = acc | pixels[x, y]
            out_file.write(b'%c' % acc)
