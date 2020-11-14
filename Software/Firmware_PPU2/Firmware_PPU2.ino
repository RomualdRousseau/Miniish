
#define VBLANK    (1 << PORTB2)
#define WRITE_RAM (1 << PORTB7)

volatile byte vram[160 * 96];
volatile byte currx = 0;
volatile byte curry = 0;
volatile boolean vblank = false;

int spr_x = 0;
int spr_y = 0;
int spr_dx = 1;
int spr_dy = 1;

void setup() {

  // Configure the Control Port

  DDRB  = ~VBLANK;
  PORTB = WRITE_RAM;

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
  if (vblank) {
    return; 
  }

  vram[160 * spr_y + spr_x]++;

  spr_x+=spr_dx;
  if (spr_x <= 0 || spr_x >= 159) {
    spr_dx=-spr_dx;
  }
  
  spr_y+=spr_dy;
  if (spr_y <= 0 || spr_y >= 95) {
    spr_dy=-spr_dy;
  }
  
  delay(10);
}


ISR (INT2_vect)
{
  vblank = true;
  
  // Acquire the Address and Data Bus
  
  DDRA = 0b11111111;
  DDRD = 0b11111111;
  DDRC = 0b11111111;

  // Write pixels

  asm volatile(

    "start_scan_line:\n"
    
    // Prepare the stral address for the scan line
    
    "    movw z, %[vram]\n"
   
    "    ldi r20, 160\n"
    "    mul r20, %[y]\n"
    "    add r30, __tmp_reg__\n"
    "    adc r31, __zero_reg__\n"
    "    clr __zero_reg__\n"
    
    "    add r30, %[x]\n"
    "    adc r31, __zero_reg__\n"

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
    
    "    sbis %[pinb], %[vblank]\n"
    "    rjmp end_frame\n"

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
    "    cpi %[y], 96\n"
    "    breq end_frame\n"

    "    rjmp start_scan_line\n"

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
       [x] "r" (currx),
       [y] "r" (curry),
       [vram] "l" (vram),
       [wram] "i" (PINB7),
       [vblank] "i" (PINB2)
      : "r20"
  );

  // Release the Address and Data Bus

  DDRA = 0b00000000;
  DDRD = 0b00000000;
  DDRC = 0b00000000;

  // Prepare next block

  if(curry >= 96) {
    currx = 0;
    curry = 0;
  }

  vblank = false;
}
