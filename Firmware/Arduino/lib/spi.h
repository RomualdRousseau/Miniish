#ifndef _SPI_H_
#define _SPI_H_

#define SPI_DDR DDRB
#define SPI_PORT PORTB
#define SPI_MISO PB4
#define SPI_MOSI PB3
#define SPI_SCK PB5
#define SPI_SS PB2

extern void spi_init();

extern const uint8_t spi_writereadbyte(const uint8_t data);

#endif
