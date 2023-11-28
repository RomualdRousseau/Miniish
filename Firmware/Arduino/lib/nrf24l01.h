#ifndef _NRF24L01_H_
#define _NRF24L01_H_

#include <avr/io.h>

// TODO: Setup right pins
// CE and CSN port definitions
#define NRF24L01_DDR DDRB
#define NRF24L01_PORT PORTB
#define NRF24L01_CE PB0
#define NRF24L01_CSN PB1

// CE and CSN functions
#define nrf24l01_CSNhi NRF24L01_PORT |= (1 << NRF24L01_CSN);
#define nrf24l01_CSNlo NRF24L01_PORT &= ~(1 << NRF24L01_CSN);
#define nrf24l01_CEhi NRF24L01_PORT |= (1 << NRF24L01_CE);
#define nrf24l01_CElo NRF24L01_PORT &= ~(1 << NRF24L01_CE);

// power setup
#define NRF24L01_RF24_PA_MIN 1
#define NRF24L01_RF24_PA_LOW 2
#define NRF24L01_RF24_PA_HIGH 3
#define NRF24L01_RF24_PA_MAX 4

// speed setup
#define NRF24L01_RF24_SPEED_250KBPS 1
#define NRF24L01_RF24_SPEED_1MBPS 2
#define NRF24L01_RF24_SPEED_2MBPS 3

// crc setup
#define NRF24L01_RF24_CRC_DISABLED 1
#define NRF24L01_RF24_CRC_8 2
#define NRF24L01_RF24_CRC_16 3

// transmission channel
#define NRF24L01_CH 76

// auto retransmit delay and count
#define NRF24L01_RETR (0b0100 << NRF24L01_REG_ARD) | (0b0111 << NRF24L01_REG_ARC) // 1500uS, 15 times

// address size
#define NRF24L01_ADDRSIZE 5

// address size
#define NRF24L01_PAYLOAD 32

extern void nrf24l01_init();
extern void nrf24l01_set_pa_level(const uint8_t level);
extern void nrf24l01_set_data_rate(const uint8_t speed);
extern void nrf24l01_set_crc_length(const uint8_t crc);

extern void nrf24l01_open_reading_pipe(const uint8_t pipe, const uint8_t *addr);
extern void nrf24l01_start_listening();
extern const uint8_t nrf24l01_available(uint8_t *pipe);
extern void nrf24l01_read(uint8_t *data, const uint8_t size);

extern void nrf24l01_open_writing_pipe(const uint8_t *addr);
extern void nrf24l01_stop_listening();
extern const uint8_t nrf24l01_write(const uint8_t *data, const uint8_t size);

#endif
