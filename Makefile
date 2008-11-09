POVRAY=povray
BUILD_DIR=build
OUTPUT_PG=world
POV_HEADER=head.pov
POV_OPTIONS=+W2000 +H1125 +Q11 +A
#POV_OPTIONS=-geometry 400x350 +Q10 +A

clean:
	rm -rf $(BUILD_DIR)/$(OUTPUT_PG).png $(BUILD_DIR)/$(OUTPUT_PG).rca $(BUILD_DIR)/$(OUTPUT_PG).pov

pov_pg:
	cat head.pov >$(BUILD_DIR)/$(OUTPUT_PG).pov
	./example-postgis.py >>$(BUILD_DIR)/$(OUTPUT_PG).pov

render_pg:
	$(POVRAY) $(POV_OPTIONS) +O$(BUILD_DIR)/$(OUTPUT_PG).png $(BUILD_DIR)/$(OUTPUT_PG).pov


postgis: pov_pg render_pg


