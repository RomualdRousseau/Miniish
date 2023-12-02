#ifndef NRF24_H
#define NRF24_H

extern void nrf24_init(const uint8_t* address);

extern void nrf24_write_async(const uint8_t *data, const uint8_t size);
extern void nrf24_write_wait();
extern void nrf24_write(const uint8_t *data, const uint8_t size);

#endif
