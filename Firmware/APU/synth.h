#ifndef _SYNTH
#define _SYNTH
#include <avr/pgmspace.h>
#include <avr/interrupt.h>

#include "tables.h"

#define FS 20000.0f
#define BPM  450.0f

#define SINE     0
#define TRIANGLE 1
#define SQUARE   2
#define SAW      3
#define RAMP     4
#define NOISE    5

#define ENVELOPE0 0
#define ENVELOPE1 1
#define ENVELOPE2 2
#define ENVELOPE3 3

#define TICK (60.0f / (16.0f * BPM))

#define SET(x,y) (x |=(1<<y))		    //-Bit set/clear macros
#define CLR(x,y) (x &= (~(1<<y)))

volatile unsigned int PCW[4] = {    //-Wave phase accumulators
  0, 0, 0, 0
};			
volatile unsigned int FTW[4] = {    //-Wave frequency tuning words
  1000, 200, 300, 400
};           
volatile unsigned char AMP[4] = {   //-Wave amplitudes [0-255]
  255, 255, 255, 255
};           
volatile unsigned int PITCH[4] = {  //-Voice pitch
  500, 500, 500, 500
};          
volatile int MOD[4] = {             //-Voice envelope modulation [0-1023 512=no mod. <512 pitch down >512 pitch up]
  20, 0, 64, 127
};                         
volatile unsigned int wavs[4];      //-Wave table selector [address of wave in memory]
volatile unsigned int envs[4];      //-Envelopte selector [address of envelope in memory]
volatile unsigned int EPCW[4] = {   //-Envelope phase accumulator
  0x8000, 0x8000, 0x8000, 0x8000
}; 
volatile unsigned int EFTW[4] = {   //-Envelope speed tuning word
  10, 10, 10, 10
};               
volatile unsigned char divider = 4; //-Sample rate decimator for envelope
volatile unsigned int tim = 0;
volatile unsigned char tik = 0;


//*********************************************************************************************
//  Audio driver interrupt
//*********************************************************************************************

SIGNAL(TIMER1_COMPA_vect)
{
  //-------------------------------
  // Time division
  //-------------------------------
  divider++;
  if (!(divider &= 0x03))
    tik = 1;

  //-------------------------------
  // Volume envelope generator
  //-------------------------------

  if (!(((unsigned char*)&EPCW[divider])[1] & 0x80))
    AMP[divider] = pgm_read_byte(envs[divider] + (((unsigned char*) & (EPCW[divider] += EFTW[divider]))[1]));
  else
    AMP[divider] = 0;

  //-------------------------------
  //  Synthesizer/audio mixer
  //-------------------------------

  OCR2A = OCR2B = 127 +
                  ((
                     (((signed char)pgm_read_byte(wavs[0] + ((unsigned char *) & (PCW[0] += FTW[0]))[1]) * AMP[0]) >> 8) +
                     (((signed char)pgm_read_byte(wavs[1] + ((unsigned char *) & (PCW[1] += FTW[1]))[1]) * AMP[1]) >> 8) +
                     (((signed char)pgm_read_byte(wavs[2] + ((unsigned char *) & (PCW[2] += FTW[2]))[1]) * AMP[2]) >> 8) +
                     (((signed char)pgm_read_byte(wavs[3] + ((unsigned char *) & (PCW[3] += FTW[3]))[1]) * AMP[3]) >> 8)
                   ) >> 2);

  //************************************************
  //  Modulation engine
  //************************************************

  FTW[divider] = PITCH[divider] + (int)   (((PITCH[divider] >> 6) * (EPCW[divider] >> 6)) / 128) * MOD[divider];
  
  tim++;
}

class Synth
{
  private:

  public:

    Synth()
    {
    }

    void begin()
    {
      TCCR1A = 0x00;                                  //-Start audio interrupt
      TCCR1B = 0x09;
      TCCR1C = 0x00;
      OCR1A = 16000000.0 / FS;			                  //-Auto sample rate
      SET(TIMSK1, OCIE1A);                            //-Start audio interrupt
      sei();                                          //-+

      TCCR2A = 0x83;                                  //-8 bit audio PWM
      TCCR2B = 0x01;                                  // |
      OCR2A = 127;                                    //-+
      SET(DDRB, 3);				                            //-PWM pin
    }

    //*********************************************************************
    //  Timing/sequencing functions
    //*********************************************************************

    unsigned char synthTick(void)
    {
      if (tik)
      {
        tik = 0;
        return 1;  //-True every 4 samples
      }
      return 0;
    }

    unsigned char voiceFree(unsigned char voice)
    {
      if (!(((unsigned char*)&EPCW[voice])[1] & 0x80))
        return 0;
      return 1;
    }

    //*********************************************************************
    //  Setup wave [0-6]
    //*********************************************************************

    void setWave(unsigned char voice, unsigned char wave)
    {
      switch (wave)
      {
        case TRIANGLE:
          wavs[voice] = (unsigned int)TriangleTable;
          break;
        case SQUARE:
          wavs[voice] = (unsigned int)SquareTable;
          break;
        case SAW:
          wavs[voice] = (unsigned int)SawTable;
          break;
        case RAMP:
          wavs[voice] = (unsigned int)RampTable;
          break;
        case NOISE:
          wavs[voice] = (unsigned int)NoiseTable;
          break;
        default:
          wavs[voice] = (unsigned int)SinTable;
          break;
      }
    }

    //*********************************************************************
    //  Setup Envelope [0-4]
    //*********************************************************************

    void setEnvelope(unsigned char voice, unsigned char env)
    {
      switch (env)
      {
        case ENVELOPE1:
          envs[voice] = (unsigned int)Env1;
          break;
        case ENVELOPE2:
          envs[voice] = (unsigned int)Env2;
          break;
        case ENVELOPE3:
          envs[voice] = (unsigned int)Env3;
          break;
        default:
          envs[voice] = (unsigned int)Env0;
          break;
      }
    }

    //*********************************************************************
    //  Setup mod
    //*********************************************************************

    void setMod(unsigned char voice, unsigned char mod)
    {
      MOD[voice] = (int)mod - 64; //0-1023 512=no mod
    }

    //*********************************************************************
    //  Setup frequency
    //*********************************************************************

    void setFrequency(unsigned char voice, float f)
    {
      PITCH[voice] = f / (FS / 65535.0);
    }

    void setPitch(unsigned char voice, float p)
    {
      this->setFrequency(voice, 65.41f * pow(2.0f, p / 12.0f));
    }

    //*********************************************************************
    //  Setup time
    //*********************************************************************

    void setTime(unsigned char voice, float t)
    {
      EFTW[voice] = (1.0f / t) / (FS / 32767.5f);
    }

    void setSpeed(unsigned char voice, float s)
    {
      this->setTime(voice, s * TICK);
    }

    //*********************************************************************
    //  Trigger
    //*********************************************************************

    void trigger(unsigned char voice)
    {
      EPCW[voice] = 0;
      FTW[voice] = PITCH[voice];
    }

    //*********************************************************************
    //  Suspend/resume synth
    //*********************************************************************

    void suspend()
    {
      CLR(TIMSK1, OCIE1A); //-Stop audio interrupt
    }
    void resume()
    {
      SET(TIMSK1, OCIE1A); //-Start audio interrupt
    }
};

#endif
