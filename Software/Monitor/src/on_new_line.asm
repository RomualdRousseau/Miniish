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
    ; else digit
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
    lda #4
    sta state
    jmp on_new_line
    ; check if space
L10:cmp #' '
    bne L11
    lda #4
    sta state
    inc buf_start
    jmp on_new_line
    ; check if range
L11:cmp #'.'
    bne L12
    lda #2
    sta state
    lda #0
    sta mem_end
    sta mem_end + 1
    inc buf_start
    jmp on_new_line
    ; check if write
L12:cmp #':'
    bne L13
    lda #3
    sta state
    inc buf_start
    jmp on_new_line
    ; check if run
L13:cmp #'R'
    bne L14
    lda #6
    sta state
    inc buf_start
    jmp on_new_line

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

    lda r0
    sta mem_start
    sta mem_end
    lda r1
    sta mem_start + 1
    sta mem_end + 1

    inc buf_start
    jmp on_new_line

state_2:
    ; check buffer end
    cpy buf_end
    bne L20
    lda #4
    sta state
    jmp on_new_line
    ; check if space
L20:cmp #' '
    bne L21
    lda #4
    sta state
    inc buf_start
    jmp on_new_line

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

    lda r0
    sta mem_end
    lda r1
    sta mem_end + 1

    inc buf_start
    jmp on_new_line

state_3:
    ; check buffer end
    cpy buf_end
    bne L30
    lda #5
    sta state
    jmp on_new_line
    ; check if space
L30:cmp #' '
    bne L31
    lda #5
    sta state
    inc buf_start
    jmp on_new_line

    ; Convert hex to byte
L31:jsr xtob
    sta r0

    lda mem_val
    asl
    asl
    asl
    asl
    clc
    adc r0
    sta mem_val

    inc buf_start
    jmp on_new_line

state_4:
    ; r4:r5 = mem_start
    lda mem_start
    sta r4
    lda mem_start + 1
    sta r5

    ; select output as UART
L40:lda #dev_uart
    sta r0

    ; print the address
    lda r5
    sta r1
    jsr print_hex
    lda r4
    sta r1
    jsr print_hex

    ; print a separator
    lda #':'
    sta r1
    jsr put_char
    lda #' '
    sta r1
    jsr put_char

    ; print the hex value at the address
    lda (r4)
    sta r1
    jsr print_hex

    ; print a separator
    lda #' '
    sta r1
    jsr put_char

    ; print the ascii value at the address
    lda (r4)
    sta r1
    jsr put_char

    ; print a line return
    lda #'\r'
    sta r1
    jsr put_char
    lda #'\n'
    sta r1
    jsr put_char

    ; r2:r3 = mem_end + 1
    lda mem_end
    sta r0
    lda mem_end + 1
    sta r1
    jsr inc_16
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
    lda r0
    sta r4
    lda r1
    sta r5

    ; loop if r0:r1 != r2:r3
    jsr cmp_16
    beq L41
    jmp L40

    ; check if end of string
L41:ldy buf_start
    cpy buf_end
    beq L42
    lda #0
    sta state
    jmp on_new_line
L42:rts

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