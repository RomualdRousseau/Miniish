#include "pgmutil.h"
#include "data.h"

#define VBLANK    (1 << PORTB2)
#define WRITE_RAM (1 << PORTB1)

#define BLOCK_SIZE  (8 * 4)

struct gmem_t
{
  // bank 0 and 1
  byte nametables[2][12][20];
  byte reserved1[32];
  // bank 2
  byte attributes[2][6][10];
  byte palettes[8][4];
  byte reserved2[104];
  // Bank 3 and 4
  byte patterns[16][32];
};
struct gmem_t gmem;

byte vram_block[160 * BLOCK_SIZE];
byte curr_block = 0;
volatile byte spinlock = 0;

void load_data_from_eeprom() {
  memcpy_P(gmem.nametables, nametable, 2 * 12 * 20);
  memcpy_P(gmem.attributes, attributes, 2 * 6 * 10);
  memcpy_P(gmem.palettes, palettes, 8 * 4);
  memcpy_P_T(gmem.patterns, patterns, 32, 16);
}

void build_new_block() {
  const int b = curr_block * BLOCK_SIZE;
  byte* vram = vram_block;

  for (int y = b; y < b + BLOCK_SIZE; y++) {
    const byte* n_y = gmem.nametables[0][y >> 3];
    const byte* p_y = gmem.patterns[y & 7];
    const byte* a_y = gmem.attributes[0][y >> 4];
   
    for (int x = 0; x < (160 / 8); x++) {
      const byte* p = gmem.palettes[a_y[x >> 1]];
      const byte* s = &p_y[n_y[x]];
      byte s1 = s[0];
      byte s2 = s[8 * 32];
      
      for (int xx = 0; xx < 8; xx++) {
        *(vram++) = p[((s2 & 1) << 1) | (s1 & 1)];
        s1 >>= 1;
        s2 >>= 1;
      }
    }
  }
}

void setup() {

  // Configure the Control Port

  DDRB  = ~VBLANK;
  PORTB = WRITE_RAM;

  load_data_from_eeprom();
  
  build_new_block();

  // Configure the Address and Data Bus

  DDRA = 0b00000000;
  DDRD = 0b00000000;
  DDRC = 0b00000000;

  cli();

  // Clear and stop all timers

  //TCCR0A = 0;
  //TCCR0B = 0;
  TCCR1A = 0;
  TCCR1B = 0;
  TCCR2A = 0;
  TCCR2B = 0;

  // Configure VBLANK interrupt on INT2 (PB2)

  EICRA |= (1 << ISC21) | (1 << ISC20); // Rising level
  EIMSK |= (1 << INT2);
  
  sei();
}

void loop() {
  static int spr_x = 0;
  static int spr_y = 0;
  static int spr_dx = 1;
  static int spr_dy = 1;

  if (!spinlock) {
    return; 
  }

  gmem.nametables[0][spr_y][spr_x] = 0;
  gmem.attributes[0][spr_y >> 1][spr_x >> 1] = 0;

  spr_x+=spr_dx;
  if (spr_x <= 0 || spr_x >= 19) {
    spr_dx=-spr_dx;
  }
  
  spr_y+=spr_dy;
  if (spr_y <= 0 || spr_y >= 11) {
    spr_dy=-spr_dy;
  }

  gmem.nametables[0][spr_y][spr_x] = 1;
  gmem.attributes[0][spr_y >> 1][spr_x >> 1] = 1;

  delay(25);
}

ISR (INT2_vect)
{
  if (spinlock > 0) {
    if (--spinlock > 0) {
      return;
    }
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
    
    // Check if vblank is cleared, continue otherwise
    
//    "    sbis %[pinb], %[vblank]\n"
//    "    rjmp end_frame\n"

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
       [y]      "r" (curr_block * BLOCK_SIZE),
       [h]      "r" (curr_block * BLOCK_SIZE + BLOCK_SIZE),
       [vram]   "l" (vram_block),
       [wram]   "i" (PINB1),
       [vblank] "i" (PINB2)
      : "r20"
  );

  // Release the Address and Data Bus

  DDRA = 0b00000000;
  DDRD = 0b00000000;
  DDRC = 0b00000000;

  // Prepare next block

  curr_block++;
  if(curr_block == 3) {
    curr_block = 0;
    spinlock = 2;
  }

  build_new_block();
}
