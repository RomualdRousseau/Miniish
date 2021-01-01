void memcpy_R(void* dest, unsigned int addr, size_t m) { 
  byte* p = (byte*) dest;
  byte* e = p + m;
  
  for(;p < e; p++, addr++) {
    PORTA = addr >> 8;
    PORTD = addr;
    
    PORTB &= ~PIN_RROM;
    
    asm volatile("nop\n");
    asm volatile("nop\n");
    asm volatile("nop\n");
    asm volatile("nop\n");
    asm volatile("nop\n");

    *p = PINC;
    
    PORTB |= PIN_RROM;
  }
}
