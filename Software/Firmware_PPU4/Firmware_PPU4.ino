/*
    Welcome to PPU v1.0 firmware

    To upload this firmware, select the following board:
    Board: "ATMEGA 1284P"
    Clock: "20MHz"
    Bootloader: "Empty"
*/

#include "globals.h"
#include "vram.h"
#include "dma.h"
#include "ppu.h"

void setup() {

  // Configure the Control Port

  DDRB = ~(PIN_VBLANK | PIN_RW | PIN_ENABLE | PIN_CLOCK);
  PORTB = PIN_RROM | PIN_WRAM | PIN_NMI;

  // Configure the Address and Data Bus

  DDRA = 0b00000000;
  DDRD = 0b00000000;
  DDRC = 0b00000000;

  cli();

  // Initialize HAL

  VRAM.init();
  DMA.init();
  PPU.init();

  VRAM.build_first_block();

  // Wait VGA to stabilize

  delay(200);

  // Clear and stop all timers

  TCCR0A = 0;
  TCCR0B = 0;
  TCCR1A = 0;
  TCCR1B = 0;
  TCCR2A = 0;
  TCCR2B = 0;

  // Configure PIN_VBLANK interrupt on INT2 (PB2)

  EICRA |= (1 << ISC21) | (1 << ISC20); // Rising level
  EIMSK |= (1 << INT2);

  sei();
}

ISR (INT2_vect)
{
  if (vram_block == (SCREEN_ROWS / TILE_PER_BLOCK)) {
    if (status & STATUS_DMA) {

      // Do all queued DMA transfers

      DMA.transfer();
    } else {

      // Receive and process PPU instructions

      PPU.do_instructions();

      // Generate first block if no DMA request in the queue

      if (!(status & STATUS_DMA)) {
        VRAM.build_first_block();
      }
    }
  } else {
    if (!(status & STATUS_CLEAR)) {
      
      // Zeroed VRAM
    
      VRAM.clear();
      
    } else {
      
      // Write to VRAM
    
      VRAM.write();
    }

    // Prepare next block

    VRAM.build_next_block();
  }
}

void loop() {
  // Do nothing
}
