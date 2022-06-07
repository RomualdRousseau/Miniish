; audio.i

sound_load
 phx
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
 lda sound,x
 cmp #-1
 beq sound_load_done
 ; load pitch
 lda sound+1,x
 sta (apu_ptr),y
 ; load wave and effect
 lda sound,x
 sta (apu_ptr),y
sound_load_done
 plx
 rts
