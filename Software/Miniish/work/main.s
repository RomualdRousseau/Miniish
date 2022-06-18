zero_start = $0000
stck_start = $0100
oam_start  = $1000
code_start = $8000
data_start = $a000
inte_start = $ffea

 .dsect
 .org zero_start ; zero ========
lcd_ptr   .word $0000
apu_ptr   .word $0000
src_ptr   .word $0000
dst_ptr   .word $0000
retraces  .byte $00
timer     .byte $00
joypad    .byte $00
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
 .include "ppu.i"
 .include "apu.i"
 .include "lcd.i"
 .include "joypad.i"
 .include "map.i"
 .include "hero.i"
 .include "sketch.i"

setup
 ; init all libraries
 jsr ppu_init
 jsr apu_init
 jsr lcd_init
 jsr joypad_init
 ; init game
 jsr init
 ; start ppu retrace
 jsr ppu_start
 cli

loop
 jsr joypad_read
 jmp loop

 .org data_start ; data ========
sprites
 .incbin "sprites.dat"
map
 .incbin "map.dat"
song
 .incbin "music.dat"
sound
 .incbin "sound.dat"

 .org inte_start ; int vectors =
table_irq
 .word irq0_func
 .word $0000
 .word $0000
 .word $0000
 .word $0000
 .word $0000
 .word $0000
 .word $0000
table_vec
 .word nmi_func
 .word main
 .word irq_func
