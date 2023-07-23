    .include "miniish.inc"
    .include "stdio.inc"

    .global state, mem_start, mem_end, mem_val
    .global on_new_line

    .section data
    
state:
    .byte $00
mem_start:
    .word $0000
mem_end:
    .word $0000
mem_val:
    .byte $00

    .section text

on_new_line:
    ; load state in X
    lda state
    clc
    asl
    tax
    ; get next token in A
    ldy buf_start
    lda buf_data, y
    ; switch case
    ; A = token
    ; X = state
    ; Y = buf_start
    jmp (state_switch, x)

state_switch:
    .word state_0 ; ([.:R]|\x)?
    .word state_1 ; (\x+)?([.:R])?
    .word state_2 ; (\x+)?
    .word state_3 ; (\x+)?
    .word state_4 ; read from mem_start to mem_end
    .word state_5 ; write mem_val
    .word state_6 ; run

state_0:
    ; check buffer end
    cpy buf_end
    beq L00
    ; check if space
    cmp #' '
    beq L00
    ; check if range
    cmp #'.'
    beq L00
    ; check if write
    cmp #':'
    beq L00
    ; check if run
    cmp #'R'
    beq L00
    ; else start digit
    lda #0
    sta mem_start
    sta mem_start + 1
L00:lda #1
    sta state
    jmp on_new_line

state_1:
    ; check buffer end
    cpy buf_end
    bne L10
    dec buf_start
    lda #4
    jmp L15
    ; check if space
L10:cmp #' '
    bne L11
    lda #4
    jmp L15
    ; check if range
L11:cmp #'.'
    bne L12
    lda #0
    sta mem_end
    sta mem_end + 1
    lda #2
    jmp L15
    ; check if write
L12:cmp #':'
    bne L13
    lda #3
    jmp L15
    ; check if run
L13:cmp #'R'
    bne L14
    lda #6
    jmp L15
    ; Convert hex to byte
L14:jsr xtob
    sta r2
    ; mem_start = mem_start << 4 + R2
    lda mem_start
    sta r0
    lda mem_start + 1
    sta r1
    ldy #4
    jsr asl_16
    jsr adc_16
    ; save mem_start and meme_end
    lda r0
    sta mem_start
    sta mem_end
    lda r1
    sta mem_start + 1
    sta mem_end + 1
    ; go to next state
    lda #1
L15:sta state
    inc buf_start
    jmp on_new_line

state_2:
    ; check buffer end
    cpy buf_end
    bne L20
    dec buf_start
    lda #4
    jmp L22
    ; check if space
L20:cmp #' '
    bne L21
    lda #4
    jmp L22
    ; Convert hex to byte
L21:jsr xtob
    sta r2
    ; mem_end = mem_end << 4 + R2
    lda mem_end
    sta r0
    lda mem_end + 1
    sta r1
    ldy #4
    jsr asl_16
    jsr adc_16
    ; save mem_end
    lda r0
    sta mem_end
    lda r1
    sta mem_end + 1
    ; go to next state
    lda #2
L22:sta state
    inc buf_start
    jmp on_new_line

state_3:
    ; check buffer end
    cpy buf_end
    bne L30
    dec buf_start
    lda #5
    jmp L32
    ; check if space
L30:cmp #' '
    bne L31
    lda #5
    jmp L32
    ; Convert hex to byte
L31:jsr xtob
    sta r0
    ; mem_val = mem_val << 4 + R0
    lda mem_val
    asl
    asl
    asl
    asl
    clc
    adc r0
    sta mem_val
    ; go to next state
    lda #3
L32:sta state
    inc buf_start
    jmp on_new_line

state_4:
    ; select output as UART
    lda #dev_uart
    sta r0
    ; r4:r5 = mem_start
    lda mem_start
    sta r4
    lda mem_start + 1
    sta r5
    ; print the address
L40:lda r5
    sta r1
    jsr print_hex
    lda r4
    sta r1
    jsr print_hex
    ; print a separator
    lda #':'
    sta r1
    jsr put_char
    ; print space
L41:lda #' '
    sta r1
    jsr put_char
    ; print the hex value at the address
    lda (r4)
    sta r1
    jsr print_hex
    ; r2:r3 = mem_end + 1
    lda mem_end
    sta r0
    lda mem_end + 1
    sta r1
    jsr inc_16
    ; r2:r3 = r0:r1
    lda r0
    sta r2
    lda r1
    sta r3
    ; r4:r5 += 1
    lda r4
    sta r0
    lda r5
    sta r1
    jsr inc_16
    ; r4:r5 = r0:r1
    lda r0
    sta r4
    lda r1
    sta r5
    ; check if end of memory
    jsr cmp_16
    beq L42
    ; reselect output as UART
    lda #dev_uart
    sta r0
    ; emit new line mem_start module 8
    lda r4
    and #%00000111
    bne L41
    jsr print_ln
    jmp L40
    ; reselect output as UART
L42:lda #dev_uart
    sta r0
    jsr print_ln
    ; check if end of string
    ldy buf_start
    cpy buf_end
    beq L43
    lda #0
    sta state
    jmp on_new_line
L43:rts

state_5:
    ; write mem_val to the address
    lda mem_start
    sta r0
    lda mem_start + 1
    sta r1
    lda mem_val
    sta (r0)
    ; increment the address
    jsr inc_16
    lda r0
    sta mem_start
    lda r1
    sta mem_start + 1
    ; check if end of string
    ldy buf_start
    cpy buf_end
    beq L50
    lda #3
    sta state
    jmp on_new_line
L50:rts

state_6:
    jmp (mem_start)