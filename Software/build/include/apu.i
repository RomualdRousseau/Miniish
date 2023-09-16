apu_ctrl   = port_apu+$00
apu_status = port_apu+$01
apu_snd0   = port_apu+$10
apu_snd1   = port_apu+$11
apu_snd2   = port_apu+$12
apu_snd3   = port_apu+$13

apu_init
 ; set apu_tmrs to 0
 lda #0
 sta apu_tmr1
 sta apu_tmr2
 ; disable sound channel
 lda #-1
 sta apu_sfx
 ; set channel array
 lda #>apu_snd0
 sta apu_ptr+1
 lda #<apu_snd0
 sta apu_ptr
 ; wait APU to be ready
apu_init_wait
 lda apu_status
 and #%00000001
 beq apu_init_wait
 rts

apu_play
 ; start playing song
 lda #0
 sta apu_ctrl
 rts

apu_play_sfx
 sta apu_sfx
 rts

irq0_func
 phy
 pha
 lda r1
 pha
play_music
 ; load current song pattern in x
 lda apu_tmr1
 and #%11111000
 lsr
 tax
 lda song,x
 ; loop song if reached the end
 cmp #-1
 bne load_channel_0
 lda #0
 sta apu_tmr1
 tax
load_channel_0
 lda song+1,x
 cmp #-1
 beq load_channel_1
 ldy #0
 jsr apu_load_snd
load_channel_1
 lda song+2,x
 cmp #-1
 beq load_channel_2
 ldy #1
 jsr apu_load_snd
load_channel_2
 lda song+3,x
 cmp #-1
 beq load_channel3
 ldy #2
 jsr apu_load_snd
load_channel3
 lda apu_sfx
 cmp #-1
 beq play_channels
 ldy #3
 jsr apu_load_sfx
 bne play_channels_and_sfx
 lda #-1
 sta apu_sfx
 lda #0
 sta apu_tmr2
play_channels_and_sfx
 lda #3
 sta apu_ctrl
 inc apu_tmr2
 jmp play_done
play_channels
 lda #24
 sta apu_ctrl
play_done
 inc apu_tmr1
 pla
 sta r1
 pla
 ply
 plx
 rti
 
apu_load_snd
 phx
 ;load current note in x
 ;x = a * 16 + (apu_tmr1 % 8) * 2
 asl
 asl
 asl
 asl
 sta r1
 lda apu_tmr1
 and #%00000111
 asl
 ora r1
 tax
 ;if(sound[x] <> -1){
 lda sound,x
 cmp #-1
 beq apu_load_snd_done
 ;load pitch
 ;apu_ptr[y]=sound[x+1]
 lda sound+1,x
 sta (apu_ptr),y
 ;load wave and effect
 ;apu_ptr[y]=sound[x]
 lda sound,x
 sta (apu_ptr),y
 ;}
apu_load_snd_done
 plx
 rts

apu_load_sfx
 phx
 ;load current note in x
 ;x = a * 16 + (apu_tmr2 % 8) * 2
 asl
 asl
 asl
 asl
 sta r1
 lda apu_tmr2
 and #%00000111
 asl
 ora r1
 tax
 ;if(sound[x] <> -1){
 lda sound,x
 cmp #-1
 beq apu_load_sfx_done
 ;load pitch
 ;apu_ptr[y]=sound[x+1]
 lda sound+1,x
 sta (apu_ptr),y
 ;load wave and effect
 ;apu_ptr[y]=sound[x]
 lda sound,x
 sta (apu_ptr),y
 ;return 1
 plx
 lda #1
 rts
 ;}
apu_load_sfx_done
 ;return 0
 plx
 lda #0
 rts

; vim:syntax=asmM6502
