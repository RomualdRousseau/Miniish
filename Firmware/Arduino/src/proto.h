#ifndef PROTO_H
#define PROTO_H

#define CHANNELS 16
#define RESOLUTION 11
#define HEADER_MAGIC 0x0F

typedef struct
{
    uint8_t header;
    uint8_t data[(CHANNELS * RESOLUTION) / sizeof(uint8_t)];
    uint8_t flag;
    uint8_t footer;
} packet_t;

extern const packet_t *proto_encode_packet(const uint16_t *channels, packet_t *packet);

#endif