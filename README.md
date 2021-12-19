# Miniish - Homebrew 6502 Computer

The goal of this project is to build a 8bit game console based on 6502 CPU.
The entire project is strongly inspired by the work and videos of Ben Eater, but
also Javidx9 and his emulator.

## Mother Board

It is basically the same hardware design presented by Ben Eater. I just cleaned
up the adress control logic to have as mush of the 32K RAM available.

The address plan is:

0000 --------------------------------

//   RAM

8000 --------------------------------

//   LO ROM

D000 --------------------------------

//   IRQ Status

D100 --------------------------------

//   PICTURE PROCESSING UNIT (PORT1B)

D200 --------------------------------

//   AUDIO PROCESSING UNIT (PORT2B)

D300 --------------------------------

//   I/O

D400 --------------------------------

//   Reserved

E000 --------------------------------

//   HI ROM

FFFF --------------------------------

## Picture Processing Unit (PPU)

### VGA Card

The card is again inspired by Ben Eater "worst video card" But I replaced the
counter logic by a ATMEGA328P (First I built using an arduino uno). The micro
controller generates the HSYNC, VSYNC and one address counter. The address counter
is connected to a SRAM which generates the pixels send to the VGA monitor.

The overall specs of the VGA card is 64 colors with a 160x100 display area using
the VGA 640x480 60Hz standard.

The VGA card is interfaced to the motherboard through a sprite based unit. The
video ram is not mapped to the computer ram but instead, the CPU sends instructions
to a sprite generator very similar to the Nintendo PPU (greatly based on Javidx9
explanations). The Sprite generator is using a ATMEGA1284P clocked at 20MHz.

The overall spec of the sprite generator is:

* 2 nametables for the background composed of 16 * 12 tiles. Each tile is 8x8
pixels. Scrolling vertical and horizontal modes are supported.

* 2 attributes tables to set the palette of each tiles of the background.

* 8 palettes of 4 colors each to asign to the background or the sprites

* 32 sprites with tansparency support. Each sprite is also a tile of 8x8 pixels.

* Collision support (to come)

Because of the limited power of the micro controller. A full image is generated
every 4 VGA frames. It means with a 60Hz frame rate, the image is generated at a rate of 15Hz.

The sprite generator generates the picture in a interlaced mode described as follow:

![PPU signals](https://github.com/RomualdRousseau/Miniish/blob/main/Material/PPU%20signals.png)

Main parts of the code are in assembler to provide greater control of the timings.

## Audio Procesing Unit (APU)

4 channels; 3 square + 1 noise


