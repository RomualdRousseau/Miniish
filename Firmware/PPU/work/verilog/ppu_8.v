/*
   This file was generated automatically by Alchitry Labs version 1.2.7.
   Do not edit this file directly. Instead edit the original Lucid source.
   This is a temporary file and any changes made to it will be destroyed.
*/

module ppu_8 (
    input clk,
    input rst,
    input vga_line_clk,
    input vga_is_drawing,
    output reg [7:0] vram_addr,
    output reg vram_en,
    output reg [3:0] vram_data,
    output reg [13:0] sprites_addr,
    input [3:0] sprites_data,
    output reg [9:0] map_addr,
    input [7:0] map_data
  );
  
  
  
  reg [7:0] hscroll;
  
  reg [7:0] vscroll;
  
  localparam IDLE_state = 2'd0;
  localparam LOOP_state = 2'd1;
  localparam READ_TILE_state = 2'd2;
  localparam WRITE_PIXEL_state = 2'd3;
  
  reg [1:0] M_state_d, M_state_q = IDLE_state;
  reg [7:0] M_count_d, M_count_q = 1'h0;
  reg [7:0] M_haddress_d, M_haddress_q = 1'h0;
  reg [7:0] M_vaddress_d, M_vaddress_q = 1'h0;
  wire [1-1:0] M_line_clk_out;
  reg [1-1:0] M_line_clk_in;
  edge_detector_4 line_clk (
    .clk(clk),
    .in(M_line_clk_in),
    .out(M_line_clk_out)
  );
  
  always @* begin
    M_state_d = M_state_q;
    M_count_d = M_count_q;
    M_vaddress_d = M_vaddress_q;
    M_haddress_d = M_haddress_q;
    
    M_line_clk_in = vga_line_clk;
    vram_addr = {M_vaddress_q[0+0-:1], M_haddress_q[0+6-:7]};
    vram_en = 1'h0;
    vram_data = 4'bxxxx;
    vscroll = M_vaddress_q + 7'h40;
    hscroll = M_haddress_q + 7'h40;
    map_addr = {vscroll[3+4-:5], hscroll[3+4-:5]};
    sprites_addr = {map_data, vscroll[0+2-:3], hscroll[0+2-:3]};
    
    case (M_state_q)
      IDLE_state: begin
        if (M_line_clk_out) begin
          if (!vga_is_drawing) begin
            M_vaddress_d = 8'h00;
          end else begin
            M_vaddress_d = M_vaddress_q + 1'h1;
          end
          M_haddress_d = 8'h00;
          M_count_d = 8'h80;
          M_state_d = LOOP_state;
        end
      end
      LOOP_state: begin
        if (M_count_q == 1'h0) begin
          M_state_d = IDLE_state;
        end else begin
          M_count_d = M_count_q - 1'h1;
          M_state_d = READ_TILE_state;
        end
      end
      READ_TILE_state: begin
        M_state_d = WRITE_PIXEL_state;
      end
      WRITE_PIXEL_state: begin
        vram_en = 1'h1;
        vram_data = sprites_data;
        M_haddress_d = M_haddress_q + 1'h1;
        M_state_d = LOOP_state;
      end
    endcase
  end
  
  always @(posedge clk) begin
    if (rst == 1'b1) begin
      M_count_q <= 1'h0;
      M_haddress_q <= 1'h0;
      M_vaddress_q <= 1'h0;
      M_state_q <= 1'h0;
    end else begin
      M_count_q <= M_count_d;
      M_haddress_q <= M_haddress_d;
      M_vaddress_q <= M_vaddress_d;
      M_state_q <= M_state_d;
    end
  end
  
endmodule
