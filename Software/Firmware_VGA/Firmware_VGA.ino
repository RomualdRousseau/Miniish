#define CONTROL_PORT     PORTB
#define VADDR_PORT       PORTC
#define HADDR_PORT       PORTD

#define VADDR7_PIN       0  // PIN 8  (PB0)
#define CTRL_HSYNC_PIN   1  // PIN 9  (PB1)
#define CTRL_VSYNC_PIN   2  // PIN 10 (PB2)
#define CTRL_HLINE_PIN   3  // PIN 11 (PB3)
#define CTRL_VBLANK_PIN  4  // PIN 12 (PB4)

#define VSYNC_PULSE      127   // 64us
#define VSYNC_LENGTH     33326 // 16.666ms
#define VSYNC_START_LINE -80

#define HSYNC_PULSE      6    // 3.8us
#define HSYNC_START_LINE 15   // 6.5us
#define HSYNC_LENGTH     62   // 31.7us

static volatile int vline = 0;

void setup() {
  cli();

  // Setup outputs
  
  DDRB = 0b00001111;
  DDRC = 0b00000000;
  DDRD = 0b00000000;
  PORTB  = 0;

  // Clear and stop all timers

  TCCR0A = 0;
  TCCR0B = 0;

  TCCR1A = 0;
  TCCR1B = 0;
  
  TCCR2A = 0;
  TCCR2B = 0;

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

  // Start all timers with a prescaler of 1/8

  TCCR1B |= (1 << CS11);
  TCCR2B |= (1 << CS21);
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
  
  if (((unsigned) vline) >= 384) {
    if (vline == 384) {
      // Disable data outputs
      DDRB = 0b00011110;
      DDRC = 0b00000000;
      DDRD = 0b00000000;
      // Notify VBLANK start
      PORTB |= (1 << CTRL_VBLANK_PIN);
    } else if (vline == -6) {
      // Enable data outputs
      DDRB = 0b00011111;
      DDRC = 0b00111111;
      DDRD = 0b11111111;
      // Notify VBLANK stop
      PORTB &= ~(1 << CTRL_VBLANK_PIN);
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
  asm volatile(
    "    nop\n"
    "    nop\n"
    "    nop\n"
    "    lds r20, %[tcnt2]\n"
    "    subi r20, %[tsync]\n"
    "    brpl nojitter\n"
    "    nop\n"
    "    nop\n"
    "nojitter:"
    :
    :[tcnt2] "i" (&TCNT2),
     [tsync] "i" (HSYNC_START_LINE)
    :"r20"
   );

  //
  // Visible Section
  //

  // Notify HLINE start
  asm volatile("cbi %[portb], %[outp]\n"::[portb] "I" (_SFR_IO_ADDR(CONTROL_PORT)), [outp] "i" (CTRL_HLINE_PIN):);

  // Output pixels by incrementing the line address counter
  asm volatile(
      "    ldi r20, 1\n"
      ".rept 10\n"
      "    out %[portd], r20\n"
      "    inc r20\n"
      "    out %[portd], r20\n"
      "    nop\n"
      "    inc r20\n"
      "    out %[portd], r20\n"
      "    inc r20\n"
      "    out %[portd], r20\n"
      "    inc r20\n"
      "    out %[portd], r20\n"
      "    inc r20\n"
      "    nop\n"
      "    out %[portd], r20\n"
      "    inc r20\n"
      "    out %[portd], r20\n"
      "    inc r20\n"
      "    out %[portd], r20\n"
      "    inc r20\n"
      "    nop\n"
      "    out %[portd], r20\n"
      "    inc r20\n"
      "    out %[portd], r20\n"
      "    nop\n"
      "    inc r20\n"
      "    out %[portd], r20\n"
      "    inc r20\n"
      "    out %[portd], r20\n"
      "    inc r20\n"
      "    out %[portd], r20\n"
      "    inc r20\n"
      "    nop\n"
      "    out %[portd], r20\n"
      "    inc r20\n"
      "    out %[portd], r20\n"
      "    inc r20\n"
      "    out %[portd], r20\n"
      "    inc r20\n"
      ".endr\n"
      //"    out %[portd], __zero_reg__\n"
      :
      :[portd] "I" (_SFR_IO_ADDR(HADDR_PORT))
      :"r20"
    );

  // Notify HLINE stop
  asm volatile("sbi %[portb], %[outp]\n"::[portb] "I" (_SFR_IO_ADDR(CONTROL_PORT)), [outp] "i" (CTRL_HLINE_PIN):);

  //
  // Front Porch Section
  //
  
  // Sync and stabilize signal
  asm volatile(
      ".rept 8\n"
      "    nop\n"
      ".endr\n"
    );
}

void loop() {
}
