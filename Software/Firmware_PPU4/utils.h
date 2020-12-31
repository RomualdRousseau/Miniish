inline byte rom_read_byte(unsigned int addr) {
  PORTA = addr >> 8;
  PORTD = addr;
  PORTB &= ~PIN_RROM;
  asm volatile("nop\nnop\nnop\n");
  const byte data = PINC;
  PORTB |= PIN_RROM;
  return data;
}

void memcpy_R(void* dest, unsigned int addr, size_t m) {
  for(int i = 0; i < m; i++) {
    ((byte*) dest)[i] = rom_read_byte(addr + i);
  }
}

void memcpy_R_T(void* dest, unsigned int addr, size_t m, size_t n) {
  for(int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
      ((byte*) dest)[j * m + i] = rom_read_byte(addr + i * n + j);
    }
  }
}

void memcpy_P_T(void* dest, const void* src, size_t m, size_t n) {
  for(int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
      ((byte*) dest)[j * m + i] = pgm_read_byte(&((const byte*) src)[i * n + j]);
    }
  }
}
