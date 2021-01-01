// SCREEN CONFIGURATION

#define SCREEN_REAL_WIDTH    160
#define SCREEN_COLUMNS       16
#define SCREEN_ROWS          12
#define SCREEN_WIDTH         (SCREEN_COLUMNS * TILE_SIZE)
#define SCREEN_HEIGHT        (SCREEN_ROWS * TILE_SIZE)
#define COLOR_PER_PALETTE    4

// TILE AND BLOCK CONFIGURAITON

#define TILE_SIZE            8
#define TILE_PER_BLOCK       4
#define BLOCK_SIZE           (TILE_PER_BLOCK * TILE_SIZE)

// SPRITE CONFIGURATION

#define SPRITE_PER_SCANLINE  7

// GRAPHIC MEMORY CONFIGURATION

#define NAMETABLES_COUNT     2
#define PALETTES_COUNT       8
#define PATTERNS_COUNT       64
#define NAMETABLES_OFFEST    0
#define ATTRIBUTES_OFFSET    512
#define PATTERNS_OFFSET      1024
#define NAMETABLES_SIZE      (NAMETABLES_COUNT * NAMETABLE_SIZE)
#define NAMETABLE_SIZE       (SCREEN_ROWS * SCREEN_COLUMNS)
#define ATTRIBUTES_SIZE      NAMETABLES_SIZE
#define ATTRIBUTE_SIZE       NAMETABLE_SIZE
#define PALETTES_SIZE        (PALETTES_COUNT * COLOR_PER_PALETTE)
#define PATTERNS_SIZE        (PATTERNS_COUNT * PATTERN_SIZE)
#define PATTERN_SIZE         (TILE_SIZE * (COLOR_PER_PALETTE / 2))
#define OAM_PALETTES_OFFSET  (PALETTES_COUNT / 2)
#define OAM_COUNT            32
#define DMAQ_COUNT           32
#define DMA_CHUNK_SIZE       256

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
#define FUNC_STATUS    0x02
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

// DMA TYPE

#define DMA_NAMETABLE  0x00
#define DMA_ATTRIBUTE  0x01
#define DMA_PALETTE    0x02
#define DMA_PATTERN    0x03

// DMA STATE

#define DMA_INIT       0
#define DMA_TRANSFER   1

// GRAPHIC MEMORY

struct gmem_t
{
  // bank 0 and 1
  byte nametables[NAMETABLES_COUNT][SCREEN_ROWS][SCREEN_COLUMNS];
  byte reserved1[ATTRIBUTES_OFFSET - NAMETABLES_SIZE];
  // bank 2 and 3
  byte attributes[NAMETABLES_COUNT][SCREEN_ROWS][SCREEN_COLUMNS];
  byte palettes[PALETTES_COUNT][COLOR_PER_PALETTE];
  byte reserved2[PATTERNS_OFFSET - ATTRIBUTES_OFFSET - ATTRIBUTES_SIZE - PALETTES_SIZE];
  // Bank 4 and 5
  byte patterns[PATTERN_SIZE][PATTERNS_COUNT];
};
struct gmem_t gmem;

// OBJECT ATTRIBUTE MEMORY

struct oam_t
{
  byte posy;
  byte pattern;
  byte attribute;
  byte posx;
};
struct oam_t oam[OAM_COUNT];

// DMA QUEUE

struct dmaq_t
{
  word addr;
  byte type;
};
struct dmaq_t dmaq[DMAQ_COUNT];

struct dma_info_t
{
  byte state;
  byte index;
  word source;
  byte* destination;
  word size_curr;
  word size_total;
};
struct dma_info_t dma_info;

// VIDEO RAM

byte vram_data[SCREEN_REAL_WIDTH * BLOCK_SIZE];

// REGISTERS

byte status     = 0;
byte control    = 0;
word gmem_addr  = 0;
byte gmem_incr  = 1;
word oam_addr   = 0;
word dma_addr   = 0;
byte dma_type   = 0;
byte dmaq_curr  = 0;
byte vram_block = 0;
