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
  
  
  
  localparam WAIT_state = 1'd0;
  localparam COPY_DATA_state = 1'd1;
  
  reg M_state_d, M_state_q = WAIT_state;
  reg [6:0] M_haddress_d, M_haddress_q = 1'h0;
  reg [6:0] M_vaddress_d, M_vaddress_q = 1'h0;
  wire [1-1:0] M_line_clk_out;
  reg [1-1:0] M_line_clk_in;
  edge_detector_4 line_clk (
    .clk(clk),
    .in(M_line_clk_in),
    .out(M_line_clk_out)
  );
  
  always @* begin
    M_state_d = M_state_q;
    M_vaddress_d = M_vaddress_q;
    M_haddress_d = M_haddress_q;
    
    M_line_clk_in = vga_line_clk;
    vram_addr = {M_vaddress_q[0+0-:1], M_haddress_q};
    vram_en = 1'h0;
    vram_data = 1'h0;
    map_addr = {M_vaddress_q[3+3-:4], M_haddress_q[3+3-:4]} + 1'h1;
    sprites_addr = {M_vaddress_q, M_haddress_q} + 1'h1;
    
    case (M_state_q)
      WAIT_state: begin
        if (M_line_clk_out) begin
          if (!vga_is_drawing) begin
            M_vaddress_d = 7'h00;
          end else begin
            M_vaddress_d = M_vaddress_q + 1'h1;
          end
          M_haddress_d = 7'h00;
          M_state_d = COPY_DATA_state;
        end
      end
      COPY_DATA_state: begin
        vram_en = 1'h1;
        vram_data = sprites_data;
        if (M_haddress_q < 7'h7f) begin
          M_haddress_d = M_haddress_q + 1'h1;
          M_state_d = COPY_DATA_state;
        end else begin
          M_state_d = WAIT_state;
        end
      end
    endcase
  end
  
  always @(posedge clk) begin
    if (rst == 1'b1) begin
      M_haddress_q <= 1'h0;
      M_vaddress_q <= 1'h0;
      M_state_q <= 1'h0;
    end else begin
      M_haddress_q <= M_haddress_d;
      M_vaddress_q <= M_vaddress_d;
      M_state_q <= M_state_d;
    end
  end
  
endmodule
