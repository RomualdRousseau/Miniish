create_clock -period 10.00 -name {clk_0} -waveform [list 0.00 5.00] [get_ports clk]
create_clock -period 1000.00 -name {vga_signals_6|pixel_clk_inferred_clock} -waveform [list 0.00 500.00] [get_pins this_vga_signals.pixel_clk_inferred_clock_RNO_LC_13_20_6/lcout]
