#include <stdio.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>

#include "uart.h"

#define UART_BAUD_SELECT(baudRate) ((F_CPU) / ((baudRate) * 16UL) - 1)
#define UART_BAUD_SELECT_DOUBLE_SPEED(baudRate) ((F_CPU) / ((baudRate) * 8UL) - 1)

FILE uart_out = FDEV_SETUP_STREAM(uart_putc_f, NULL, _FDEV_SETUP_RW);

void uart_init(const uint32_t baudrate)
{
    uint16_t bps;
    if (baudrate < 115200) {
        bps = UART_BAUD_SELECT(baudrate);
    }
    else {
        bps = UART_BAUD_SELECT_DOUBLE_SPEED(baudrate);
        UCSR0A = (1 << U2X0);
    }
    
    // Set Baud Rate
    UBRR0H = (uint8_t)((bps >> 8) & 0xFF);
    UBRR0L = (uint8_t)(bps & 0xFF);

    /* Set frame format: asynchronous, 8data, no parity, 1stop bit */
    UCSR0C = (0 << UMSEL00) | (0 << UPM00) | (0 << USBS0) | (3 << UCSZ00);

    /* Enable USART receiver and transmitter */
    UCSR0B = (1 << RXEN0) | (1 << TXEN0);
}

void uart_set_stdout(void)
{
    stdout = &uart_out;
}

const uint8_t uart_available(void)
{
    return ((UCSR0A & (1 << RXC0)) == 0) ? 0 : 1;
}

const uint8_t uart_getc(void)
{
    //while ((UCSR0A & (1 << RXC0)) == 0); // Do nothing until UDR is ready
    return UDR0;
}

void uart_putc(const uint8_t data)
{
    while ((UCSR0A & (1 << UDRE0)) == 0); // Do nothing until UDR is ready
    UDR0 = data;
}

int uart_putc_f(char c, FILE *stream)
{
    uart_putc(c);
    return 0;
}

void uart_puts(const char *s)
{
    while (*s)
    {
        uart_putc(*s++);
    }
}

void uart_puts_p(const char *progmem_s)
{
    register char c;
    while ((c = pgm_read_byte(progmem_s++)))
    {
        uart_putc(c);
    }
}
