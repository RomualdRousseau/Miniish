class DMA_t
{
  public:
    void init() {
      memset(dma_queue, 0, DMAQ_COUNT * sizeof(dma_queue_t));
    }

    void transfer();
    
    void start_first_request() {
      state = DMA_START;
      index = 0;
      status |= STATUS_DMA;
    }

    void start_next_request() {
      state = DMA_START;
      index++;
      if (index >= dma_curr) {
        status &= ~STATUS_DMA;
      }
    }

  private:
    void copy_from_ROM(void* dest, unsigned int addr, size_t m);

    byte state;
    byte index;
    word source;
    byte* destination;
    word size_curr;
    word size_total;
};
DMA_t DMA;

void DMA_t::transfer() {
  const byte base = control & CONTROL_BASE;
  const dma_queue_t* pdmaq = &dma_queue[this->index];

  // Acquire the Address and Data Bus

  DDRA = 0b11111111;
  DDRD = 0b11111111;

  switch (state) {

    case DMA_START:

      // Prepare dma transfer

      state = DMA_TRANSFER;
      source = pdmaq->addr;
      size_curr = 0;

      // Setup destination memory

      switch (pdmaq->type) {

        case DMA_NAMETABLE:
          destination = &gmem.nametables[base][0][0];
          size_total = NAMETABLE_SIZE;
          break;

        case DMA_ATTRIBUTE:
          destination = &gmem.attributes[base][0][0];
          size_total = ATTRIBUTE_SIZE;
          break;

        case DMA_PALETTE:
          destination = &gmem.palettes[0][0];
          size_total = PALETTES_SIZE;
          break;

        case DMA_PATTERN:
          destination = &gmem.patterns[0][0];
          size_total = PATTERNS_SIZE;
          break;

        default:

          // If unknown type of transfer, just skip it

          start_next_request();

          // Release the Address and Data Bus

          DDRA = 0b00000000;
          DDRD = 0b00000000;

          return;
      }

    // Do not break here to avoid one frame lost

    case DMA_TRANSFER:

      // Transfer current chunk of DMA_CHUNK_SIZE bytes

      copy_from_ROM(
        destination + size_curr,
        source + size_curr,
        min(DMA_CHUNK_SIZE, size_total - size_curr));

      // Prepare next chunk

      size_curr += DMA_CHUNK_SIZE;
      if (size_curr >= size_total) {

        // Prepare next dma transfer

        start_next_request();
      }
      break;
  }

  // Release the Address and Data Bus

  DDRA = 0b00000000;
  DDRD = 0b00000000;
}

void DMA_t::copy_from_ROM(void* dest, unsigned int addr, size_t len) {
  byte* curr = (byte*) dest;
  byte* end = curr + len;

  for (; curr < end; curr++, addr++) {
    PORTA = addr >> 8;
    PORTD = addr;

    PORTB &= ~PIN_RROM;

    asm volatile("nop\n");
    asm volatile("nop\n");
    asm volatile("nop\n");
    asm volatile("nop\n");
    asm volatile("nop\n");

    *curr = PINC;

    PORTB |= PIN_RROM;
  }
}
