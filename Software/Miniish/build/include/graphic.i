mget_rom
; Gets the sprite number assigned to a cell on the rom map.
;
; args
; ----
; r0: The column coordinate of the cell.
; r1: The row coordinate of the cell.
;
; notes
; -----
; N/A
;
 ;r5:r6=map+(r1/8)*32
 phy
 lda r1
 and #%11111000
 asl
 asl
 sta r5
 lda r1
 lsr
 lsr
 lsr
 lsr
 lsr
 lsr
 clc
 adc #>map
 sta r6
 ;r7=r0/8
 lda r0
 lsr
 lsr
 lsr
 sta r7
 ;return map[r5:r6][r7]
 ldy r7
 lda (r5),y
 ply
 rts

mget
; Gets the sprite number assigned to a cell on the map.
;
; args
; ----
; r0: The column coordinate of the cell.
; r1: The row coordinate of the cell.
;
; notes
; -----
; N/A
;
 lda r1
 lsr
 lsr
 lsr
 sta ppu_mapadr
 lda r0
 lsr
 lsr
 lsr
 sta ppu_mapadr
 lda ppu_mapdat
 rts
 
mset
; Set a cell on the map to a new sprite number.
;
; args
; ----
; r0: The column coordinate of the cell.
; r1: The row coordinate of the cell.
; r2: The new sprite number to store.
;
; notes
; -----
; N/A
;
 ;r5:r6=map_start+(r1/8)*32
 lda r1
 lsr
 lsr
 lsr
 sta ppu_mapadr
 lda r0
 lsr
 lsr
 lsr
 sta ppu_mapadr
 lda r2
 sta ppu_mapdat
 rts
 
; vim:syntax=asmM6502
