; audio.i

sound_load
 cmp #-1
 beq sound_load_done
 ; x = a * 16 + (timer % 8) * 2
 asl
 asl
 asl
 asl
 sta r1
 lda timer
 and #%00000111
 asl
 ora r1
 tax
 lda sound+1,x
 cmp #0
 beq sound_load_done
 ; load wave
 ldy #0
 lda sound,x
 lsr
 lsr
 lsr
 lsr
 sta (apu_ptr),y
 ; load envelope
 ldy #1
 lda #1
 sta (apu_ptr),y
 ; load length
 ldy #2
 lda #127
 sta (apu_ptr),y
 ; load modulation
 ldy #3
 lda #64
 sta (apu_ptr),y
 ; load note
 ldy #4
 lda sound+1,x
 clc
 adc #32
 sta (apu_ptr),y
sound_load_done
 rts
