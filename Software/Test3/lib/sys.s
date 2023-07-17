delay:
; Delay by A milliseconds
;
; args
; ----
; A : The number of milliseconds to delay.
; 
; notes
; -----
; N/A
;
 jsr delay_1ms
 sbc #1
 bne delay
 rts

delay_1ms:
; Delay by 1 millisecond.
;
; args
; ----
; N/A
; 
; notes
; -----
; This is a rough estimate based on the assertion of the CPU speed of 1MHz and 
; the number of cycles.
;
 pha
 lda #100
delay_1ms_loop:
 nop
 nop
 nop
 sbc #1
 bne delay_1ms_loop
 pla
 rts
 
memset:
; Sets the first Y bytes of the block of memory pointed by r0:r1 to the
; specified value A.
;
; args
; ----
; r0:r1 : This is a pointer to the block of memory to fill.
; A : This is the value to be set.
; Y : This is the number of bytes to be set to the value.
; 
; notes
; -----
; Setting the value 0 to r3 will fill an entire block of 256 bytes
;
 sta (r0),y
 iny
 bne memset
 rts

; vim:syntax=asm
