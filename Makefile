POVRAY=povray
#BUILD_DIR=build
OUTPUT=world
POV_HEADER=head.pov
POV_OPTIONS=+W2000 +H1125 +Q11 +A
#POV_OPTIONS=-geometry 400x350 +Q10 +A

clean:
	rm -rf $(OUTPUT).png $(OUTPUT).rca $(OUTPUT).pov

pov:
	cat head.pov >$(OUTPUT).pov
	./example-postgis.py >>$(OUTPUT).pov

render:
	$(POVRAY) $(POV_OPTIONS) +O$(OUTPUT).png $(OUTPUT).pov

all: clean pov render
