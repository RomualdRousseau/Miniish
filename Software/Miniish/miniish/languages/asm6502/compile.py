import os
import subprocess

from miniish.pyco import *

def compile(args, out):
    for i, text in enumerate(PYCO.sources):
        if len(text) > 0:
            line = text[0]
            file_name = f"buffer{i}.i"
            if i == 0:
                file_name = "main.s"
            elif line[0] == ';':
                file_name = line[1:].strip()
            with open("work/" + file_name, "w") as writer:
                for line in text:
                    writer.write(line + "\n")
    
    with open("work/sprites.dat", "wb") as writer:
        for y in range(16):
            for x in range(16):
                for sy in range(8):
                    for sx in range(8):
                        pixel = pyco.sget((x * 8 + sx, y * 8 + sy))
                        if sx % 2 == 0:
                            acc = pixel << 4
                        else:
                            acc = acc | pixel
                            writer.write(b'%c' % acc)
    
    with open("work/map.dat", "wb") as writer:
        for i in range(32):
            for j in range(32):
                writer.write(b'%c' % pyco.mget((j, i)))
   
    with open("work/sound.dat", "wb") as writer:
        for i in range(16):
            s = PYCO.sounds[i]
            for j in range(8):
                p, w, v, e, _ = s[j]
                if v > 0:
                    pack = (w << 5) | (e << 2) | ((v >> 1) << 0)
                    writer.write(b'%c' % (pack & 0xFF))
                    writer.write(b'%c' % (p & 0xFF))
                else:
                    writer.write(b'%c' % (0xFF))
                    writer.write(b'%c' % (0xFF))
 
    with open("work/music.dat", "wb") as writer:
        for i in range(32):
                m = PYCO.music[i]
                flag = -1
                for j in range(3):
                    if m[j] >= 0:
                        flag = 0
                writer.write(b'%c' % (flag & 0xFF))
                for j in range(3):
                    writer.write(b'%c' % (m[j] & 0xFF))

    result = subprocess.run(["make", "-C", "work", "burn"], capture_output=True, text = True)
    if result.returncode == 0:
        out.print(result.stdout.lower())
    else:
        out.print(result.stderr.lower())

    return None
