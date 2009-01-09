POVRAY=povray
OUTPUT_PG=world_carbonfootprint
POV_OPTIONS=+W1000 +H575 +Q11 +A

clean:
	rm -rf $(OUTPUT_PG).png $(OUTPUT_PG).rca $(OUTPUT_PG).pov

pov: clean
	./example.py >$(OUTPUT_PG).pov

render: pov
	$(POVRAY) $(POV_OPTIONS) +O$(OUTPUT_PG).png $(OUTPUT_PG).pov


