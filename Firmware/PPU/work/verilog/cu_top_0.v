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
  
  
  localparam PALETTE = 96'hfb698b33ce31fea564252040;
  
  reg rst;
  
  reg dma;
  
  wire [1-1:0] M_this_pixel_clock_out;
  pixel_clock_1 this_pixel_clock (
    .clk(clk),
    .rst(rst),
    .out(M_this_pixel_clock_out)
  );
  reg [5:0] M_this_pixel_data_d, M_this_pixel_data_q = 1'h0;
  localparam INIT_this_state = 3'd0;
  localparam DMA_START_this_state = 3'd1;
  localparam DMA_TRANSFER_HALF1_this_state = 3'd2;
  localparam DMA_TRANSFER_HALF2_this_state = 3'd3;
  localparam WAIT_this_state = 3'd4;
  localparam WRITE_HIGH_ADDRESS_this_state = 3'd5;
  localparam WRITE_LOW_ADDRESS_this_state = 3'd6;
  localparam WRITE_DATA_this_state = 3'd7;
  
  reg [2:0] M_this_state_d, M_this_state_q = INIT_this_state;
  reg [15:0] M_this_external_address_d, M_this_external_address_q = 1'h0;
  reg [13:0] M_this_internal_address_d, M_this_internal_address_q = 1'h0;
  reg [13:0] M_this_data_count_d, M_this_data_count_q = 1'h0;
  wire [1-1:0] M_this_reset_cond_out;
  reg [1-1:0] M_this_reset_cond_in;
  reset_conditioner_2 this_reset_cond (
    .clk(clk),
    .in(M_this_reset_cond_in),
    .out(M_this_reset_cond_out)
  );
  wire [1-1:0] M_this_delay_clk_out;
  reg [1-1:0] M_this_delay_clk_in;
  pipeline_3 this_delay_clk (
    .clk(clk),
    .in(M_this_delay_clk_in),
    .out(M_this_delay_clk_out)
  );
  wire [1-1:0] M_this_start_address_delay_out;
  reg [1-1:0] M_this_start_address_delay_in;
  edge_detector_4 this_start_address_delay (
    .clk(clk),
    .in(M_this_start_address_delay_in),
    .out(M_this_start_address_delay_out)
  );
  wire [1-1:0] M_this_start_data_delay_out;
  reg [1-1:0] M_this_start_data_delay_in;
  edge_detector_5 this_start_data_delay (
    .clk(clk),
    .in(M_this_start_data_delay_in),
    .out(M_this_start_data_delay_out)
  );
  
  wire [1-1:0] M_this_vga_signals_hsync;
  wire [1-1:0] M_this_vga_signals_hblank;
  wire [1-1:0] M_this_vga_signals_vsync;
  wire [1-1:0] M_this_vga_signals_vblank;
  wire [14-1:0] M_this_vga_signals_address;
  wire [1-1:0] M_this_vga_signals_new_pixel;
  vga_signals_6 this_vga_signals (
    .clk(M_this_pixel_clock_out),
    .rst(rst),
    .hsync(M_this_vga_signals_hsync),
    .hblank(M_this_vga_signals_hblank),
    .vsync(M_this_vga_signals_vsync),
    .vblank(M_this_vga_signals_vblank),
    .address(M_this_vga_signals_address),
    .new_pixel(M_this_vga_signals_new_pixel)
  );
  
  wire [4-1:0] M_this_vram_read_data;
  reg [14-1:0] M_this_vram_waddr;
  reg [4-1:0] M_this_vram_write_data;
  reg [1-1:0] M_this_vram_write_en;
  reg [14-1:0] M_this_vram_raddr;
  simple_dual_ram_7 #(.SIZE(3'h4), .DEPTH(16'h4000)) this_vram (
    .rclk(clk),
    .wclk(clk),
    .waddr(M_this_vram_waddr),
    .write_data(M_this_vram_write_data),
    .write_en(M_this_vram_write_en),
    .raddr(M_this_vram_raddr),
    .read_data(M_this_vram_read_data)
  );
  
  always @* begin
    M_this_state_d = M_this_state_q;
    M_this_external_address_d = M_this_external_address_q;
    M_this_internal_address_d = M_this_internal_address_q;
    M_this_data_count_d = M_this_data_count_q;
    
    M_this_reset_cond_in = ~rst_n;
    rst = M_this_reset_cond_out;
    dma = M_this_state_q == DMA_START_this_state || M_this_state_q == DMA_TRANSFER_HALF1_this_state || M_this_state_q == DMA_TRANSFER_HALF2_this_state ? 1'h0 : 1'h1;
    M_this_delay_clk_in = port_clk;
    M_this_start_address_delay_in = M_this_delay_clk_out || port_enb;
    M_this_start_data_delay_in = M_this_delay_clk_out || port_enb;
    M_this_vram_waddr = M_this_internal_address_q;
    M_this_vram_write_en = 1'h0;
    M_this_vram_write_data = 1'h0;
    IO_port_rw_enable = ~dma;
    IO_port_rw_write = 1'h1;
    IO_port_address_enable = {5'h10{~dma}};
    IO_port_address_write = M_this_external_address_q;
    IO_port_data_enable = 1'h0;
    IO_port_data_write = 1'h0;
    port_data_rw = !IO_port_rw_read || !dma ? 1'h1 : 1'h0;
    port_dmab = dma;
    port_nmib = !M_this_vga_signals_vblank || !dma ? 1'h1 : 1'h0;
    debug[0+0-:1] = M_this_vga_signals_new_pixel;
    debug[1+0-:1] = ~M_this_vga_signals_hblank;
    
    case (M_this_state_q)
      INIT_this_state: begin
        M_this_external_address_d = 16'ha000;
        M_this_internal_address_d = 1'h0;
        M_this_data_count_d = 15'h2000;
        M_this_state_d = DMA_START_this_state;
      end
      DMA_START_this_state: begin
        if (M_this_data_count_q == 1'h0) begin
          M_this_state_d = WAIT_this_state;
        end else begin
          if (M_this_start_address_delay_out) begin
            M_this_state_d = DMA_TRANSFER_HALF1_this_state;
          end
        end
      end
      DMA_TRANSFER_HALF1_this_state: begin
        if (M_this_start_data_delay_out) begin
          M_this_vram_write_en = 1'h1;
          M_this_vram_write_data = IO_port_data_read[4+3-:4];
          M_this_internal_address_d = M_this_internal_address_q + 1'h1;
          M_this_state_d = DMA_TRANSFER_HALF2_this_state;
        end
      end
      DMA_TRANSFER_HALF2_this_state: begin
        M_this_vram_write_en = 1'h1;
        M_this_vram_write_data = IO_port_data_read[0+3-:4];
        M_this_external_address_d = M_this_external_address_q + 1'h1;
        M_this_internal_address_d = M_this_internal_address_q + 1'h1;
        M_this_data_count_d = M_this_data_count_q - 1'h1;
        M_this_state_d = DMA_START_this_state;
      end
      WAIT_this_state: begin
        if (M_this_start_address_delay_out) begin
          
          case (IO_port_address_read[0+7-:8])
            8'h00: begin
              if (!IO_port_rw_read) begin
                M_this_state_d = WRITE_HIGH_ADDRESS_this_state;
              end
            end
            8'h01: begin
              if (!IO_port_rw_read) begin
                M_this_state_d = WRITE_LOW_ADDRESS_this_state;
              end
            end
            8'h02: begin
              if (!IO_port_rw_read) begin
                M_this_state_d = WRITE_DATA_this_state;
              end
            end
          endcase
        end
      end
      WRITE_HIGH_ADDRESS_this_state: begin
        if (M_this_start_data_delay_out) begin
          M_this_internal_address_d[7+6-:7] = IO_port_data_read[0+6-:7];
          M_this_state_d = WAIT_this_state;
        end
      end
      WRITE_LOW_ADDRESS_this_state: begin
        if (M_this_start_data_delay_out) begin
          M_this_internal_address_d[0+6-:7] = IO_port_data_read[0+6-:7];
          M_this_state_d = WAIT_this_state;
        end
      end
      WRITE_DATA_this_state: begin
        if (M_this_start_data_delay_out) begin
          M_this_vram_write_en = 1'h1;
          M_this_vram_write_data = IO_port_data_read[0+3-:4];
          M_this_internal_address_d = M_this_internal_address_q + 1'h1;
          M_this_state_d = WAIT_this_state;
        end
      end
    endcase
  end
  
  always @* begin
    M_this_pixel_data_d = M_this_pixel_data_q;
    
    M_this_vram_raddr = M_this_vga_signals_address;
    hsync = M_this_vga_signals_hsync;
    vsync = M_this_vga_signals_vsync;
    hblank = M_this_vga_signals_hblank;
    vblank = M_this_vga_signals_vblank;
    rgb = M_this_pixel_data_q;
    if (!M_this_vga_signals_hblank && !M_this_vga_signals_vblank) begin
      if (M_this_vga_signals_new_pixel) begin
        M_this_pixel_data_d = PALETTE[(M_this_vram_read_data)*6+5-:6];
      end
    end else begin
      M_this_pixel_data_d = 6'h00;
    end
  end
  
  always @(posedge clk) begin
    if (rst == 1'b1) begin
      M_this_pixel_data_q <= 1'h0;
      M_this_external_address_q <= 1'h0;
      M_this_internal_address_q <= 1'h0;
      M_this_data_count_q <= 1'h0;
      M_this_state_q <= 1'h0;
    end else begin
      M_this_pixel_data_q <= M_this_pixel_data_d;
      M_this_external_address_q <= M_this_external_address_d;
      M_this_internal_address_q <= M_this_internal_address_d;
      M_this_data_count_q <= M_this_data_count_d;
      M_this_state_q <= M_this_state_d;
    end
  end
  
endmodule
