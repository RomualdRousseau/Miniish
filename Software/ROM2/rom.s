DDRB = $7002
PORTB = $7000
 
  .org $8000

setup:  
  jsr init_leds

loop:  
  
  jsr display_pattern1
  jsr delay_1s
  
  jsr display_pattern2
  jsr delay_1s
  
  lda #%01010101
  sta $7401
   
  jmp loop
  
init_leds:
  lda #%11111111
  sta DDRB
  rts
  
display_pattern1:
  lda #%01010101
  sta PORTB
  rts
  
display_pattern2:
  lda #%10101010
  sta PORTB
  rts

delay_1s:
  pha
  lda #10
delay_1s_loop:
  jsr delay_100ms
  sbc #1
  bne delay_1s_loop
  pla
  rts
  
delay_100ms:
  pha
  lda #100
delay_100ms_loop:
  jsr delay_1ms
  sbc #1
  bne delay_100ms_loop
  pla
  rts
  
delay_1ms:
  pha
  lda #100
delay_1ms_loop:
  nop
  nop
  nop
  sbc #1
  bne delay_1ms_loop
  pla
  rts
  
  .org $FFFC
  .word setup
  .word $0000

