 .include "sym.i"

 .dsect
 .org zero_user ; zero ========
timer .byte $00
 .dend

 .org code_user ; code ========

init
 ; print message1 at (0, 1)
 lda #%10010100
 jsr lcd_send_cmd
 lda #<message
 sta r0
 lda #>message
 sta r0+1
 jsr lcd_print
 ; init and install timer
 lda #0
 sta timer
 lda #%11000000
 sta ier
 lda #%01000000
 sta acr
 lda #$ff
 sta t1ll
 lda #$ff
 sta t1ch
 cli
 rts

update
 ; print timer values
 jsr lcd_home
 lda #%11000000
 jsr lcd_send_cmd
 lda timer
 jsr lcd_print_byte
 rts

irq0_func
 bit t1cl
 inc timer
 plx
 rti

irq1_func
irq2_func
irq3_func
irq4_func
irq5_func
irq6_func
 plx
nmi_func
 rti

 .org data_user ; data ========
message
 .asciiz "i am xiaoniuniu"
