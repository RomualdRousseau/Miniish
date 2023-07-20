    .include "miniish.inc"

    .global memset

    .section kernel

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
