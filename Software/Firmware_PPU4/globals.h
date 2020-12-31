// CONFIGURATION

#define SCREEN_COLUMNS       20
#define SCREEN_ROWS          12
#define SCREEN_BORDER        1
#define NAMETABLE_COUNT      2
#define PALETTE_COUNT        8
#define COLOR_PER_PALETTE    4
#define PATTERN_COUNT        64
#define OAM_COUNT            32
#define TILE_SIZE            8
#define TILE_PER_BLOCK       4
#define SCREEN_WIDTH         (SCREEN_COLUMNS * TILE_SIZE)
#define SCREEN_HEIGHT        (SCREEN_ROWS * TILE_SIZE)
#define BLOCK_SIZE           (TILE_PER_BLOCK * TILE_SIZE)

// PINS

#define PIN_RROM     (1 << PORTB0)
#define PIN_WRAM     (1 << PORTB1)
#define PIN_VBLANK   (1 << PORTB2)
#define PIN_RW       (1 << PORTB3)
#define PIN_ENABLE   (1 << PORTB4)
#define PIN_NMI      (1 << PORTB5)
#define PIN_CLOCK    (1 << PORTB6)

// FUNCTIONS

#define FUNC_CTRL      0x00
#define FUNC_STATUS    0x01
#define FUNC_MEM_ADDR  0x03
#define FUNC_MEM_DATA  0x04
#define FUNC_MEM_DMA   0x05
#define FUNC_OAM_ADDR  0x06
#define FUNC_OAM_DATA  0x07
#define FUNC_DMA_ADDR  0x08
#define FUNC_DMA_DATA  0x09

// CONTROL MASK

#define CONTROL_BASE   0b00000001

/// STATUS MASK

#define STATUS_DMA     0b00000001
#define STATUS_NMI     0b00000010

// OAM ATTRIBUTE MASK

#define OAM_ATTR_PAL   0b00000011
#define OAM_ATTR_SHOW  0b00000100

// GRAPHIC MEMORY

struct gmem_t
{
  // bank 0 and 1
  byte nametables[NAMETABLE_COUNT][SCREEN_ROWS][SCREEN_COLUMNS];
  byte reserved1[32];
  // bank 2 and 3
  byte attributes[NAMETABLE_COUNT][SCREEN_ROWS][SCREEN_COLUMNS];
  byte palettes[PALETTE_COUNT][COLOR_PER_PALETTE];
  // Bank 4 and 5
  byte patterns[TILE_SIZE * 2][PATTERN_COUNT];
};
struct gmem_t gmem;

// OBJECT ATTRIBUTE MEMORY

struct oam_t
{
  byte posx;
  byte pattern;
  byte attribute;
  byte posy;
};
struct oam_t oam[OAM_COUNT];

// VIDEO RAM

byte vram_data[SCREEN_WIDTH * BLOCK_SIZE];

// REGISTERS

byte status     = 0;
byte control    = 0;
word gmem_addr  = 0;
byte gmem_incr  = 1;
word oam_addr   = 0;
word dma_addr   = 0;
byte dma_type   = 0;
byte vram_block = 0;
