####---- CreateClock list ----2
create_clock  -period 10.00 -waveform {0.00 5.00} -name {clk_0} [get_ports {clk}] 
create_clock  -period 1000.00 -waveform {0.00 500.00} -name {vga_signals_6|pixel_clk_inferred_clock} [get_pins {this_vga_signals.pixel_clk_inferred_clock_RNO/O}] 

