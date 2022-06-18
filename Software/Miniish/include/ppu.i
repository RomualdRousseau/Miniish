ppu_ctrl    = port_ppu + $00
ppu_status  = port_ppu + $01
ppu_scroll  = port_ppu + $04
ppu_dmaspr  = port_ppu + $10
ppu_dmamap  = port_ppu + $11
ppu_dmaoam  = port_ppu + $12

ppu_init
 ; set retraces to 0
 lda #0
 sta retraces
 ; clear oam data
 lda #<oam_start
 sta src_ptr
 lda #>oam_start
 sta src_ptr+1
 lda #0
 ldy #255
 jsr mem_set
 ; wait PPU to be ready
ppu_init_wait
 lda ppu_status
 and #%00000001
 beq ppu_init_wait
 rts

ppu_start
 ; start PPU handler
 lda #%11100000
 sta ppu_ctrl
 rts
 
nmi_func
 pha
 phx
 phy
 lda retraces
 and #1
 bne nmi_done
 jsr update
nmi_draw
 lda retraces
 and #15
 bne nmi_flush
 jsr draw
nmi_flush
 lda #>oam_start
 sta ppu_dmaoam
nmi_done
 inc retraces
 ply
 plx
 pla
 rti
