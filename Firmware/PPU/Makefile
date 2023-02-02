PROG=alchitry
WORKDIR=work

DEVICE=--hx8k --package cb132
OPTIONS=--timing-allow-fail --freq 100

all: $(WORKDIR)/$(PROG).bin

clean:
	rm -f $(WORKDIR)/$(PROG).bin

upload:
	iceprog $(WORKDIR)/$(PROG).bin 

$(WORKDIR)/%.json: $(WORKDIR)/verilog/*.v
	yosys -p 'synth_ice40 -top cu_top_0 -json $@' $^ 

$(WORKDIR)/%.asc: $(WORKDIR)/%.json $(WORKDIR)/constraint/$(PROG).pcf 
	nextpnr-ice40 $(OPTIONS) $(DEVICE) --json $< --pcf $(WORKDIR)/constraint/$(PROG).pcf --asc $@

$(WORKDIR)/%.bin: $(WORKDIR)/%.asc
	icepack $< $@
