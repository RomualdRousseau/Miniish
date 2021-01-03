#include <synth.h>

#define PIN_RW         (1 << PORTB1)
#define PIN_ENABLE     (1 << PORTB2)
#define PIN_CLOCK      (1 << PORTB4)

#define FUNC_CTRL      0x0A
#define FUNC_STATUS    0x0B
#define FUNC_CTRL_WAV0 0x00
#define FUNC_CTRL_ENV0 0x01
#define FUNC_CTRL_LEN0 0x02
#define FUNC_CTRL_MOD0 0x03
#define FUNC_NOTE0     0x04
#define FUNC_CTRL_WAV1 0x10
#define FUNC_CTRL_ENV1 0x11
#define FUNC_CTRL_LEN1 0x12
#define FUNC_CTRL_MOD1 0x13
#define FUNC_NOTE1     0x14
#define FUNC_CTRL_WAV2 0x20
#define FUNC_CTRL_ENV2 0x21
#define FUNC_CTRL_LEN2 0x22
#define FUNC_CTRL_MOD2 0x23
#define FUNC_NOTE2     0x24
#define FUNC_CTRL_WAV3 0x30
#define FUNC_CTRL_ENV3 0x31
#define FUNC_CTRL_LEN3 0x32
#define FUNC_CTRL_MOD3 0x33
#define FUNC_NOTE3     0x34

#define STATUS_BUSY    0b00000001

synth edgar;

word commands[256];
byte command_curr = 0;

byte status = 0;

void setup() {

  // Configure Control Port

  DDRB = ~(PIN_RW | PIN_ENABLE | PIN_CLOCK);

  // Configure the Address and Data Bus

  DDRC = 0b00000000;
  DDRD = 0b00000000;

  // Start synthesizer

  edgar.begin();
}

void loop() {

  cli();
  
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

      // Execute the commands in the queue

      if (status & STATUS_BUSY) {
        process_commands();
        status &= ~STATUS_BUSY;
      }

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
      status |= STATUS_BUSY;
    }
  }
}

void process_commands() {

  sei();
  
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

  cli();

  // Reset all commands

  command_curr = 0;
}
