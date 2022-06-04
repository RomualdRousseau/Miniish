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

The card is built using a FPGA and strongly inspired to the NES PPU and the
capability of PICO-8.

The overall specs of the VGA card is 16 colors with a 128x128 display area using
the VGA 640x480 60Hz standard. The 16 colors are the PICO8 palette.

The VGA card is interfaced to the motherboard through a sprite based unit. The
video ram is not mapped to the computer ram but instead, the CPU sends instructions
to a sprite generator very similar to the NES (greatly based on Javidx9
explanations).

The overall spec of the sprite generator is:

* 1 nametables for the background composed of 16 * 16 tiles. Each tile is 8x8
pixels. Scrolling vertical and horizontal modes are supported.

* 256 sprites with tansparency support. Each sprite is also a tile of 8x8 pixels.

* 64 simultaneous sprites on screen and 16 sprites per scanline

* NMI is generated at each vertical blank

## Audio Procesing Unit (APU)

The card is built using a ATMEGA328p at 20Mhz with the library the_synth of Edgar.

The synthetizer has the overall spec: 

* 4 channels at 20KHz

* 4 waveforms: triangle, square, sinus + noise

* 4 envelopes

* modulation

* IRQ0 is generated as the next data frame callback
