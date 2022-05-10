/*
   This file was generated automatically by Alchitry Labs version 1.2.7.
   Do not edit this file directly. Instead edit the original Lucid source.
   This is a temporary file and any changes made to it will be destroyed.
*/

/*
   Parameters:
     RISE = 1
     FALL = 0
     DELAY = 20
*/
module edge_detector_with_delay_3 (
    input clk,
    input in,
    output reg out
  );
  
  localparam RISE = 1'h1;
  localparam FALL = 1'h0;
  localparam DELAY = 5'h14;
  
  
  wire [1-1:0] M_this_edge_detector_out;
  reg [1-1:0] M_this_edge_detector_in;
  edge_detector_8 this_edge_detector (
    .clk(clk),
    .in(M_this_edge_detector_in),
    .out(M_this_edge_detector_out)
  );
  wire [1-1:0] M_this_delay_out;
  reg [1-1:0] M_this_delay_in;
  pipeline_7 this_delay (
    .clk(clk),
    .in(M_this_delay_in),
    .out(M_this_delay_out)
  );
  
  always @* begin
    M_this_edge_detector_in = in;
    M_this_delay_in = M_this_edge_detector_out;
    out = M_this_delay_out;
  end
endmodule
