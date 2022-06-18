; map.i

map_init
 rts

map_update
 lda hero+$01
 clc
 sbc #3*8
 sta ppu_scroll
 lda #0
 sta ppu_scroll
 rts

map_draw
 rts
