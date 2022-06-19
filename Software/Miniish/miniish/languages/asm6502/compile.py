import os
import shutil
import tempfile
import subprocess

from miniish.pyco import *

def build_sources(workdir):
    for i, text in enumerate(PYCO.sources):
        if len(text) > 0:
            line = text[0]
            file_name = f"buffer{i}.i"
            if i == 0:
                file_name = "main.s"
            elif line[0] == ';':
                file_name = line[1:].strip()
            with open(workdir + "/" + file_name, "w") as writer:
                for line in text:
                    writer.write(line + "\n")


def build_sprites(workdir):
    with open(workdir + "/sprites.dat", "wb") as writer:
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
 

def build_flags(workdir):
    with open(workdir + "/flags.dat", "wb") as writer:
        for n in range(256):
            flag = pyco.fget(n)
            writer.write(b'%c' % flag)            


def build_map(workdir):
    with open(workdir + "/map.dat", "wb") as writer:
        for i in range(32):
            for j in range(32):
                writer.write(b'%c' % pyco.mget((j, i)))
     

def build_sound(workdir):
    with open(workdir + "/sound.dat", "wb") as writer:
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
     

def build_music(workdir):
    with open(workdir + "/music.dat", "wb") as writer:
        for i in range(32):
                m = PYCO.music[i]
                flag = -1
                for j in range(3):
                    if m[j] >= 0:
                        flag = 0
                writer.write(b'%c' % (flag & 0xFF))
                for j in range(3):
                    writer.write(b'%c' % (m[j] & 0xFF))


def build_all(workdir, checkonly):
    build_sources(workdir)
    build_sprites(workdir)
    build_flags(workdir)
    build_map(workdir)
    build_sound(workdir)
    build_music(workdir)
    # Prepare project build tool
    shutil.copy("build/Makefile", workdir + "/Makefile")
    my_env = os.environ.copy()
    my_env["MINIISH_ROOT"] = os.getcwd()
    action = "all" if checkonly else "burn"
    return subprocess.run(["make", "-C", workdir, action], env = my_env, capture_output=True, text = True)
    

def compile(args, out, checkonly = False):
    with tempfile.TemporaryDirectory() as workdir:
        result = build_all(workdir, checkonly)
        if result.returncode == 0:
            out.print(result.stdout.lower())
        else:
            out.print(result.stderr.lower())
    return None
