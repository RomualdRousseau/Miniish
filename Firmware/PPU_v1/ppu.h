class PPU_t
{
  public:
    void init() {}

    void do_instructions();
};
PPU_t PPU;

void PPU_t::do_instructions() {
  byte* pgmem = (byte*) &gmem.nametables[0][0][0];
  byte* poam = (byte*) &oam[0];

  dma_curr = 0;

  // Notify the CPU to start PPU instructions

  status |= STATUS_NMI;
  PORTB &= ~PIN_NMI;

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

      while (!(PINB & PIN_ENABLE))
      {
        ; // wait to the end of the command
      }
    
    } else {

      // Command is a write

      DDRC = 0b00000000;
      while (!(PINB & PIN_CLOCK))
      {
        ; // wait to receive the data
      }
      const byte data = PINC;

      while (!(PINB & PIN_ENABLE))
      {
        ; // wait to the end of the command
      }

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
          dma_queue[dma_curr].addr = dma_addr;
          dma_queue[dma_curr++].type = data;
          break;
      }
    }
  }

  if (dma_curr > 0) {
    DMA.start_first_request();
  }

  // Notify the CPU to stop PPU instructions

  PORTB |= PIN_NMI;
  status &= ~STATUS_NMI;
}
