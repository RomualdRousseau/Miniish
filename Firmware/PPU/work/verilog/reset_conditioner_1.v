/*
   This file was generated automatically by Alchitry Labs version 1.2.7.
   Do not edit this file directly. Instead edit the original Lucid source.
   This is a temporary file and any changes made to it will be destroyed.
*/

/*
   Parameters:
     STAGES = 10
*/
module reset_conditioner_1 (
    input clk,
    input in,
    output reg out
  );
  
  localparam STAGES = 4'ha;
  
  
  reg [9:0] M_stage_d, M_stage_q = 10'h3ff;
  
  always @* begin
    M_stage_d = M_stage_q;
    
    M_stage_d = {M_stage_q[0+8-:9], 1'h0};
    out = M_stage_q[9+0-:1];
  end
  
  always @(posedge clk) begin
    if (in == 1'b1) begin
      M_stage_q <= 10'h3ff;
    end else begin
      M_stage_q <= M_stage_d;
    end
  end
  
endmodule