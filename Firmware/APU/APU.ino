#include "synth.h"



#define PIN_RW         (1 << PORTB1)
#define PIN_ENABLE     (1 << PORTB2)
#define PIN_CLOCK      (1 << PORTB4)
#define PIN_IRQ        (1 << PORTB5)

#define FUNC_CTRL       0x00
#define FUNC_STATUS     0x01
#define FUNC_SND0       0x10
#define FUNC_SND1       0x11
#define FUNC_SND2       0x12
#define FUNC_SND3       0x13

#define STATUS_READY   0b00000001

Synth edgar;

word voice_data[] = {0, 0, 0, 0};
byte voice_mask[] = {0, 0, 0, 0};

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

  // Play a little note

  edgar.setSpeed(0, 16.0f);
  edgar.setWave(0, TRIANGLE);
  edgar.setEnvelope(0, ENVELOPE2);
  edgar.setMod(0, 64);
  edgar.setFrequency(0, 50.0f); 
  edgar.trigger(0);
  delay(floor(16.0f * TICK * 1000.f));
  edgar.setFrequency(0, 60.0f);
  edgar.trigger(0);
  delay(floor(16.0f * TICK * 1000.f));
  edgar.setFrequency(0, 440.0f);
  edgar.trigger(0);
  delay(floor(16.0f * TICK * 1000.f));
  edgar.setFrequency(0, 1000.0f);
  edgar.trigger(0);
  delay(floor(16.0f * TICK * 1000.f));

  // Reset everything to known values

  for( int i = 0; i < 4; i++) {
    edgar.setWave(0, 0);
    edgar.setEnvelope(0, 0);
    edgar.setMod(0, 64);
    edgar.setTime(0, 0.0f);
    edgar.setFrequency(0, 0.0f);
  }

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

    // Execute the command

    switch (ctrl) {

      case FUNC_CTRL:
        for (int i = 0; i < 4; i++) if (voice_mask[i]) {
          const float speed = data;
          const float pitch = (voice_data[i] >> 8) & 0x00FF;
          const byte wave = (voice_data[i] >> 4) & 0x000F;
          const byte effect = voice_data[i] & 0x000F; 
          edgar.setWave(i, wave);
          edgar.setPitch(i, pitch);
          edgar.setSpeed(i, speed);
          switch(effect) {
            case 1: // FADE_IN
              edgar.setEnvelope(i, ENVELOPE1);
              edgar.setMod(i, 64);
              break;
            case 2: // FADE OUT
              edgar.setEnvelope(i, ENVELOPE2);
              edgar.setMod(i, 64);
              break;
            case 3: // DROP
              edgar.setEnvelope(i, ENVELOPE0);
              edgar.setMod(i, 0);
              break;
            case 4: // SLIDE
              edgar.setEnvelope(i, ENVELOPE0);
              edgar.setMod(i, 127);
              break;
            case 5: // VIBRATO
              edgar.setEnvelope(i, ENVELOPE0);
              edgar.setMod(i, 64);
              break;
            default: // NONE
              edgar.setEnvelope(i, ENVELOPE0);
              edgar.setMod(i, 64);
              break;
          }
          edgar.trigger(i);
        }
        delay(floor(((float) data) * TICK * 1000.0f));
        for (int i = 0; i < 4; i++) {
          voice_data[i] = 0;
          voice_mask[i] = 0;
        }
        break;

      case FUNC_SND0:
        voice_data[0] = (voice_data[0] << 8) + data;
        voice_mask[0] = 1;
        break;
        
      case FUNC_SND1:
        voice_data[1] = (voice_data[1] << 8) + data;
        voice_mask[1] = 1;
        break;

      case FUNC_SND2:
        voice_data[2] = (voice_data[2] << 8) + data;
        voice_mask[2] = 1;
        break;
        
      case FUNC_SND3:
        voice_data[3] = (voice_data[3] << 8) + data;
        voice_mask[3] = 1;
        break;
    }
  }

  // Reset all commands

  command_curr = 0;
}

void loop() {
}
