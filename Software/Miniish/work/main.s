ZERO_START = $0000
STCK_START = $0100
OAM_START  = $1000
CODE_START = $8000
DATA_START = $A000
INTE_START = $FFEA

 .dsect
 .org ZERO_START ; ZERO ========
LCD_PTR   .word $0000
JOYPAD    .byte $00
TIMER     .byte $00
COUNTER   .byte $00
NMI_STATE .byte $00
R1        .byte $00
R2        .byte $00
R3        .byte $00
R4        .byte $00
R5        .byte $00
 .dend

 .dsect ; OAM ==================
 .org OAM_START
HERO      .byte $00,$00,$00,$00
COIN      .byte $00,$00,$00,$00
 .dend

 .org CODE_START ; CODE ========
MAIN
 ldx #$FF ; STACK SIZE
 txs
 jmp SETUP

 ; IMPORTS =====================
 .include "sys.i"
 .include "lcd.i"
 .include "joypad.i"

SETUP

 ; INIT VARIABLES

 lda #0
 sta TIMER

 lda #0
 sta COUNTER

 lda #0
 sta NMI_STATE

 ; INIT LCD

 jsr LCD_INIT
 jsr LCD_CLEAR

 ; PRINT MESSAGE1 AT (0, 1)

 lda #%10010100
 jsr LCD_SEND_CMD
 lda #<MESSAGE1
 sta LCD_PTR
 lda #>MESSAGE1
 sta LCD_PTR + 1
 jsr LCD_PRINT

 ; INIT JOYPAD

 jsr JOYPAD_INIT

 ; INSTALL TIMER

 lda #%11000000
 sta IER
 lda #%01000000
 sta ACR
 lda #$FF
 sta T1LL
 lda #$FF
 sta T1CH
 cli

LOOP
 jsr JOYPAD_READ

 ; PRINT JOYPAD AND TIMER VALUES

 jsr LCD_HOME
 lda JOYPAD
 jsr LCD_PRINT_BYTE

 lda #%11000000
 jsr LCD_SEND_CMD

 lda TIMER
 jsr LCD_PRINT_BYTE

 lda #' '
 jsr LCD_SEND_CHAR

 lda COUNTER
 jsr LCD_PRINT_BYTE

 ; CHECK IF START PRESSED

 lda JOYPAD
 and #%00010000
 beq LOOP

 ; PRINT MESSAGE2 AT (0, 3)

 lda #%11010100
 jsr LCD_SEND_CMD
 lda #<MESSAGE2
 sta LCD_PTR
 lda #>MESSAGE2
 sta LCD_PTR + 1
 jsr LCD_PRINT

 jmp LOOP

IRQ0_FUNC
 plx
 rti

IRQ1_FUNC
 bit T1CL
 inc TIMER
 plx
 rti

NMI_FUNC
 pha
 lda NMI_STATE
 cmp #0
 beq NMI_INIT
 cmp #1
 beq NMI_DRAW
 jmp NMI_DONE
NMI_INIT
 ; INIT HERO
 lda #16
 sta HERO
 lda #0
 sta HERO + $01
 lda #0
 sta HERO + $02
 lda #0
 sta HERO + $03
 ; init coin
 lda #18
 sta COIN
 lda #8*8
 sta COIN + $01
 lda #12*8
 sta COIN + $02
 lda #0
 sta COIN + $03
 ; load assets in ppu
 lda #$a0
 sta PORT_PPU + $03
 lda #$00
 sta PORT_PPU + $04
 lda #$c0
 sta PORT_PPU + $03
 lda #$20
 sta PORT_PPU + $04
 ; next state
 lda #1
 sta NMI_STATE
 jmp NMI_DONE
NMI_DRAW
 inc COUNTER
 lda COUNTER
 and #3
 bne NMI_DONE
 ; update hero
 lda JOYPAD
 cmp #0
 beq HERO_UPDATE
HERO_KEYUP
 lda JOYPAD
 and #%00001000
 beq HERO_KEYDOWN
 dec HERO + $02
HERO_KEYDOWN
 lda JOYPAD
 and #%00000100
 beq HERO_KEYLEFT
 inc HERO + $02
HERO_KEYLEFT
 lda JOYPAD
 and #%00000010
 beq HERO_KEYRIGHT
 dec HERO + $01
HERO_KEYRIGHT
 lda JOYPAD
 and #%00000001
 beq HERO_UPDATE
 inc HERO + $01
HERO_UPDATE
 lda COUNTER
 and #15
 bne ALL_UPDATE
 lda HERO
 clc
 adc #1
 and #%11111101
 sta HERO
COIN_UPDATE
 lda COIN
 clc
 adc #1
 cmp #20
 bne COIN_NEXT_ANIM
 lda #18
COIN_NEXT_ANIM
 sta COIN
ALL_UPDATE
 ;update oam in ppu
 lda #$10
 sta PORT_PPU + $03 
 lda #$24
 sta PORT_PPU + $04
NMI_DONE
 pla
 rti

 .org DATA_START ; DATA ========
SPRITES
 .incbin "sprites.dat"
MAP
 .incbin "map.dat"
MESSAGE1
 .asciiz "I am XiaoNiuNiu"
MESSAGE2
 .asciiz "Wo ai ni (521 1314)"

 .org INTE_START ; INT VECTORS =
TABLE_IRQ
 .word IRQ0_FUNC
 .word IRQ1_FUNC
 .word $0000
 .word $0000
 .word $0000
 .word $0000
 .word IRQ1_FUNC
 .word IRQ0_FUNC
TABLE_VEC
 .word NMI_FUNC
 .word MAIN
 .word IRQ_FUNC
