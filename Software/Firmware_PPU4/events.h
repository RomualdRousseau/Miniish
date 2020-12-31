#include "data.h"

void load_data_from_eeprom() {
  memcpy_P(gmem.nametables, nametable, 2 * 12 * 20);
  memcpy_P(gmem.attributes, attributes, 2 * 12 * 20);
  memcpy_P(gmem.palettes, palettes, 8 * 4);
  memcpy_P_T(gmem.patterns, patterns, 64, 16);
}

void load_data_from_rom() {
  memcpy_R(gmem.palettes, 0x0000, 8 * 4);
  memcpy_R(gmem.patterns, 0x0020, 64 * 16);
}

void build_next_block() {
  byte* vram = vram_data;

  byte* n_y = &gmem.nametables[0][vram_block * TILE_PER_BLOCK][0];
  
  for (byte y = 0; y < BLOCK_SIZE; y++) {
    const byte yy = y & (TILE_SIZE - 1);
    const byte* p_y = gmem.patterns[yy];
    const byte* n_x = n_y + SCREEN_BORDER;
    const byte* a_x = n_y + 512;
    
    vram += SCREEN_BORDER * TILE_SIZE;
    
    for (int x = 0; x < SCREEN_COLUMNS - 2 * SCREEN_BORDER; x++) {
      const byte* p = gmem.palettes[*a_x];
      const byte* s = &p_y[*n_x];
      byte s1 = s[0];
      byte s2 = s[TILE_SIZE * 64];

      for (int xx = 0; xx < TILE_SIZE; xx++) {
        *(vram++) = p[((s2 & 128) >> 6) | ((s1 & 128) >> 7)];
        s1 <<= 1;
        s2 <<= 1;
      }

      n_x++;
      a_x++;
    }

    vram += SCREEN_BORDER * TILE_SIZE;

    if (yy == (TILE_SIZE - 1)) {
      n_y += SCREEN_COLUMNS;
    }
  }
}

void read_commands() {
  byte* pgmem = (byte*) &gmem.nametables[0][0][0];
  byte* poam = (byte*) &oam[0];
 
  while (PINB & PIN_VBLANK) {

    // Check if a command is available, skip otherwise
    
    if (PINB & (PIN_ENABLE | PIN_CLOCK))
    {
      continue;
    }
  
    // Read the command
    
    const byte addr = PIND;
    const byte flags = PINB;

    if (flags & PIN_RW) {
      DDRC = 0b11111111;
      
      switch(addr) {
        case FUNC_STATUS:
          gmem_addr = 0;
          dma_addr = 0;
          PORTC = status;
          break;

        case FUNC_MEM_DATA:
          PORTC = pgmem[gmem_addr];
          break;

        case FUNC_OAM_DATA:
          PORTC = poam[oam_addr];
          break;
      }
    } else {
      DDRC = 0b00000000;
      while (!(PINB & PIN_CLOCK))
      {
        ; // wait to receive the data
      }
      const byte data = PINC;
  
      switch(addr) {
        case FUNC_CTRL:
          control = data;
          break;
          
        case FUNC_MEM_ADDR:
          gmem_addr = (gmem_addr << 8) + data;
          break;
    
        case FUNC_MEM_DATA:
          pgmem[gmem_addr] = data;
          gmem_addr += gmem_incr;
          break;

        case FUNC_OAM_ADDR:
          oam_addr = data;
          break;
    
        case FUNC_OAM_DATA:
          poam[oam_addr] = data;
          oam_addr++;
          break;

        case FUNC_DMA_ADDR:
          dma_addr = (dma_addr << 8) + data;
          break;
    
        case FUNC_DMA_DATA:
          dma_type = data;
          status |= STATUS_DMA;
          break;
      }
    }
    
    while (!(PINB & PIN_ENABLE))
    {
      ; // wait to the end of the command
    }
  }
}

void process_commands() {
  const byte base = control & CONTROL_BASE;
  byte* nametable = &gmem.nametables[base][0][0];
  
  for (byte i = 0; i < OAM_COUNT; i++) {
    oam_t* o = &oam[i];
    if (o->attribute & OAM_ATTR_SHOW) {
      int off = o->posy * 20 + o->posx;
      nametable[off] = o->pattern;
      nametable[off + 512] = o->attribute & OAM_ATTR_PAL;
    }
  }
}
