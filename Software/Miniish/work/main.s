zero_start = $0000
stck_start = $0100
oam_start  = $1000
map_start  = $1100
code_start = $8000
data_start = $a000
inte_start = $ffea

 .dsect
 .org zero_start ; zero ========
lcd_ptr   .word $0000
src_ptr   .word $0000
dst_ptr   .word $0000
retraces  .byte $00
joypad    .byte $00
timer     .byte $00
r1        .byte $00
r2        .byte $00
r3        .byte $00
r4        .byte $00
r5        .byte $00

 .org oam_start ; oam ==================
hero      .byte $00,$00,$00,$00
coin      .byte $00,$00,$00,$00
 .dend

 .org code_start ; code ========
main
 ldx #$ff ; stack size
 txs
 jmp setup

 ; includes =====================
 .include "sys.i"
 .include "lcd.i"
 .include "joypad.i"
 .include "map.i"
 .include "hero.i"

init
 jsr map_init
 jsr hero_init
 ; load assets in ppu
 lda #>sprites
 sta ppu_dmaspr
 lda #>map
 sta ppu_dmamap
 rts

update
 jsr map_update
 jsr hero_update
 rts

draw
 jsr map_draw
 jsr hero_draw
 rts

setup
 ; init variables
 lda #0
 sta retraces
 lda #0
 sta timer
 lda #<oam_start
 sta src_ptr
 lda #>oam_start
 sta src_ptr+1
 ldy #0
 lda #0
mem_set
 sta (src_ptr),y
 iny
 bne mem_set
 ; init lcd
 jsr lcd_init
 jsr lcd_clear
 ; print message1 at (0, 1)
 lda #%10010100
 jsr lcd_send_cmd
 lda #<message1
 sta lcd_ptr
 lda #>message1
 sta lcd_ptr+1
 jsr lcd_print
 ; init joypad
 jsr joypad_init
 ; install timer
 lda #%11000000
 sta ier
 lda #%01000000
 sta acr
 lda #$ff
 sta t1ll
 lda #$ff
 sta t1ch
 cli
 ; init game
 jsr init
 ; start ppu
 lda #%11100000
 sta ppu_ctrl

loop
 jsr joypad_read
 ; print joypad and timer values
 jsr lcd_home
 lda joypad
 jsr lcd_print_byte
 lda #%11000000
 jsr lcd_send_cmd
 lda timer
 jsr lcd_print_byte
 lda #' '
 jsr lcd_send_char
 lda retraces
 jsr lcd_print_byte
 ; check if start pressed
 lda joypad
 and #%00010000
 beq loop
 ; print message2 at (0, 3)
 lda #%11010100
 jsr lcd_send_cmd
 lda #<message2
 sta lcd_ptr
 lda #>message2
 sta lcd_ptr+1
 jsr lcd_print
 jmp loop

irq0_func
 plx
 rti

irq1_func
 bit t1cl
 inc timer
 plx
 rti

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
 lda hero+$01
 clc
 sbc #3*8
 sta ppu_scroll
 lda #0
 sta ppu_scroll
 lda #>oam_start
 sta ppu_dmaoam
nmi_done
 inc retraces
 ply
 plx
 pla
 rti

 .org data_start ; data ========
sprites
 .incbin "sprites.dat"
map
 .incbin "map.dat"
message1
 .asciiz "i am xiaoniuniu"
message2
 .asciiz "wo ai ni (521 1314)"

 .org inte_start ; int vectors =
table_irq
 .word irq0_func
 .word irq1_func
 .word $0000
 .word $0000
 .word $0000
 .word $0000
 .word irq1_func
 .word irq0_func
table_vec
 .word nmi_func
 .word main
 .word irq_func
