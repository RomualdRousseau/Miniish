#include "common.h"
#include "util.h"
#include "proto.h"

const packet_t *proto_encode_packet(const uint16_t *channels, packet_t *packet)
{
    packet->header = HEADER_MAGIC;
    packet->flag = 0;

    uint8_t sum = packet->header + packet->flag;
    uint8_t off = 0;
    for (int i = 0; i < CHANNELS; i++)
    {
        for (int j = 0; j < RESOLUTION; j++)
        {
            const uint8_t val = (channels[i] >> j) & 0x01;
            array_set_bit(packet->data, off, val);
            sum += val;
            off += 1;
        }
    }

    packet->footer = sum;

    return packet;
}