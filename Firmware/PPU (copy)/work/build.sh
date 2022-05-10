#!/bin/bash
export LD_LIBRARY_PATH=/opt/lscc/iCEcube2.2020.12/sbt_backend/bin/linux/opt/synpwrap:$LD_LIBRARY_PATH
export LM_LICENSE_FILE=/opt/lscc/license.dat
export SYNPLIFY_PATH=/opt/lscc/iCEcube2.2020.12/synpbase
export SBT_DIR=/opt/lscc/iCEcube2.2020.12/sbt_backend
/opt/lscc/iCEcube2.2020.12/sbt_backend/bin/linux/opt/synpwrap/synpwrap -prj "/home/romuald/Projects/Miniish/Firmware/PPU/work/alchitry_syn.prj"
tclsh "/home/romuald/Projects/Miniish/Firmware/PPU/work/iCEcube2_flow.tcl"
