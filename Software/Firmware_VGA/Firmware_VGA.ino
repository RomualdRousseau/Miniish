/*
    Welcome to VGA v1.0 firmware

    To upload this firmware, select the following board:
    Board: "ATMEGA 328P"
    Clock: "20MHz"
    Bootloader: "Empty"
*/

#define CONTROL_PORT     PORTB
#define VADDR_PORT       PORTC
#define HADDR_PORT       PORTD

#define VADDR7_PIN       0  // PIN 8  (PB0)
#define CTRL_HSYNC_PIN   1  // PIN 9  (PB1)
#define CTRL_VSYNC_PIN   2  // PIN 10 (PB2)
#define CTRL_HLINE_PIN   3  // PIN 11 (PB3)
#define CTRL_VBLANK_PIN  4  // PIN 12 (PB4)

#define VSYNC_PULSE      27     // 86.4us rather larger than 64us
#define VSYNC_LENGTH     5209   // 16.668ms
#define VSYNC_START_LINE -76

#define HSYNC_PULSE      9      // 3.6us
#define HSYNC_LENGTH     79     // 31.6us

static volatile int vline = 0;

void setup() {
  
  // Initialize pins directions and values
  
  DDRB = 0b00001111;
  DDRC = 0b00000000;
  DDRD = 0b00000000;
  PORTB  = 0;

  cli();

  // Clear and stop all timers

  TCCR0A = 0;
  TCCR0B = 0;

  TCCR1A = 0;
  TCCR1B = 0;
  
  TCCR2A = 0;
  TCCR2B = 0;

  // Setup Anti jitter on TIMER0

  TIMSK0=0;
  OCR0A=0;
  OCR0B=0;
  TCNT0=0;

  // Setup VSYNC pulse on TIMER1

  TCCR1A |= (1 << WGM11) | (1 << WGM10);   // Fast PWM
  TCCR1B |= (1 << WGM13) | (1 << WGM12);
  TIMSK1 |= (1 << OCIE1B) | (1 << OCIE1A); // Enable interrupts
  OCR1A = VSYNC_LENGTH;
  OCR1B = VSYNC_PULSE;

  // Setup HSYNC pulse on TIMER2
  
  TCCR2A |= (1 << WGM21) | (1 << WGM20);   // Fast PWM
  TCCR2B |= (1 << WGM22);
  TIMSK2 |= (1 << OCIE2B) | (1 << OCIE2A); // Enable interrupts
  OCR2A = HSYNC_LENGTH;
  OCR2B = HSYNC_PULSE;
  
  sei();

  // Start all timers

  TCCR0B |= (1 << CS00); // Prescaler 1/1
  TCCR1B |= (1 << CS11) | (1 << CS10); // Prescaler 1/64
  TCCR2B |= (1 << CS21); // Prescaler 1/8
}

// VSync Interrupts

ISR (TIMER1_COMPA_vect)
{ 
  asm volatile("sbi %[portb], %[outp]\n"::[portb] "I" (_SFR_IO_ADDR(CONTROL_PORT)), [outp] "i" (CTRL_VSYNC_PIN):);
}

ISR (TIMER1_COMPB_vect)
{   
  asm volatile("cbi %[portb], %[outp]\n"::[portb] "I" (_SFR_IO_ADDR(CONTROL_PORT)), [outp] "i" (CTRL_VSYNC_PIN):);
  vline = VSYNC_START_LINE;
  TCNT0 = 0;
}

// HSync Interrupts

ISR (TIMER2_COMPA_vect)
{ 
  asm volatile("cbi %[portb], %[outp]\n"::[portb] "I" (_SFR_IO_ADDR(CONTROL_PORT)), [outp] "i" (CTRL_HSYNC_PIN):);
}

ISR (TIMER2_COMPB_vect)
{
  asm volatile("sbi %[portb], %[outp]\n"::[portb] "I" (_SFR_IO_ADDR(CONTROL_PORT)), [outp] "i" (CTRL_HSYNC_PIN):);
  vline++;

  //
  // Back Porch Section
  //
  
  if (((unsigned) vline) >= 389) {
    if (vline == 389) {
      // Disable data outputs
      DDRB = 0b00011110;
      DDRC = 0b00000000;
      DDRD = 0b00000000;
      // Notify VBLANK start
      PORTB |= (1 << CTRL_VBLANK_PIN);
    } else if (vline == -5) {
      // Notify VBLANK stop
      PORTB &= ~(1 << CTRL_VBLANK_PIN);
    } else if (vline == -1) {
      // Enable data outputs
      DDRB = 0b00011111;
      DDRC = 0b00111111;
      DDRD = 0b11111111;
    }
    return;
  }


  // Initialize line address counter 
  
  asm volatile(
    //PORTB = HIGH(vline >> 2);
    "    sbrc %[vline], 6\n"
    "    sbi %[portb], %[outp]\n"
    "    sbrs %[vline], 6\n"
    "    cbi %[portb], %[outp]\n" 
    //PORTC = LOW(vline >> 2);
    "    andi %[vline], 0x3F\n"
    "    out %[portc], %[vline]\n"
    //PORTD = 0;
    "    out %[portd], __zero_reg__\n"
    :
    :[portb] "I" (_SFR_IO_ADDR(CONTROL_PORT)),
     [portc] "I" (_SFR_IO_ADDR(VADDR_PORT)),
     [portd] "I" (_SFR_IO_ADDR(HADDR_PORT)),
     [outp] "i" (VADDR7_PIN),
     [vline] "r" (vline >> 2)
    :"r20"
  );

  // Sync and stabilize signal

  #define DEJITTER_OFFSET 2
  #define DEJITTER_SYNC   -2
  asm volatile(
    "     lds r16, %[timer]\n"
    "     add r16, %[toff]\n"
    "     subi r16, %[tsync]\n"
    "     andi r16, 3\n"
    "     call TLH\n"
    "TLH:\n"
    "     pop r31\n"
    "     pop r30\n"
    "     adiw r30, (LWH-TLH-2)\n"
    "     add r30, r16\n"
    "     ijmp\n"
    "LWH:\n"
    ".rept 8\n"
    "     nop\n"
    ".endr\n"
    :
    : [timer] "i" (&TCNT0),
      [toff] "i" ((uint8_t) DEJITTER_OFFSET),
      [tsync] "i" ((uint8_t) DEJITTER_SYNC)
    : "r30", "r31", "r16", "r17"
  );

  //
  // Visible Section
  //

  // Notify HLINE start

  asm volatile("cbi %[portb], %[outp]\n"::[portb] "I" (_SFR_IO_ADDR(CONTROL_PORT)), [outp] "i" (CTRL_HLINE_PIN):);

  // Output pixels by incrementing the line address counter
  
  asm volatile(
      "    ldi r20, 0\n"
      ".rept 159\n"
      "    inc r20\n"
      "    out %[portd], r20\n"
      "    nop\n"
      ".endr\n"
      :
      :[portd] "I" (_SFR_IO_ADDR(HADDR_PORT))
      :"r20"
    );
    
  // Notify HLINE stop
  
  asm volatile("sbi %[portb], %[outp]\n"::[portb] "I" (_SFR_IO_ADDR(CONTROL_PORT)), [outp] "i" (CTRL_HLINE_PIN):);
  
  //
  // Front Porch Section
  //

  asm volatile(
      ".rept 4\n"
      "    nop\n"
      ".endr\n"
    );
}

void loop() {
  // Do nothing
}
