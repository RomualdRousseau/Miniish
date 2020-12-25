#define ROMB      (1 << PORTB0)
#define WRAM      (1 << PORTB1)
#define VBLANK    (1 << PORTB2)
#define RW        (1 << PORTB3)
#define PORT2     (1 << PORTB4)
#define NMI       (1 << PORTB5)
#define CLOCK     (1 << PORTB6)

void setup() {
  DDRB = ~(VBLANK | RW | PORT2 | CLOCK);
  PORTB = ROMB | WRAM | NMI;
}

void loop() {
}
