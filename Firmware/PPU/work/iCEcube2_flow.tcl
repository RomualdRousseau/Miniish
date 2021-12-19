#!usr/bin/tclsh8.4

set device iCE40HX8K-CB132
set top_module cu_top_0
set proj_dir /home/romuald/Projects/alchitry/PPU/work
set output_dir "alchitry_imp"
set edif_file "cu_top_0"
set tool_options ":edifparser -y \"/home/romuald/Projects/alchitry/PPU/work/constraint/merged_constraint.pcf \""
set sbt_root $::env(SBT_DIR)
append sbt_tcl $sbt_root "/tcl/sbt_backend_synpl.tcl"
source $sbt_tcl
run_sbt_backend_auto $device $top_module $proj_dir $output_dir $tool_options $edif_file
exit
