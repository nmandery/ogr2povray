POVRAY=povray
OUTPUT_PG=world_road_density
POV_OPTIONS=+W2000 +H1125 +Q11 +A
#POV_OPTIONS=-geometry 400x350 +Q10 +A

clean:
	rm -rf $(OUTPUT_PG).png $(OUTPUT_PG).rca $(OUTPUT_PG).pov

pov: clean
	./ogr2povray.py >$(OUTPUT_PG).pov

render: pov
	$(POVRAY) $(POV_OPTIONS) +O$(OUTPUT_PG).png $(OUTPUT_PG).pov


