; audio.i

sound_load
 cmp #-1
 beq sound_load_done
 ; x = a * 16 + (timer % 4) * 4
 asl
 asl
 asl
 asl
 sta r1
 lda timer
 and #%00000011
 asl
 asl
 ora r1
 tax
 ; load wave if any
 ldy #0
 lda sound,x
 cmp #-1
 beq sound_load_done
 lsr
 lsr
 lsr
 lsr
 sta (apu_ptr),y
 ; load envelope
 ldy #1
 lda sound,x
 and #$0f
 sta (apu_ptr),y
 ; load length
 ldy #2
 lda sound+1,x
 sta (apu_ptr),y
 ; load modulation
 ldy #3
 lda sound+2,x
 sta (apu_ptr),y
 ; load note
 ldy #4
 lda sound+3,x
 sta (apu_ptr),y
sound_load_done
 rts
