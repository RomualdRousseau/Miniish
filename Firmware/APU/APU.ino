#include "synth.h"

#define PIN_RW         (1 << PORTB1)
#define PIN_ENABLE     (1 << PORTB2)
#define PIN_CLOCK      (1 << PORTB4)
#define PIN_IRQ        (1 << PORTB5)

#define FUNC_CTRL      0x00
#define FUNC_STATUS    0x01
#define FUNC_SND0      0x10
#define FUNC_SND1      0x11
#define FUNC_SND2      0x12
#define FUNC_SND3      0x13

#define STATUS_READY   0b00000001

Synth synth;

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

  synth.begin();

  // Play a little note as diagnostic

  synth.setWave(0, TRIANGLE);
  synth.setEnvelope(0, ENVELOPE2);
  synth.setSpeed(0, 16.0f);
  synth.setFrequency(0, 440.0f);
  synth.trigger(0);
  synth.wait();
  synth.setFrequency(0, 1000.0f);
  synth.trigger(0);
  synth.wait();

  synth.reset();

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

        // Notify CPU we are ready to accept next commands

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
          const float pitch = (voice_data[i] >> 8) & 0x00FF;
          const byte wave   = (voice_data[i] >> 4) & 0x000F;
          const byte effect = voice_data[i] & 0x000F;
          const float speed = data; 
          synth.setWave(i, wave);
          synth.setPitch(i, pitch);
          synth.setSpeed(i, speed);
          switch(effect) {
            case 1: // FADE_IN
              synth.setEnvelope(i, ENVELOPE1);
              synth.setModulation(i, 64);
              break;
            case 2: // FADE OUT
              synth.setEnvelope(i, ENVELOPE2);
              synth.setModulation(i, 64);
              break;
            case 3: // DROP
              synth.setEnvelope(i, ENVELOPE3);
              synth.setModulation(i, 64);
              break;
            case 4: // SLIDE
              synth.setEnvelope(i, ENVELOPE0);
              synth.setModulation(i, 127);
              break;
            case 5: // VIBRATO
              synth.setEnvelope(i, ENVELOPE0);
              synth.setModulation(i, 64);
              break;
            default: // NONE
              synth.setEnvelope(i, ENVELOPE0);
              synth.setModulation(i, 64);
              break;
          }
          synth.trigger(i);
        }
        synth.wait();
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
