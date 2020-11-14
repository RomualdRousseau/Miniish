#include <avr/pgmspace.h>
#include "data.h"

#define VBLANK    (1 << PORTB2)
#define WRITE_RAM (1 << PORTB7)

struct gmem_t
{
  // bank 0 and 1
  byte nametables[2][12][20];
  byte reserved[32];
  // bank 2 and 3
  byte attributes[2][12][20];
  byte palettes[16][2];
  // Bank 4
  byte patterns[32][8];
};
struct gmem_t gmem;

volatile byte currx = 0;
volatile byte curry = 0;

void setup() {

  // Configure the Control Port

  DDRB  = ~VBLANK;
  PORTB = WRITE_RAM;

  // Load graphic data

  memset((void*) &gmem, 0, 5 * 256);
  //memcpy_P((void*) gmem.nametables, nametable, 12 * 20);
  //memcpy_P((void*) gmem.attributes, attribute, 12 * 20);
  memcpy_P((void*) gmem.palettes, palettes, 8 * 2);
  memcpy_P((void*) gmem.patterns, patterns, 16 * 8);

  gmem.nametables[0][0][0] = 1;

  // Wait other parts of the circuit to stabilize
  
  delay(100);

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

  // Sync to a new vertical blank
  
  while(PINB & VBLANK) {
    asm volatile("nop\n");
  }
  while(!(PINB & VBLANK)) {
    asm volatile("nop\n");
  }

  // Configure VBLANK interrupt on INT2 (PB2)

  EICRA |= (1 << ISC21) | (1 << ISC20); // Rising level
  EIMSK |= (1 << INT2);
  
  sei();
}

void loop() {
  byte* p = (byte*) gmem.nametables;
  *(p + 100) = 1;
//  static int spr_x = 0;
//  static int spr_y = 0;
//  static int spr_dx = 1;
//  static int spr_dy = 1;
//
//  while(PINB & VBLANK) {
//    asm volatile("nop\n");
//  }
//  
//  gmem.nametables[0][spr_y][spr_x] = 1;
//  gmem.nametables[0][spr_y + 1][spr_x + 1] = 1;
//  
//  spr_x++;
//  spr_y++;
//  if (spr_y <= 0 || spr_y >= 11) {
//    spr_dy=-spr_dy;
//  }
//  if (spr_x <= 0 || spr_x >= 19) {
//    spr_dx=-spr_dx;
//  }
//  delay(1000);
}


ISR (INT2_vect)
{
  // Acquire the Address and Data Bus
  
  DDRA = 0b11111111;
  DDRD = 0b11111111;
  DDRC = 0b11111111;

  // Write pixels

  asm volatile(
    "begin_scan_line:\n"
    
    // Locate pattern in nametable in Y = gmem[0x0000 + (y >> 3) * 20 + (x >> 3)]

    "    movw y, %[gmem]\n"
    
    "    mov __tmp_reg__, %[y]\n"
    "    lsr __tmp_reg__\n"
    "    lsr __tmp_reg__\n"
    "    lsr __tmp_reg__\n"
    "    ldi r20, 20\n"
    "    mul __tmp_reg__, r20\n"
    "    add r28, __tmp_reg__\n"
    "    adc r29, __zero_reg__\n"
    "    clr __zero_reg__\n"

    "    mov __tmp_reg__, %[x]\n"
    "    lsr __tmp_reg__\n"
    "    lsr __tmp_reg__\n"
    "    lsr __tmp_reg__\n"
    "    add r28, __tmp_reg__\n"
    "    adc r29, __zero_reg__\n"

    // Locate sprite in patterns in X = gmem[0x0400 + (y & 7)]

    "    movw x, %[gmem]\n"

    "    mov r20, %[y]\n"
    "    andi r20, 7\n"
    "    add r26, r20\n"
    "    ldi r20, 4\n"
    "    adc r27, r20\n"

    // Output y coordinate
    
    "    out %[porta], %[y]\n"

    "loop_scan_line:\n"

    // Load attribute r16 = Y[0x0200] * 2 + 224
    
    "    movw z, y\n"
    "    ldi r20, 2\n"
    "    add r31, r20\n"
    "    ld r16, z\n"
    "    lsl r16\n"
    "    ldi r20, 224\n"
    "    add r16, r20\n"

    // Load sprite in r15 = X[(Y++)[0] * 8]
    
    "    movw z, x\n"
    "    ld r15, y+\n"
    "    ldi r20, 8\n"
    "    mul r15, r20\n"
    "    add r30, __tmp_reg__\n"
    "    adc r31, __zero_reg__\n"
    "    ld r15, z\n"
    "    clr __zero_reg__\n"

    // Draw sprite

    "draw_sprite:\n"
    
    // Load color in palette in gmem[0x0300 + r16 + (r15 & 1)]

    "    mov r20, r15\n"
    "    andi r20, 1\n"
    "    add r20, r16\n"
    "    movw z, %[gmem]\n"
    "    add r30, r20\n"
    "    ldi r20, 3\n"
    "    adc r31, r20\n"
    "    ld r20, z\n"

    // Output x coordinate

    "    out %[portd], %[x]\n"

    // Output pixel
    
    "    out %[portc], r20\n"
    "    cbi %[portb], %[wram]\n"
    "    sbi %[portb], %[wram]\n"

    // Check if vblank is cleared, continue scan line otherwise
    
    "    sbis %[pinb], %[vblank]\n"
    "    rjmp end_frame\n"

    // Next pixel

    "    lsr r15\n"
    "    inc %[x]\n"

    // Check if end of sprite, continue draw sprite otherwise
    
    "    mov r20, %[x]\n"
    "    andi r20, 7\n"
    "    brne draw_sprite\n"

    // Check if end of line, continue scan line otherwise

    "    cpi %[x], 160\n"
    "    breq end_scan_line\n"
    "    rjmp loop_scan_line\n"
    
    "end_scan_line:\n"
    
    // Output a black pixel for end of line
    
    "    out %[portc], __zero_reg__\n"
    "    out %[portd], %[x]\n"
    "    cbi %[portb], %[wram]\n"
    "    sbi %[portb], %[wram]\n"

    // Go to the next scan line
    
    "    clr %[x]\n"
    "    inc %[y]\n"
    "    cpi %[y], 96\n"
    "    breq end_frame\n"

    // Check if vblank is cleared, continue scan line otherwise

    "    sbic %[pinb], %[vblank]\n"
    "    rjmp begin_scan_line\n"

    "end_frame:\n"
    "    mov %[xr], %[x]\n"
    "    mov %[yr], %[y]\n"
      :[xr] "=r" (currx),
       [yr] "=r" (curry)
      :[porta] "I" (_SFR_IO_ADDR(PORTA)),
       [portb] "I" (_SFR_IO_ADDR(PORTB)),
       [portc] "I" (_SFR_IO_ADDR(PORTC)),
       [portd] "I" (_SFR_IO_ADDR(PORTD)),
       [pinb] "I" (_SFR_IO_ADDR(PINB)),
       [wram] "i" (PINB7),
       [vblank] "i" (PINB2),
       [x] "a" (currx),
       [y] "a" (curry),
       [gmem] "l" (gmem.nametables)
      : "r15", "r16", "r20", "memory"
  );

  // Release the Address and Data Bus

  DDRA = 0b00000000;
  DDRD = 0b00000000;
  DDRC = 0b00000000;

  // Prepare next frame

  if(curry >= 96) {
    currx = 0;
    curry = 0;
  }
}
