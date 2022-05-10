from PIL import Image

image = Image.open("data/cow.png")
pixels = image.load()

out_file = open("cow.bin", "wb")

for y in range(128):
    for x in range(128):
        pixel = pixels[x, y]
        if x % 2 == 0:
            acc = pixel << 4
        else:
            acc = acc | pixel
            out_file.write(b'%c' % acc)
