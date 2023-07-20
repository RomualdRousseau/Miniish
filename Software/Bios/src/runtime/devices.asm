    .include "miniish.inc"
    .include "stdio.inc"

    .global dev_table

    .dsect
    .org zero_start + $10

dev_table:
    .word $0000, $0000, $0000
    .word $0000, $0000, $0000
    .word $0000, $0000, $0000
    .word $0000, $0000, $0000

    .dend