#ifndef _SYNTH
#define _SYNTH
#include <avr/pgmspace.h>
#include <avr/interrupt.h>

#include "tables.h"

#define FS        20000.0f
#define BPM       450.0f

#define SINE      0
#define TRIANGLE  1
#define SQUARE    2
#define SAW       3
#define RAMP      4
#define NOISE     5

#define ENVELOPE0 0
#define ENVELOPE1 1
#define ENVELOPE2 2
#define ENVELOPE3 3

#define TICK       (60.0f / (16.0f * BPM))
#define PIN_OUTPUT (1 << PORTB3)

volatile word wavs[4];
volatile word envs[4];

volatile word PITCH[4];
volatile int MOD[4];

volatile word EFTW[4];      // Envelope speed tuning word
volatile word EPCW[4];      // Envelope phase accumulator
volatile word FTW[4];       // Wave frequency tuning words
volatile word PCW[4];       // Wave phase accumulators
volatile byte AMP[4];

volatile byte divider = 4;
float time_to_wait = 0;

//*********************************************************************************************
//  Audio driver interrupt
//*********************************************************************************************

SIGNAL(TIMER1_COMPA_vect)
{
  //-------------------------------
  // Time division
  //-------------------------------
  divider++;
  divider &= 0x03;

  //-------------------------------
  // Volume envelope generator
  //-------------------------------

  if (!(((byte*)&EPCW[divider])[1] & 0x80)) {
    AMP[divider] = pgm_read_byte(envs[divider] + (((byte*) & (EPCW[divider] += EFTW[divider]))[1]));
  }
  else {
    AMP[divider] = 0;
  }

  //-------------------------------
  //  Synthesizer/audio mixer
  //-------------------------------

  OCR2A = OCR2B = 127 +
                  ((
                     (((char)pgm_read_byte(wavs[0] + ((byte*) & (PCW[0] += FTW[0]))[1]) * AMP[0]) >> 8) +
                     (((char)pgm_read_byte(wavs[1] + ((byte*) & (PCW[1] += FTW[1]))[1]) * AMP[1]) >> 8) +
                     (((char)pgm_read_byte(wavs[2] + ((byte*) & (PCW[2] += FTW[2]))[1]) * AMP[2]) >> 8) +
                     (((char)pgm_read_byte(wavs[3] + ((byte*) & (PCW[3] += FTW[3]))[1]) * AMP[3]) >> 8)
                   ) >> 2);

  //************************************************
  //  Modulation engine
  //************************************************

  FTW[divider] = PITCH[divider] + (int)(((PITCH[divider] >> 6) * (EPCW[divider] >> 6)) >> (6 + 1)) * MOD[divider];
}

class Synth
{
  public:

    Synth()
    {
      this->reset();
    }

    void begin()
    {
      TCCR1A = 0x00;
      TCCR1B = 0x09;
      TCCR1C = 0x00;
      OCR1A = 16000000.0 / FS; // Sampling rate
      TIMSK1 |= (1 << OCIE1A);
      
      TCCR2A = 0x83;
      TCCR2B = 0x01;
      OCR2A = 127;
      DDRB |= PIN_OUTPUT;

      sei();
    }

    void reset() {
      for ( int i = 0; i < 4; i++) {
        this->setWave(0, 0);
        this->setEnvelope(0, 0, 3);
        this->setModulation(0, 64);
        this->setTime(0, 0.0f);
        this->setFrequency(0, 0.0f);
      }
    }

    boolean isVoiceFree(byte voice)
    {
      return ((byte*)&EPCW[voice])[1] & 0x80;
    }

    void setWave(byte voice, byte wave)
    {
      switch (wave)
      {
        case TRIANGLE:
          wavs[voice] = (word)TriangleTable;
          break;
        case SQUARE:
          wavs[voice] = (word)SquareTable;
          break;
        case SAW:
          wavs[voice] = (word)SawTable;
          break;
        case RAMP:
          wavs[voice] = (word)RampTable;
          break;
        case NOISE:
          wavs[voice] = (word)NoiseTable;
          break;
        default:
          wavs[voice] = (word)SinTable;
          break;
      }
    }

    void setEnvelope(byte voice, byte env, byte volume)
    {
      switch (env)
      {
        case ENVELOPE1:
          envs[voice] = (word)Env1[volume];
          break;
        case ENVELOPE2:
          envs[voice] = (word)Env2[volume];
          break;
        case ENVELOPE3:
          envs[voice] = (word)Env3[volume];
          break;
        default:
          envs[voice] = (word)Env0[volume];
          break;
      }
    }

    void setFrequency(byte voice, float f)
    {
      PITCH[voice] = f / (FS / 65535.0f);
    }

    void setPitch(byte voice, float p)
    {
      this->setFrequency(voice, 65.41f * pow(2.0f, p / 12.0f));
    }

    void setTime(byte voice, float t)
    {
      EFTW[voice] = (1.0f / t) / (FS / (32767.5f * 4.0f));
      time_to_wait = t;
    }

    void setSpeed(byte voice, float s)
    {
      this->setTime(voice, s * TICK);
    }

    void setModulation(byte voice, byte mod)
    {
      MOD[voice] = (int)mod - 64;
    }

    void trigger(byte voice)
    {
      EPCW[voice] = 0;
      FTW[voice] = PITCH[voice];
    }

    void suspend()
    {
      TIMSK1 &= ~(1 << OCIE1A);
    }

    void resume()
    {
      TIMSK1 |= (1 << OCIE1A);
    }

    void wait()
    {
      delay(floor(time_to_wait * 1000.f));
    }
};

#endif
