#ifndef UART_H
#define UART_H

extern void uart_init(const uint32_t baudrate);
extern void uart_set_stdout(void);

extern const uint8_t uart_available(void);
extern const uint8_t uart_getc(void);

extern void uart_putc(const uint8_t data);
extern int uart_putc_f(char data, FILE *stream);

extern void uart_puts(const char *s);
extern void uart_puts_p(const char *s);
#define uart_puts_P(__s) uart_puts_p(PSTR(__s))

#endif
