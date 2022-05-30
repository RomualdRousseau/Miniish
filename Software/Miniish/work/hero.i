; hero.i

hero_init
 lda #16
 sta hero
 lda #3*8
 sta hero+$01
 lda #14*8
 sta hero+$02
 lda #0
 sta hero+$03
 rts

hero_update
 lda joypad
 ;cmp #0
 beq hero_update_done
hero_update_keyup
 lda joypad
 and #%00001000
 beq hero_update_keydown
 dec hero+$02
hero_update_keydown
 lda joypad
 and #%00000100
 beq hero_update_keyleft
 inc hero+$02
hero_update_keyleft
 lda joypad
 and #%00000010
 beq hero_update_keyright
 dec hero+$01
hero_update_keyright
 lda joypad
 and #%00000001
 beq hero_update_done
 inc hero+$01
hero_update_done
 rts

hero_draw
 lda hero
 clc
 adc #1
 cmp #18
 bne hero_draw_1
 lda #16
hero_draw_1
 sta hero
 rts
