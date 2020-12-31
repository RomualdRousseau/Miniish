#include "globals.h"
#include "utils.h"
#include "events.h"

void setup() {

  // Configure the Control Port

  DDRB = ~(PIN_VBLANK | PIN_RW | PIN_ENABLE | PIN_CLOCK);
  PORTB = PIN_RROM | PIN_WRAM | PIN_NMI;

  // Configure the Address and Data Bus

  DDRA = 0b00000000;
  DDRD = 0b00000000;
  DDRC = 0b00000000;

  // Load and prepare data
 
  load_data_from_eeprom();
  
  build_next_block();
  
  cli();

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

  status = STATUS_DMA;
}

ISR (INT2_vect)
{
  if (vram_block == 3) {
    if (status & STATUS_DMA) {

      // Acquire the Address and Data Bus

      DDRA = 0b11111111;
      DDRD = 0b11111111;

      // Load data from rom
      
      load_data_from_rom();

      // Release the Address and Data Bus

      DDRA = 0b00000000;
      DDRD = 0b00000000;

      // Reset status

      status &= ~STATUS_DMA;
    } else {

      // Notify the CPU to start read commands

      status |= STATUS_NMI;
      PORTB &= ~PIN_NMI;
  
      // Read commands
      
      read_commands();

      // Notify the CPU to stop read commands

      PORTB |= PIN_NMI;
      status &= ~STATUS_NMI;

      if (!(status & STATUS_DMA)) {
  
        // Process the commands
        
        process_commands();
  
        // Prepare first block
        
        vram_block = 0;
        build_next_block();
      }
    }
    return;
  }
  
  // Acquire the Address and Data Bus

  DDRA = 0b11111111;
  DDRD = 0b11111111;
  DDRC = 0b11111111;
  
  // Write pixels

  asm volatile(

    "    movw z, %[vram]\n"

    "start_scan_line:\n"

    // Output y coordinate
    
    "    out %[porta], %[y]\n"

    "loop_scan_line:\n"

    // Output x coordinate

    "    out %[portd], %[x]\n"
    
    // Output pixel
    
    "    ld __tmp_reg__, z+\n"   
    "    out %[portc], __tmp_reg__\n"
    "    cbi %[portb], %[wram]\n"
    "    sbi %[portb], %[wram]\n"
    
    // Next pixel
    
    "    inc %[x]\n"
    
    // Cehck if end of line, continue otherwise

    "    cpi %[x], 160\n"
    "    brne loop_scan_line\n"

    // Output a black pixel at the end of line
    
    "    out %[portd], %[x]\n"
    "    out %[portc], __zero_reg__\n"
    "    cbi %[portb], %[wram]\n"
    "    sbi %[portb], %[wram]\n"

    // Go to the next scan line

    "    clr %[x]\n"
    "    inc %[y]\n"
    "    cp %[y], %[h]\n"
    "    breq end_frame\n"

    "    rjmp start_scan_line\n"

    "end_frame:\n"
      :
      :[porta]  "I" (_SFR_IO_ADDR(PORTA)),
       [portb]  "I" (_SFR_IO_ADDR(PORTB)),
       [portc]  "I" (_SFR_IO_ADDR(PORTC)),
       [portd]  "I" (_SFR_IO_ADDR(PORTD)),
       [pinb]   "I" (_SFR_IO_ADDR(PINB)),
       [x]      "r" (0),
       [y]      "r" (vram_block * BLOCK_SIZE),
       [h]      "r" (vram_block * BLOCK_SIZE + BLOCK_SIZE),
       [vram]   "l" (vram_data),
       [wram]   "i" (PINB1),
       [vblank] "i" (PINB2)
      : "r20"
  );

  // Release the Address and Data Bus

  DDRA = 0b00000000;
  DDRD = 0b00000000;
  DDRC = 0b00000000;
  
  // Prepare next block

  vram_block++;
  if(vram_block < 3) {
    build_next_block();
  }
}

void loop() {
}
