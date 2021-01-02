class VRAM_t
{
  public:
    void init() {
      memset(&gmem, 0, sizeof(gmem_t));
      memset(oam, 0, OAM_COUNT * sizeof(oam_t));
    }

    void clear();

    void write();

    void build_first_block() {
      vram_block = 0;
      build_block();
    }

    void build_next_block() {
      vram_block++;
      if (vram_block < (SCREEN_ROWS / TILE_PER_BLOCK)) {
        build_block();
      }
    }

  private:
    void build_block();
};
VRAM_t VRAM;

void VRAM_t::clear() {

  // Acquire the Address and Data Bus

  DDRA = 0b11111111;
  DDRD = 0b11111111;
  DDRC = 0b11111111;

  // Write pixels

  asm volatile(

    "start_clear_line:\n"

    // Output y coordinate

    "    out %[porta], %[y]\n"

    "loop_clear_line:\n"

    // Output x coordinate

    "    out %[portd], %[x]\n"

    // Output black pixel

    "    out %[portc], __zero_reg__\n"
    "    cbi %[portb], %[wram]\n"
    "    sbi %[portb], %[wram]\n"

    // Next pixel

    "    inc %[x]\n"

    // Check if end of line, continue otherwise

    "    cpi %[x], "STRINGIFY(SCREEN_REAL_WIDTH + 1)"\n"
    "    brne loop_clear_line\n"

    // Go to the next clear line

    "    clr %[x]\n"
    "    inc %[y]\n"
    "    cp %[y], %[h]\n"
    "    breq clear_end_frame\n"

    "    rjmp start_clear_line\n"

    "clear_end_frame:\n"
    :
    :[porta] "I" (_SFR_IO_ADDR(PORTA)),
    [portb]  "I" (_SFR_IO_ADDR(PORTB)),
    [portc]  "I" (_SFR_IO_ADDR(PORTC)),
    [portd]  "I" (_SFR_IO_ADDR(PORTD)),
    [x]      "r" (0),
    [y]      "r" (vram_block * (BLOCK_SIZE + 1)),
    [h]      "r" (vram_block * (BLOCK_SIZE + 1) + (BLOCK_SIZE + 1)),
    [wram]   "i" (PINB1)
    : "r20"
  );

  // Release the Address and Data Bus

  DDRA = 0b00000000;
  DDRD = 0b00000000;
  DDRC = 0b00000000;

  if (vram_block == (SCREEN_ROWS / TILE_PER_BLOCK - 1)) {
    status |= STATUS_CLEAR;
  }
}

void VRAM_t::write() {
  
  // Acquire the Address and Data Bus

  DDRA = 0b11111111;
  DDRD = 0b11111111;
  DDRC = 0b11111111;

  // Write pixels

  asm volatile(

    "    movw z, %[vram]\n"

    "start_scan_line:\n"

    // Output y coordinate

    "    out %[porta], %[y]\n"

    "loop_scan_line:\n"

    // Output x coordinate

    "    out %[portd], %[x]\n"

    // Output pixel

    "    ld __tmp_reg__, z+\n"
    "    out %[portc], __tmp_reg__\n"
    "    cbi %[portb], %[wram]\n"
    "    sbi %[portb], %[wram]\n"

    // Next pixel

    "    inc %[x]\n"

    // Check if end of line, continue otherwise

    "    cpi %[x], "STRINGIFY(SCREEN_WIDTH + (SCREEN_REAL_WIDTH - SCREEN_WIDTH) / 2)"\n"
    "    brne loop_scan_line\n"

    // Go to the next scan line

    "    subi %[x], "STRINGIFY(SCREEN_WIDTH)"\n"
    "    inc %[y]\n"
    "    cp %[y], %[h]\n"
    "    breq scan_end_frame\n"

    "    rjmp start_scan_line\n"

    "scan_end_frame:\n"
    :
    :[porta] "I" (_SFR_IO_ADDR(PORTA)),
    [portb]  "I" (_SFR_IO_ADDR(PORTB)),
    [portc]  "I" (_SFR_IO_ADDR(PORTC)),
    [portd]  "I" (_SFR_IO_ADDR(PORTD)),
    [x]      "r" ((SCREEN_REAL_WIDTH - SCREEN_WIDTH) / 2),
    [y]      "r" (vram_block * BLOCK_SIZE + 1),
    [h]      "r" (vram_block * BLOCK_SIZE + BLOCK_SIZE + 1),
    [vram]   "l" (vram_data),
    [wram]   "i" (PINB1)
    : "r20"
  );

  // Release the Address and Data Bus

  DDRA = 0b00000000;
  DDRD = 0b00000000;
  DDRC = 0b00000000;
}

void VRAM_t::build_block() {
  const byte start_y = vram_block * BLOCK_SIZE;
  byte* n_y = &gmem.nametables[0][start_y / TILE_SIZE][0];
  byte* vram_y = vram_data;

  for (byte y = 0; y < BLOCK_SIZE; y++) {
    const byte yy = y & (TILE_SIZE - 1);
    const byte* p_y = gmem.patterns[yy];
    const byte* n_x = n_y;
    const byte* a_x = n_x + ATTRIBUTES_OFFSET;

    // Draw tiles on the scanline

    byte* vram_x = vram_y;

    for (byte x = 0; x < SCREEN_COLUMNS; x++, n_x++, a_x++) {
      const byte* p = gmem.palettes[*a_x];
      const byte* s = &p_y[*n_x];
      const byte lo = s[0];
      const byte hi = s[TILE_SIZE * PATTERNS_COUNT];

      // Decode and draw one line of the tile

      for (byte xx = TILE_SIZE; xx > 0; xx--, vram_x++) {
        const byte b = 1 << (xx - 1);
        const byte v = ((lo & b) ? 1 : 0) + ((hi & b) ? 2 : 0);
        *vram_x = p[v];
      }
    }

    // Draw sprites on the scanline

    for (byte j = 0, i = 0; j < SPRITE_PER_SCANLINE && i < OAM_COUNT; i++) {
      const oam_t* o = &oam[i];

      // Skip if sprite if not show

      if (!(o->attribute & OAM_ATTR_SHOW)) {
        continue;
      }

      // Skip if sprite is not on the scanline

      const byte off_y = start_y + y - o->posy;
      if (!(o->attribute & OAM_ATTR_SHOW) || (off_y >= TILE_SIZE)) {
        continue;
      }

      // Offset the sprite location

      vram_x = vram_y + o->posx;

      const byte* p = gmem.palettes[(o->attribute & OAM_ATTR_PAL) + OAM_PALETTES_OFFSET];
      const byte* s = &gmem.patterns[off_y][o->pattern];
      const byte lo = s[0];
      const byte hi = s[TILE_SIZE * PATTERNS_COUNT];

      // Decode and draw one line of the sprite: 0 is transparency

      for (byte xx = TILE_SIZE; xx > 0; xx--, vram_x++) {
        const byte b = 1 << (xx - 1);
        const byte v = ((lo & b) ? 1 : 0) + ((hi & b) ? 2 : 0);
        if (v) {
          *vram_x = p[v];
        }
      }

      // Consume one sprite

      j++;
    }

    // Prepare next scanline

    vram_y += SCREEN_WIDTH;

    if (yy == (TILE_SIZE - 1)) {
      n_y += SCREEN_COLUMNS;
    }
  }
}
