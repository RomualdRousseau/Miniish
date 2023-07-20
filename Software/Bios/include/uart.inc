uart_port        = io_port3
uart_data_reg    = uart_port + $00
uart_status_reg  = uart_port + $01
uart_command_reg = uart_port + $02
uart_control_reg = uart_port + $03
uart_status_tde  = zero_start + $10