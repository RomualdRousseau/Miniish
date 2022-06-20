collide
; Performs a collision check between a sprite and the map.
;
; args
; ----
; r0: The column coordinate (x) of the bounding box.
; r1: The row coordinate (y) of the bounding box.
; r2: The width (w) of the bounding box.
; r3: The height (h) of the bounding box.
; r4: The type of tile to hit.
;
; notes
; -----
; The sprite is represented by its bounding box (x, y, w, h) and will check
; the overlap with nearby tiles.

; The procedure returns 1 if the sprite overlaps a tile with the given flags,
; 0 otherwise.
;
 ;r0=r0+r2/2
 lda r2
 lsr
 clc
 adc r0
 sta r0
 ;r1=r1+r3/2
 lda r3
 lsr
 clc
 adc r1
 sta r1
 ;if(flags[mget(r0,r1)]<>r4) {
 jsr mget
 tax
 lda flags,x
 and r4
 beq collide_done
 ;return 1
 lda #1
 rts
 ;}
collide_done
 ;return 0
 lda #0
 rts

collide_right
; Performs a collision check on the right between a sprite and the map.
;
; args
; ----
; r0: The column coordinate (x) of the bounding box.
; r1: The row coordinate (y) of the bounding box.
; r2: The width (w) of the bounding box.
; r3: The height (h) of the bounding box.
; r4: The type of tile to hit.
;
; notes
; -----
; The sprite is represented by its bounding box (x, y, w, h) and will check
; the overlap with nearby tiles on the right.

; The procedure returns -1 if the sprite overlaps a tile with the given flags,
; 0 otherwise.
;
 ;r0+=r2
 lda r0
 clc
 adc r2
 sta r0
 ;if(flags[mget(r0,r1)]<>r4) {
 jsr mget
 tax
 lda flags,x
 and r4
 beq collide_right_if00
 ;return -1
 lda #-1
 rts
 ;}
collide_right_if00
 ;r1+=r3
 lda r1
 clc
 adc r3
 sta r1
 ;if(flags[mget(r0,r1)]<>r4) {
 jsr mget
 tax
 lda flags,x
 and r4
 beq collide_right_done
 ;return -1
 lda #-1
 rts
 ;}
collide_right_done
 ;return 0
 lda #0
 rts

collide_left
; Performs a collision check on the left between a sprite and the map.
;
; args
; ----
; r0: The column coordinate (x) of the bounding box.
; r1: The row coordinate (y) of the bounding box.
; r2: The width (w) of the bounding box.
; r3: The height (h) of the bounding box.
; r4: The type of tile to hit.
;
; notes
; -----
; The sprite is represented by its bounding box (x, y, w, h) and will check
; the overlap with nearby tiles on the left.

; The procedure returns 1 if the sprite overlaps a tile with the given flags,
; 0 otherwise.
;
 ;if(flags[mget(r0,r1)]<>r4) {
 jsr mget
 tax
 lda flags,x
 and r4
 beq collide_left_if00
 ;return 1
 lda #1
 rts
 ;}
collide_left_if00
 ;r1+=r3
 lda r1
 clc
 adc r3
 sta r1
 ;if(flags[mget(r0,r1)]<>r4) {
 jsr mget
 tax
 lda flags,x
 and r4
 beq collide_left_done
 ;return 1
 lda #1
 rts
 ;}
collide_left_done
 ;return 0
 lda #0
 rts

collide_top
; Performs a collision check on the top between a sprite and the map.
;
; args
; ----
; r0: The column coordinate (x) of the bounding box.
; r1: The row coordinate (y) of the bounding box.
; r2: The width (w) of the bounding box.
; r3: The height (h) of the bounding box.
; r4: The type of tile to hit.
;
; notes
; -----
; The sprite is represented by its bounding box (x, y, w, h) and will check
; the overlap with nearby tiles on the top.

; The procedure returns 1 if the sprite overlaps a tile with the given flags,
; 0 otherwise.
;
 ;if(flags[mget(r0,r1)]<>r4) {
 jsr mget
 tax
 lda flags,x
 and r4
 beq collide_top_if00
 ;return 1
 lda #1
 rts
 ;}
collide_top_if00
 ;r0+=r2
 lda r0
 clc
 adc r2
 sta r0
 ;if(flags[mget(r0,r1)]<>r4) {
 jsr mget
 tax
 lda flags,x
 and r4
 beq collide_top_done
 ;return 1
 lda #1
 rts
 ;}
collide_top_done
 ;return 0
 lda #0
 rts
 
collide_bottom
; Performs a collision check on the bottom between a sprite and the map.
;
; args
; ----
; r0: The column coordinate (x) of the bounding box.
; r1: The row coordinate (y) of the bounding box.
; r2: The width (w) of the bounding box.
; r3: The height (h) of the bounding box.
; r4: The type of tile to hit.
;
; notes
; -----
; The sprite is represented by its bounding box (x, y, w, h) and will check
; the overlap with nearby tiles on the bottom.

; The procedure returns -1 if the sprite overlaps a tile with the given flags,
; 0 otherwise.
;
 ;r1+=r3
 lda r1
 clc
 adc r3
 sta r1
 ;if(flags[mget(r0,r1)]<>r4) {
 jsr mget
 tax
 lda flags,x
 and r4
 beq collide_bottom_if00
 ;return -1
 lda #-1
 rts
 ;}
collide_bottom_if00
 ;r0+=r2
 lda r0
 clc
 adc r2
 sta r0
 ;if(flags[mget(r0,r1)]<>r4) {
 jsr mget
 tax
 lda flags,x
 and r4
 beq collide_bottom_done
 ;return -1
 lda #-1
 rts
 ;}
collide_bottom_done
 ;return 0
 lda #0
 rts
; vim:syntax=asmM6502
