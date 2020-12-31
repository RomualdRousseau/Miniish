#define CONTROL_PORT     PORTB
#define VADDR_PORT       PORTC
#define HADDR_PORT       PORTD

#define VADDR7_PIN       0  // PIN 8  (PB0)
#define CTRL_HSYNC_PIN   1  // PIN 9  (PB1)
#define CTRL_VSYNC_PIN   2  // PIN 10 (PB2)
#define CTRL_HLINE_PIN   3  // PIN 11 (PB3)
#define CTRL_VBLANK_PIN  4  // PIN 12 (PB4)

#define VSYNC_PULSE      158    // 63.6us
#define VSYNC_LENGTH     41719  // 16.687ms
#define VSYNC_START_LINE -80

#define HSYNC_PULSE      8      // 3.6us
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

  // Start all timers with a prescaler of 1/8

  TCCR0B |= (1 << CS00);
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
    } else if (vline == -10) {
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

  #define DEJITTER_SYNC -4
  asm volatile(
    "     lds r16, %[timer]\n"
    "     subi r16, %[tsync]\n"
    "     andi r16, 7\n"
    "     call TL\n"
    "TL:\n"
    "     pop r31\n"
    "     pop r30\n"
    "     adiw r30, (LW-TL-5)\n"
    "     add r30, r16\n"
    "     ijmp\n"
    "LW:\n"
    ".rept 9\n"
    "     nop\n"
    ".endr\n"
    :
    : [timer] "i" (&TCNT0),
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
}

void loop() {
}
