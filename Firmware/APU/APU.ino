#include <synth.h>

#define PIN_RW         (1 << PORTB1)
#define PIN_ENABLE     (1 << PORTB2)
#define PIN_CLOCK      (1 << PORTB4)
#define PIN_IRQ        (1 << PORTB5)

#define FUNC_CTRL      0x00
#define FUNC_STATUS    0x01
#define FUNC_MASK      0x02
#define FUNC_PITCH     0x10
#define FUNC_WAVE      0x11
#define FUNC_EFFECT    0x13

#define STATUS_READY   0b00000001

#define TICK (60 / (16 * 450))

synth edgar;

word commands[256];
byte command_curr = 0;

byte status = 0;

byte voice_mask[] = {-1, -1, -1, -1};
byte voice_curr = 0;

void setup() {

  // Configure Control Port

  DDRB = ~(PIN_RW | PIN_ENABLE | PIN_CLOCK) | PIN_IRQ;

  // IRQ Disable

  PORTB |= PIN_IRQ;

  // Configure the Address and Data Bus

  DDRC = 0b00000000;
  DDRD = 0b11111111;
  PORTD = status;

  // Start synthesizer

  edgar.begin();

  // A little note

  edgar.setupVoice(0,TRIANGLE,60,ENVELOPE1,127,64);

  edgar.setFrequency(0,50.0);
  edgar.trigger(0);
  delay(100);
  edgar.setFrequency(0,60.0);
  edgar.trigger(0);
  delay(100);
  edgar.setFrequency(0,440.0);
  edgar.trigger(0);
  delay(100);
  edgar.setFrequency(0,1000.0);
  edgar.trigger(0);
  delay(100);

  cli();

  status |= STATUS_READY;

  for (;;) {

    // Check if a command is available, skip otherwise

    if (PINB & (PIN_ENABLE | PIN_CLOCK))
    {
      continue;
    }

    // Read the command

    const byte addr = PINC;
    const byte flags = PINB;

    if (flags & PIN_RW) {

      // Command is a read

      DDRD = 0b11111111;

      // Process the command

      switch (addr) {
        case FUNC_STATUS:
          PORTD = status;
          break;
      }

      while (!(PINB & PIN_ENABLE))
      {
        ; // wait to the end of the command
      }

      PORTB |= PIN_IRQ;
    } else {

      // Command is a write

      DDRD = 0b00000000;
      while (!(PINB & PIN_CLOCK))
      {
        ; // wait to receive the data
      }
      const byte data = PIND;

      while (!(PINB & PIN_ENABLE))
      {
        ; // wait to the end of the command
      }

      commands[command_curr++] = (addr << 8) + data;

      PORTB |= PIN_IRQ;

      if ((addr & 0x3F) == FUNC_CTRL) {

        // Execute the commands in the queue

        sei();
        process_commands();
        cli();

        // Notify CPU we are ready

        PORTB &= ~PIN_IRQ;
      }
    }
  }
}

void process_commands() {
  for (int i = 0; i < command_curr; i++) {

    // Parse the command

    const byte ctrl = (commands[i] >> 8) & 0x3F;
    const byte data = commands[i];

    // Exceute the command

    switch (ctrl) {

      case FUNC_CTRL:
        for (int i = 0; i < 4; i++) {
          if (!voice_mask[i]) {
            edgar.setTime(i, (float) data * TICK);
            edgar.trigger(i);
          }
        }
        delay(data * TICK);
        break;
        
      case FUNC_MASK:
        voice_curr = data;
        voice_mask[data] = 0;
        break;

      case FUNC_PITCH:
        edgar.setFrequency(voice_curr, 65.41 * pow(2, data / 12));
        break;

      case FUNC_WAVE:
        edgar.setWave(voice_curr, data);
        break;

      case FUNC_EFFECT:
        break;
    }
  }

  // Reset all commands

  command_curr = 0;
}

void loop() {
}
