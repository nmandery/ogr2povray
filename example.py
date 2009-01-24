#!/usr/bin/python

from ogr2povray import *

pov_header = """
camera {
   //orthographic
   location <15, 150, -180> // -130 
   right 16/9 * x
   up y
   look_at <15, 25, 0>
   aperture 0.1  // a bit of focal blur
   focal_point < 0, 10, 0> // focus on this point
}

//light_source { <90, 300, 0> color rgb 1 }
//light_source { <-90, 300, 0> color rgb 1 }
light_source { <0, 300, 0> color rgb <1.5 1.5 1.5> }

plane { y, 0
   pigment { 
      color rgb <1.0 1.0 1.0> 
   }
   finish { 
      ambient .2 
      diffuse .6  
      specular .75   
      roughness .001  
      reflection { .1 }  
   }
}

"""

# data
filename = 'data/shp7847/shp7847.shp'
datafieldname='CARBONFOOT'
layername='shp7847'

# colors
# green-red 
green = gradient.Color(rgb=[0.0,180.0/255.0,0.0])
red = gradient.Color(rgb=(180.0/255.0,0.0,0.0))
gradient = gradient.HSVGradient(c1=green,c2=red)

# lightblue-blue
#lightblue = gradient.Color(rgb=(92.0/255.0,142.0/255.0,232.0/255.0))
#blue = gradient.Color(rgb=(24.0/255.0,77.0/255.0,173.0/255.0))
#gradient = gradient.HSVGradient(c1=lightblue,c2=blue)

povparser=parser.Polygon2PrismParser(filename,datafieldname,layername,gradient,log=True)
povparser.parse()

print pov_header
print str(povparser)
