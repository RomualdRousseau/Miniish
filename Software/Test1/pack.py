from PIL import Image

print("Pack data ...")

image = Image.open("data/cow.png")
pixels = image.load()

with open("sprites.bin", "wb") as out_file:
    for y in range(16):
        for x in range(16):
            for sy in range(8):
                for sx in range(8):
                    pixel = pixels[x * 8 + sx, y * 8 + sy]
                    if sx % 2 == 0:
                        acc = pixel << 4
                    else:
                        acc = acc | pixel
                        out_file.write(b'%c' % acc)

with open("map.bin", "wb") as out_file:
    for i in range(32):
        for j in range(32):
            out_file.write(b'%c' % ((i % 16) * 16 + (j % 16)))
