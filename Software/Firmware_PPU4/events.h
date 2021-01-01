void load_data_from_rom() {
  const byte base = control & CONTROL_BASE;

  switch (dma_info.state) {
    case DMA_INIT:
      switch (dmaq[dma_info.index].type) {
        case DMA_NAMETABLE:
          dma_info.state = DMA_TRANSFER;
          dma_info.source = dmaq[dma_info.index].addr;
          dma_info.destination = &gmem.nametables[base][0][0];
          dma_info.size_curr = 0;
          dma_info.size_total = NAMETABLE_SIZE;
          break;
        case DMA_ATTRIBUTE:
          dma_info.state = DMA_TRANSFER;
          dma_info.source = dmaq[dma_info.index].addr;
          dma_info.destination = &gmem.attributes[base][0][0];
          dma_info.size_curr = 0;
          dma_info.size_total = ATTRIBUTE_SIZE;
          break;
        case DMA_PALETTE:
          dma_info.state = DMA_TRANSFER;
          dma_info.source = dmaq[dma_info.index].addr;
          dma_info.destination = &gmem.palettes[0][0];
          dma_info.size_curr = 0;
          dma_info.size_total = PALETTES_SIZE;
          break;
        case DMA_PATTERN:
          dma_info.state = DMA_TRANSFER;
          dma_info.source = dmaq[dma_info.index].addr;
          dma_info.destination = &gmem.patterns[0][0];
          dma_info.size_curr = 0;
          dma_info.size_total = PATTERNS_SIZE;
          break;
      }

    case DMA_TRANSFER:
      const size_t chunk_size = min(DMA_CHUNK_SIZE, dma_info.size_total - dma_info.size_curr);
      memcpy_R(dma_info.destination + dma_info.size_curr, dma_info.source + dma_info.size_curr, chunk_size);
      dma_info.size_curr += DMA_CHUNK_SIZE;
      if (dma_info.size_curr >= dma_info.size_total) {
        dma_info.state = DMA_INIT;
        dma_info.index++;
        if (dma_info.index >= dmaq_curr) {
          status &= ~STATUS_DMA;
        }
      }
      break;
  }
}

void build_next_block() {
  const byte start_y = vram_block * BLOCK_SIZE;
  byte* n_y = &gmem.nametables[0][start_y / TILE_SIZE][0];
  byte* vram_y = vram_data + (SCREEN_REAL_WIDTH - SCREEN_WIDTH) / 2;

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

    vram_y += SCREEN_REAL_WIDTH;

    if (yy == (TILE_SIZE - 1)) {
      n_y += SCREEN_COLUMNS;
    }
  }
}

void read_commands() {
  byte* pgmem = (byte*) &gmem.nametables[0][0][0];
  byte* poam = (byte*) &oam[0];

  dmaq_curr = 0;

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

      // Command is a read

      DDRC = 0b11111111;

      // Process the command

      switch (addr) {
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

      // Command is a write

      DDRC = 0b00000000;
      while (!(PINB & PIN_CLOCK))
      {
        ; // wait to receive the data
      }
      const byte data = PINC;

      // Process the command

      switch (addr) {
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
          dmaq[dmaq_curr].addr = dma_addr;
          dmaq[dmaq_curr++].type = data;
          break;
      }
    }

    while (!(PINB & PIN_ENABLE))
    {
      ; // wait to the end of the command
    }
  }

  if (dmaq_curr > 0) {
    dma_info.state = DMA_INIT;
    dma_info.index = 0;
    status |= STATUS_DMA;
  }
}
