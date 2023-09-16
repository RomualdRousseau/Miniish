ppu_ctrl   = port_ppu+$00
ppu_status = port_ppu+$01
ppu_mapadr = port_ppu+$02
ppu_mapdat = port_ppu+$03
ppu_scroll = port_ppu+$04
ppu_dmaspr = port_ppu+$10
ppu_dmamap = port_ppu+$11
ppu_dmaoam = port_ppu+$12

ppu_init
; Initialize the PPU.
;
; args
; ----
; N/A
; 
; notes
; -----
; The different memories and registers are set to 0 and wait for the PPU to be
; ready
;
 ; set ppu_retr to 0
 lda #0
 sta ppu_retr
 ; clear OAM data to 0
 lda #<oam_start
 sta r0
 lda #>oam_start
 sta r0+1
 lda #0
 ldy #0
 jsr memset
 ; wait PPU to be ready
ppu_init_wait
 lda ppu_status
 and #%00000001
 beq ppu_init_wait
 rts

ppu_start
; Start the PPU handler.
;
; args
; ----
; N/A
; 
; notes
; -----
; After this setting, the PPU will generates NMI at each vertical retrace.
;
 lda #%11100000
 sta ppu_ctrl
 rts
 
ppu_wait_nmi:
; PPU wait for NMI.
;
; args
; ----
; N/A
; 
; notes
; -----
; The handler will be called at each vertical retrace (60Hz).
;
; The OAM data are also updated to the PPU.
;
 lda ppu_retr
not_yet
 cmp ppu_retr
 beq not_yet
 ; update OAM and MAP
 lda #>oam_start
 sta ppu_dmaoam
 ;lda #>map_start
 ;sta ppu_dmamap
 rts

nmi_func
; PPU handler to update and draw the game.
;
; args
; ----
; N/A
; 
; notes
; -----
; The handler will be called at each vertical retrace (60Hz)
;
 inc ppu_retr
 rti

; vim:syntax=asmM6502
