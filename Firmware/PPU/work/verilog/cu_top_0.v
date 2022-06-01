/*
   This file was generated automatically by Alchitry Labs version 1.2.7.
   Do not edit this file directly. Instead edit the original Lucid source.
   This is a temporary file and any changes made to it will be destroyed.
*/

module cu_top_0 (
    input clk,
    input rst_n,
    input port_enb,
    input port_clk,
    inout port_rw,
    inout [15:0] port_address,
    inout [7:0] port_data,
    output reg port_data_rw,
    output reg port_dmab,
    output reg port_nmib,
    output reg hsync,
    output reg vsync,
    output reg hblank,
    output reg vblank,
    output reg [5:0] rgb,
    output reg [7:0] led,
    output reg [1:0] debug
  );
  
  reg [0:0] IO_port_rw_enable;
  wire [0:0] IO_port_rw_read;
  reg [0:0] IO_port_rw_write;
  assign port_rw = IO_port_rw_enable ? IO_port_rw_write : 1'bz;
  assign IO_port_rw_read = port_rw;
  reg [15:0] IO_port_address_enable;
  wire [15:0] IO_port_address_read;
  reg [15:0] IO_port_address_write;
  genvar GEN_port_address;
  generate
    for (GEN_port_address = 0; GEN_port_address < 16; GEN_port_address = GEN_port_address + 1) begin
      assign port_address[GEN_port_address] = IO_port_address_enable[GEN_port_address] ? IO_port_address_write[GEN_port_address] : 1'bz;
    end
  endgenerate
  assign IO_port_address_read = port_address;
  reg [7:0] IO_port_data_enable;
  wire [7:0] IO_port_data_read;
  reg [7:0] IO_port_data_write;
  genvar GEN_port_data;
  generate
    for (GEN_port_data = 0; GEN_port_data < 8; GEN_port_data = GEN_port_data + 1) begin
      assign port_data[GEN_port_data] = IO_port_data_enable[GEN_port_data] ? IO_port_data_write[GEN_port_data] : 1'bz;
    end
  endgenerate
  assign IO_port_data_read = port_data;
  
  
  localparam WIDTH = 8'h80;
  
  localparam HEIGHT = 8'h80;
  
  localparam COLORS = 5'h10;
  
  localparam MAP_WIDTH = 6'h20;
  
  localparam MAP_HEIGHT = 6'h20;
  
  localparam SPRITESHEET_WIDTH = 5'h10;
  
  localparam SPRITESHEET_HEIGHT = 5'h10;
  
  localparam SPRITE_WIDTH = 4'h8;
  
  localparam SPRITE_HEIGHT = 4'h8;
  
  localparam OAM_ENTRY_COUNT = 7'h40;
  
  localparam OAM_ENTRY_WIDTH = 6'h20;
  
  localparam OAM_ENTRY_BITS = 2'h2;
  
  localparam CTRL_NMI_EN = 3'h7;
  
  localparam CTRL_MASK_FG = 3'h6;
  
  localparam CTRL_MASK_BG = 3'h5;
  
  localparam CTRL_ADDR_INC = 3'h4;
  
  localparam STATUS_NMI = 3'h7;
  
  localparam STATUS_RDY = 1'h0;
  
  reg rst;
  
  reg dma;
  
  reg [1:0] i;
  
  wire [1-1:0] M_this_reset_cond_out;
  reg [1-1:0] M_this_reset_cond_in;
  reset_conditioner_1 this_reset_cond (
    .clk(clk),
    .in(M_this_reset_cond_in),
    .out(M_this_reset_cond_out)
  );
  
  wire [1-1:0] M_this_delay_clk_out;
  reg [1-1:0] M_this_delay_clk_in;
  pipeline_2 this_delay_clk (
    .clk(clk),
    .in(M_this_delay_clk_in),
    .out(M_this_delay_clk_out)
  );
  wire [1-1:0] M_this_start_address_delay_out;
  reg [1-1:0] M_this_start_address_delay_in;
  edge_detector_3 this_start_address_delay (
    .clk(clk),
    .in(M_this_start_address_delay_in),
    .out(M_this_start_address_delay_out)
  );
  wire [1-1:0] M_this_start_data_delay_out;
  reg [1-1:0] M_this_start_data_delay_in;
  edge_detector_4 this_start_data_delay (
    .clk(clk),
    .in(M_this_start_data_delay_in),
    .out(M_this_start_data_delay_out)
  );
  
  wire [1-1:0] M_this_pixel_clk_out;
  pixel_clock_5 this_pixel_clk (
    .clk(clk),
    .rst(rst),
    .out(M_this_pixel_clk_out)
  );
  
  wire [1-1:0] M_this_vga_signals_pixel_clk;
  wire [1-1:0] M_this_vga_signals_line_clk;
  wire [1-1:0] M_this_vga_signals_hsync;
  wire [1-1:0] M_this_vga_signals_vsync;
  wire [1-1:0] M_this_vga_signals_hblank;
  wire [1-1:0] M_this_vga_signals_vblank;
  wire [14-1:0] M_this_vga_signals_address;
  vga_signals_6 this_vga_signals (
    .clk(M_this_pixel_clk_out),
    .rst(rst),
    .pixel_clk(M_this_vga_signals_pixel_clk),
    .line_clk(M_this_vga_signals_line_clk),
    .hsync(M_this_vga_signals_hsync),
    .vsync(M_this_vga_signals_vsync),
    .hblank(M_this_vga_signals_hblank),
    .vblank(M_this_vga_signals_vblank),
    .address(M_this_vga_signals_address)
  );
  
  wire [6-1:0] M_this_vga_ramdac_rgb;
  reg [1-1:0] M_this_vga_ramdac_en;
  reg [4-1:0] M_this_vga_ramdac_vram_data;
  vga_ramdac_7 this_vga_ramdac (
    .clk(M_this_vga_signals_pixel_clk),
    .rst(rst),
    .en(M_this_vga_ramdac_en),
    .vram_data(M_this_vga_ramdac_vram_data),
    .rgb(M_this_vga_ramdac_rgb)
  );
  
  wire [8-1:0] M_this_ppu_vram_addr;
  wire [1-1:0] M_this_ppu_vram_en;
  wire [4-1:0] M_this_ppu_vram_data;
  wire [14-1:0] M_this_ppu_spr_addr;
  wire [10-1:0] M_this_ppu_map_addr;
  wire [6-1:0] M_this_ppu_oam_addr;
  reg [1-1:0] M_this_ppu_en;
  reg [1-1:0] M_this_ppu_vga_is_drawing;
  reg [2-1:0] M_this_ppu_mask;
  reg [16-1:0] M_this_ppu_scroll;
  reg [4-1:0] M_this_ppu_spr_data;
  reg [8-1:0] M_this_ppu_map_data;
  reg [32-1:0] M_this_ppu_oam_data;
  ppu_8 this_ppu (
    .clk(clk),
    .rst(rst),
    .vga_line_clk(M_this_vga_signals_line_clk),
    .en(M_this_ppu_en),
    .vga_is_drawing(M_this_ppu_vga_is_drawing),
    .mask(M_this_ppu_mask),
    .scroll(M_this_ppu_scroll),
    .spr_data(M_this_ppu_spr_data),
    .map_data(M_this_ppu_map_data),
    .oam_data(M_this_ppu_oam_data),
    .vram_addr(M_this_ppu_vram_addr),
    .vram_en(M_this_ppu_vram_en),
    .vram_data(M_this_ppu_vram_data),
    .spr_addr(M_this_ppu_spr_addr),
    .map_addr(M_this_ppu_map_addr),
    .oam_addr(M_this_ppu_oam_addr)
  );
  
  wire [4-1:0] M_this_spr_ram_read_data;
  reg [14-1:0] M_this_spr_ram_waddr;
  reg [4-1:0] M_this_spr_ram_write_data;
  reg [1-1:0] M_this_spr_ram_write_en;
  reg [14-1:0] M_this_spr_ram_raddr;
  simple_dual_ram_9 #(.SIZE(3'h4), .DEPTH(18'h04000)) this_spr_ram (
    .rclk(clk),
    .wclk(clk),
    .waddr(M_this_spr_ram_waddr),
    .write_data(M_this_spr_ram_write_data),
    .write_en(M_this_spr_ram_write_en),
    .raddr(M_this_spr_ram_raddr),
    .read_data(M_this_spr_ram_read_data)
  );
  wire [8-1:0] M_this_map_ram_read_data;
  reg [10-1:0] M_this_map_ram_waddr;
  reg [8-1:0] M_this_map_ram_write_data;
  reg [1-1:0] M_this_map_ram_write_en;
  reg [10-1:0] M_this_map_ram_raddr;
  simple_dual_ram_10 #(.SIZE(4'h8), .DEPTH(12'h400)) this_map_ram (
    .rclk(clk),
    .wclk(clk),
    .waddr(M_this_map_ram_waddr),
    .write_data(M_this_map_ram_write_data),
    .write_en(M_this_map_ram_write_en),
    .raddr(M_this_map_ram_raddr),
    .read_data(M_this_map_ram_read_data)
  );
  wire [32-1:0] M_this_oam_ram_read_data;
  reg [6-1:0] M_this_oam_ram_waddr;
  reg [32-1:0] M_this_oam_ram_write_data;
  reg [1-1:0] M_this_oam_ram_write_en;
  reg [6-1:0] M_this_oam_ram_raddr;
  simple_dual_ram_11 #(.SIZE(6'h20), .DEPTH(7'h40)) this_oam_ram (
    .rclk(clk),
    .wclk(clk),
    .waddr(M_this_oam_ram_waddr),
    .write_data(M_this_oam_ram_write_data),
    .write_en(M_this_oam_ram_write_en),
    .raddr(M_this_oam_ram_raddr),
    .read_data(M_this_oam_ram_read_data)
  );
  wire [4-1:0] M_this_vram_read_data;
  reg [8-1:0] M_this_vram_waddr;
  reg [4-1:0] M_this_vram_write_data;
  reg [1-1:0] M_this_vram_write_en;
  reg [8-1:0] M_this_vram_raddr;
  simple_dual_ram_12 #(.SIZE(3'h4), .DEPTH(10'h100)) this_vram (
    .rclk(clk),
    .wclk(clk),
    .waddr(M_this_vram_waddr),
    .write_data(M_this_vram_write_data),
    .write_en(M_this_vram_write_en),
    .raddr(M_this_vram_raddr),
    .read_data(M_this_vram_read_data)
  );
  
  reg [31:0] M_this_warmup_d, M_this_warmup_q = 1'h0;
  reg [7:0] M_this_status_flags_d, M_this_status_flags_q = 1'h0;
  reg [7:0] M_this_ctrl_flags_d, M_this_ctrl_flags_q = 1'h0;
  reg [15:0] M_this_scroll_d, M_this_scroll_q = 1'h0;
  reg [15:0] M_this_ext_address_d, M_this_ext_address_q = 1'h0;
  reg [13:0] M_this_spr_address_d, M_this_spr_address_q = 1'h0;
  reg [9:0] M_this_map_address_d, M_this_map_address_q = 1'h0;
  reg [7:0] M_this_oam_address_d, M_this_oam_address_q = 1'h0;
  
  localparam IDLE_this_state = 5'd0;
  localparam CTRL_WRITE_this_state = 5'd1;
  localparam STATUS_READ_this_state = 5'd2;
  localparam MAP_WRITE_HADDR_this_state = 5'd3;
  localparam MAP_WRITE_LADDR_this_state = 5'd4;
  localparam MAP_READ_DATA_this_state = 5'd5;
  localparam MAP_WRITE_DATA_this_state = 5'd6;
  localparam SCROLL_WRITE_HADDR_this_state = 5'd7;
  localparam SCROLL_WRITE_LADDR_this_state = 5'd8;
  localparam DMA_SPR_START_this_state = 5'd9;
  localparam DMA_MAP_START_this_state = 5'd10;
  localparam DMA_OAM_START_this_state = 5'd11;
  localparam DMA_SPR_LOOP_this_state = 5'd12;
  localparam DMA_SPR_TRANSFER_1_this_state = 5'd13;
  localparam DMA_SPR_TRANSFER_2_this_state = 5'd14;
  localparam DMA_MAP_LOOP_this_state = 5'd15;
  localparam DMA_MAP_TRANSFER_this_state = 5'd16;
  localparam DMA_OAM_LOOP_this_state = 5'd17;
  localparam DMA_OAM_TRANSFER_this_state = 5'd18;
  
  reg [4:0] M_this_state_d, M_this_state_q = IDLE_this_state;
  localparam HIGH_ADDRESS_this_substate = 1'd0;
  localparam LOW_ADDRESS_this_substate = 1'd1;
  
  reg M_this_substate_d, M_this_substate_q = HIGH_ADDRESS_this_substate;
  reg [15:0] M_this_data_count_d, M_this_data_count_q = 1'h0;
  reg [31:0] M_this_data_tmp_d, M_this_data_tmp_q = 1'h0;
  
  always @* begin
    M_this_warmup_d = M_this_warmup_q;
    
    M_this_warmup_d = M_this_warmup_q + 1'h1;
  end
  
  always @* begin
    M_this_status_flags_d = M_this_status_flags_q;
    
    M_this_reset_cond_in = ~rst_n;
    rst = M_this_reset_cond_out;
    dma = M_this_state_q > DMA_OAM_START_this_state ? 1'h1 : 1'h0;
    IO_port_rw_enable = dma;
    IO_port_rw_write = 1'h1;
    IO_port_address_enable = {5'h10{dma}};
    IO_port_address_write = M_this_ext_address_q;
    port_data_rw = !IO_port_rw_read || dma ? 1'h1 : 1'h0;
    port_dmab = ~dma;
    port_nmib = M_this_ctrl_flags_q[7+0-:1] && M_this_vga_signals_vblank && !dma ? 1'h0 : 1'h1;
    hsync = M_this_vga_signals_hsync;
    vsync = M_this_vga_signals_vsync;
    hblank = M_this_vga_signals_hblank;
    vblank = M_this_vga_signals_vblank;
    rgb = M_this_vga_ramdac_rgb;
    M_this_delay_clk_in = port_clk;
    M_this_start_address_delay_in = M_this_delay_clk_out || port_enb;
    M_this_start_data_delay_in = M_this_delay_clk_out || port_enb;
    M_this_vga_ramdac_en = !M_this_vga_signals_hblank && !M_this_vga_signals_vblank ? 1'h1 : 1'h0;
    M_this_vga_ramdac_vram_data = M_this_vram_read_data;
    M_this_ppu_en = M_this_status_flags_q[0+0-:1];
    M_this_ppu_mask = {M_this_ctrl_flags_q[6+0-:1], M_this_ctrl_flags_q[5+0-:1]};
    M_this_ppu_vga_is_drawing = !M_this_vga_signals_vblank && !dma ? 1'h1 : 1'h0;
    M_this_ppu_scroll = M_this_scroll_q;
    M_this_ppu_spr_data = M_this_spr_ram_read_data;
    M_this_ppu_map_data = M_this_map_ram_read_data;
    M_this_ppu_oam_data = M_this_oam_ram_read_data;
    M_this_vram_raddr = M_this_vga_signals_address[0+7-:8];
    M_this_vram_waddr = M_this_ppu_vram_addr;
    M_this_vram_write_en = M_this_ppu_vram_en;
    M_this_vram_write_data = M_this_ppu_vram_data;
    M_this_spr_ram_raddr = M_this_ppu_spr_addr;
    M_this_spr_ram_waddr = M_this_spr_address_q;
    M_this_map_ram_raddr = M_this_ppu_map_addr;
    M_this_map_ram_waddr = M_this_map_address_q;
    M_this_oam_ram_raddr = M_this_ppu_oam_addr;
    M_this_oam_ram_waddr = M_this_oam_address_q[2+5-:6];
    M_this_status_flags_d[7+0-:1] = M_this_vga_signals_vblank ? 1'h1 : 1'h0;
    M_this_status_flags_d[0+0-:1] = M_this_status_flags_q[0+0-:1] | M_this_warmup_q[27+0-:1];
    debug = 2'h0;
  end
  
  always @* begin
    M_this_substate_d = M_this_substate_q;
    M_this_state_d = M_this_state_q;
    M_this_data_tmp_d = M_this_data_tmp_q;
    M_this_spr_address_d = M_this_spr_address_q;
    M_this_map_address_d = M_this_map_address_q;
    M_this_ext_address_d = M_this_ext_address_q;
    M_this_scroll_d = M_this_scroll_q;
    M_this_oam_address_d = M_this_oam_address_q;
    M_this_data_count_d = M_this_data_count_q;
    M_this_ctrl_flags_d = M_this_ctrl_flags_q;
    
    IO_port_data_enable = 1'h0;
    IO_port_data_write = 1'h0;
    M_this_spr_ram_write_en = 1'h0;
    M_this_spr_ram_write_data = 1'h0;
    M_this_map_ram_write_en = 1'h0;
    M_this_map_ram_write_data = 1'h0;
    M_this_oam_ram_write_en = 1'h0;
    M_this_oam_ram_write_data = 1'h0;
    led = 8'h01;
    
    case (M_this_state_q)
      IDLE_this_state: begin
        led = 8'h03;
        if (M_this_start_address_delay_out) begin
          
          case (IO_port_address_read[0+7-:8])
            8'h00: begin
              if (!IO_port_rw_read) begin
                M_this_state_d = CTRL_WRITE_this_state;
                M_this_substate_d = HIGH_ADDRESS_this_substate;
              end
            end
            8'h01: begin
              if (IO_port_rw_read) begin
                M_this_state_d = STATUS_READ_this_state;
                M_this_substate_d = HIGH_ADDRESS_this_substate;
              end
            end
            8'h02: begin
              if (!IO_port_rw_read) begin
                if (M_this_substate_q == HIGH_ADDRESS_this_substate) begin
                  M_this_state_d = MAP_WRITE_HADDR_this_state;
                  M_this_substate_d = LOW_ADDRESS_this_substate;
                end else begin
                  M_this_state_d = MAP_WRITE_LADDR_this_state;
                  M_this_substate_d = HIGH_ADDRESS_this_substate;
                end
              end
            end
            8'h03: begin
              if (!IO_port_rw_read) begin
                M_this_state_d = MAP_WRITE_DATA_this_state;
                M_this_substate_d = HIGH_ADDRESS_this_substate;
              end else begin
                M_this_state_d = MAP_READ_DATA_this_state;
                M_this_substate_d = HIGH_ADDRESS_this_substate;
              end
            end
            8'h04: begin
              if (!IO_port_rw_read) begin
                if (M_this_substate_q == HIGH_ADDRESS_this_substate) begin
                  M_this_state_d = SCROLL_WRITE_HADDR_this_state;
                  M_this_substate_d = LOW_ADDRESS_this_substate;
                end else begin
                  M_this_state_d = SCROLL_WRITE_LADDR_this_state;
                  M_this_substate_d = HIGH_ADDRESS_this_substate;
                end
              end
            end
            8'h10: begin
              if (!IO_port_rw_read) begin
                M_this_state_d = DMA_SPR_START_this_state;
                M_this_substate_d = HIGH_ADDRESS_this_substate;
              end
            end
            8'h11: begin
              if (!IO_port_rw_read) begin
                M_this_state_d = DMA_MAP_START_this_state;
                M_this_substate_d = HIGH_ADDRESS_this_substate;
              end
            end
            8'h12: begin
              if (!IO_port_rw_read) begin
                M_this_state_d = DMA_OAM_START_this_state;
                M_this_substate_d = HIGH_ADDRESS_this_substate;
              end
            end
          endcase
        end
      end
      CTRL_WRITE_this_state: begin
        led = 8'h41;
        if (M_this_start_data_delay_out) begin
          M_this_ctrl_flags_d = IO_port_data_read;
          M_this_state_d = IDLE_this_state;
        end
      end
      STATUS_READ_this_state: begin
        led = 8'h21;
        IO_port_data_enable = 8'hff;
        IO_port_data_write = M_this_status_flags_q;
        if (M_this_start_data_delay_out) begin
          M_this_state_d = IDLE_this_state;
        end
      end
      MAP_WRITE_HADDR_this_state: begin
        led = 8'h41;
        if (M_this_start_data_delay_out) begin
          M_this_map_address_d[5+4-:5] = IO_port_data_read[0+4-:5];
          M_this_state_d = IDLE_this_state;
        end
      end
      MAP_WRITE_LADDR_this_state: begin
        led = 8'h41;
        if (M_this_start_data_delay_out) begin
          M_this_map_address_d[0+4-:5] = IO_port_data_read[0+4-:5];
          M_this_state_d = IDLE_this_state;
        end
      end
      MAP_WRITE_DATA_this_state: begin
        led = 8'h41;
        if (M_this_start_data_delay_out) begin
          M_this_map_ram_write_en = 1'h1;
          M_this_map_ram_write_data = IO_port_data_read;
          M_this_map_address_d = M_this_map_address_q + (M_this_ctrl_flags_q[4+0-:1] ? 6'h20 : 1'h1);
          M_this_state_d = IDLE_this_state;
        end
      end
      MAP_READ_DATA_this_state: begin
        led = 8'h21;
        IO_port_data_enable = 8'hff;
        IO_port_data_write = M_this_map_ram_read_data;
        if (M_this_start_data_delay_out) begin
          M_this_state_d = IDLE_this_state;
        end
      end
      SCROLL_WRITE_HADDR_this_state: begin
        led = 8'h41;
        if (M_this_start_data_delay_out) begin
          M_this_scroll_d[8+7-:8] = IO_port_data_read;
          M_this_state_d = IDLE_this_state;
        end
      end
      SCROLL_WRITE_LADDR_this_state: begin
        led = 8'h41;
        if (M_this_start_data_delay_out) begin
          M_this_scroll_d[0+7-:8] = IO_port_data_read;
          M_this_state_d = IDLE_this_state;
        end
      end
      DMA_SPR_START_this_state: begin
        led = 8'h81;
        if (M_this_start_data_delay_out) begin
          M_this_ext_address_d = {IO_port_data_read, 8'h00};
          M_this_spr_address_d = 1'h0;
          M_this_data_count_d = 21'h002000;
          M_this_state_d = DMA_SPR_LOOP_this_state;
        end
      end
      DMA_SPR_LOOP_this_state: begin
        led = 8'h81;
        if (M_this_data_count_q == 1'h0) begin
          M_this_state_d = IDLE_this_state;
        end else begin
          if (M_this_start_address_delay_out) begin
            M_this_data_count_d = M_this_data_count_q - 1'h1;
            M_this_state_d = DMA_SPR_TRANSFER_1_this_state;
          end
        end
      end
      DMA_SPR_TRANSFER_1_this_state: begin
        led = 8'hc1;
        if (M_this_start_data_delay_out) begin
          M_this_spr_ram_write_en = 1'h1;
          M_this_spr_ram_write_data = IO_port_data_read[4+3-:4];
          M_this_spr_address_d = M_this_spr_address_q + 1'h1;
          M_this_state_d = DMA_SPR_TRANSFER_2_this_state;
        end
      end
      DMA_SPR_TRANSFER_2_this_state: begin
        led = 8'hc1;
        M_this_spr_ram_write_en = 1'h1;
        M_this_spr_ram_write_data = IO_port_data_read[0+3-:4];
        M_this_spr_address_d = M_this_spr_address_q + 1'h1;
        M_this_ext_address_d = M_this_ext_address_q + 1'h1;
        M_this_state_d = DMA_SPR_LOOP_this_state;
      end
      DMA_MAP_START_this_state: begin
        led = 8'h81;
        if (M_this_start_data_delay_out) begin
          M_this_ext_address_d = {IO_port_data_read, 8'h00};
          M_this_map_address_d = 1'h0;
          M_this_data_count_d = 16'h0400;
          M_this_state_d = DMA_MAP_LOOP_this_state;
        end
      end
      DMA_MAP_LOOP_this_state: begin
        led = 8'h81;
        if (M_this_data_count_q == 1'h0) begin
          M_this_state_d = IDLE_this_state;
        end else begin
          if (M_this_start_address_delay_out) begin
            M_this_data_count_d = M_this_data_count_q - 1'h1;
            M_this_state_d = DMA_MAP_TRANSFER_this_state;
          end
        end
      end
      DMA_MAP_TRANSFER_this_state: begin
        led = 8'hc1;
        if (M_this_start_data_delay_out) begin
          M_this_map_ram_write_en = 1'h1;
          M_this_map_ram_write_data = IO_port_data_read;
          M_this_map_address_d = M_this_map_address_q + 1'h1;
          M_this_ext_address_d = M_this_ext_address_q + 1'h1;
          M_this_state_d = DMA_MAP_LOOP_this_state;
        end
      end
      DMA_OAM_START_this_state: begin
        led = 8'h81;
        if (M_this_start_data_delay_out) begin
          M_this_ext_address_d = {IO_port_data_read, 8'h00};
          M_this_oam_address_d = 1'h0;
          M_this_data_count_d = 13'h0100;
          M_this_state_d = DMA_OAM_LOOP_this_state;
        end
      end
      DMA_OAM_LOOP_this_state: begin
        led = 8'h81;
        if (M_this_data_count_q == 1'h0) begin
          M_this_state_d = IDLE_this_state;
        end else begin
          if (M_this_start_address_delay_out) begin
            M_this_data_count_d = M_this_data_count_q - 1'h1;
            M_this_state_d = DMA_OAM_TRANSFER_this_state;
          end
        end
      end
      DMA_OAM_TRANSFER_this_state: begin
        led = 8'hc1;
        if (M_this_start_data_delay_out) begin
          i = M_this_oam_address_q[0+1-:2];
          if (i == 7'h03) begin
            M_this_oam_ram_write_en = 1'h1;
            M_this_oam_ram_write_data = {IO_port_data_read, M_this_data_tmp_q[0+23-:24]};
          end else begin
            M_this_data_tmp_d[((i * 4'h8))*1+7-:8] = IO_port_data_read;
          end
          M_this_oam_address_d = M_this_oam_address_q + 1'h1;
          M_this_ext_address_d = M_this_ext_address_q + 1'h1;
          M_this_state_d = DMA_OAM_LOOP_this_state;
        end
      end
    endcase
  end
  
  always @(posedge clk) begin
    if (rst == 1'b1) begin
      M_this_data_count_q <= 1'h0;
      M_this_data_tmp_q <= 1'h0;
      M_this_state_q <= 1'h0;
      M_this_substate_q <= 1'h0;
    end else begin
      M_this_data_count_q <= M_this_data_count_d;
      M_this_data_tmp_q <= M_this_data_tmp_d;
      M_this_state_q <= M_this_state_d;
      M_this_substate_q <= M_this_substate_d;
    end
  end
  
  
  always @(posedge clk) begin
    if (rst == 1'b1) begin
      M_this_warmup_q <= 1'h0;
      M_this_status_flags_q <= 1'h0;
      M_this_ctrl_flags_q <= 1'h0;
      M_this_scroll_q <= 1'h0;
      M_this_ext_address_q <= 1'h0;
      M_this_spr_address_q <= 1'h0;
      M_this_map_address_q <= 1'h0;
      M_this_oam_address_q <= 1'h0;
    end else begin
      M_this_warmup_q <= M_this_warmup_d;
      M_this_status_flags_q <= M_this_status_flags_d;
      M_this_ctrl_flags_q <= M_this_ctrl_flags_d;
      M_this_scroll_q <= M_this_scroll_d;
      M_this_ext_address_q <= M_this_ext_address_d;
      M_this_spr_address_q <= M_this_spr_address_d;
      M_this_map_address_q <= M_this_map_address_d;
      M_this_oam_address_q <= M_this_oam_address_d;
    end
  end
  
endmodule
