#ifndef SPI_H
#define SPI_H

extern void spi_init(void);

extern const uint8_t spi_transfer(const uint8_t send_data);

#endif