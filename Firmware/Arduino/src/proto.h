#ifndef PROTO_H
#define PROTO_H

#define CHANNELS 16
#define RESOLUTION 11
#define HEADER_MAGIC 0x0F

typedef struct
{
    uint8_t header;
    uint8_t data[(CHANNELS * RESOLUTION) / 8];
    uint8_t flag;
    uint8_t footer;
} packet_t;

extern void proto_init(uint16_t *channels);

extern const packet_t *proto_encode_packet(const uint16_t *channels, packet_t *packet);

#endif