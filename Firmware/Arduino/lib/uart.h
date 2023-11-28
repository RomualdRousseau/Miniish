#ifndef UART_H
#define UART_H

#define UART_BAUD_SELECT(baudRate) ((F_CPU) / ((baudRate) * 16UL) - 1)
#define UART_BAUD_SELECT_DOUBLE_SPEED(baudRate) ((F_CPU) / ((baudRate) * 8UL) - 1)

#define uart_puts_P(__s) uart_puts_p(PSTR(__s))

extern void uart_init(const uint32_t baudrate);
extern const uint8_t uart_available(void);
extern const uint8_t uart_getc(void);
extern void uart_putc(const uint8_t data);
extern void uart_puts(const char *s);
extern void uart_puts_p(const char *s);

#endif
