#!/bin/sh

vasm6502_oldstyle -Fbin -dotdir -o rom.bin rom.s

minipro -p AT28C256 -w rom.bin

