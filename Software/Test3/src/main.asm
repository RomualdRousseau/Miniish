    .global main

    .section text

main:
    jsr setup
main_loop:
    jsr loop
    jmp main_loop
