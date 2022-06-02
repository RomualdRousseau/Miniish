#include <synth.h>

#define PIN_RW         (1 << PORTB1)
#define PIN_ENABLE     (1 << PORTB2)
#define PIN_CLOCK      (1 << PORTB4)
#define PIN_IRQ        (1 << PORTB5)


#define FUNC_STATUS    0x00
#define FUNC_CTRL      0x0A
#define FUNC_CTRL_WAV0 0x01
#define FUNC_CTRL_ENV0 0x02
#define FUNC_CTRL_LEN0 0x03
#define FUNC_CTRL_MOD0 0x04
#define FUNC_NOTE0     0x05
#define FUNC_CTRL_WAV1 0x11
#define FUNC_CTRL_ENV1 0x12
#define FUNC_CTRL_LEN1 0x13
#define FUNC_CTRL_MOD1 0x14
#define FUNC_NOTE1     0x15
#define FUNC_CTRL_WAV2 0x21
#define FUNC_CTRL_ENV2 0x22
#define FUNC_CTRL_LEN2 0x23
#define FUNC_CTRL_MOD2 0x24
#define FUNC_NOTE2     0x25
#define FUNC_CTRL_WAV3 0x31
#define FUNC_CTRL_ENV3 0x32
#define FUNC_CTRL_LEN3 0x33
#define FUNC_CTRL_MOD3 0x34
#define FUNC_NOTE3     0x35


#define STATUS_READY   0b00000001

synth edgar;

word commands[256];
byte command_curr = 0;

byte status = 0;

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
    const byte voice = (ctrl >> 4);

    // Exceute the command

    switch (ctrl) {

      case FUNC_CTRL_WAV0:
      case FUNC_CTRL_WAV1:
      case FUNC_CTRL_WAV2:
      case FUNC_CTRL_WAV3:
        edgar.setWave(voice, data);
        break;

      case FUNC_CTRL_ENV0:
      case FUNC_CTRL_ENV1:
      case FUNC_CTRL_ENV2:
      case FUNC_CTRL_ENV3:
        edgar.setEnvelope(voice, data);
        break;

      case FUNC_CTRL_LEN0:
      case FUNC_CTRL_LEN1:
      case FUNC_CTRL_LEN2:
      case FUNC_CTRL_LEN3:
        edgar.setLength(voice, data);
        break;

      case FUNC_CTRL_MOD0:
      case FUNC_CTRL_MOD1:
      case FUNC_CTRL_MOD2:
      case FUNC_CTRL_MOD3:
        edgar.setMod(voice, data);
        break;

      case FUNC_NOTE0:
      case FUNC_NOTE1:
      case FUNC_NOTE2:
      case FUNC_NOTE3:
        edgar.mTrigger(voice, data);
        break;

      case FUNC_CTRL:
        delay(data * 10);
        break;
    }
  }

  // Reset all commands

  command_curr = 0;
}

void loop() {
}
