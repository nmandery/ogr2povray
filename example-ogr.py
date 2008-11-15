#!/usr/bin/python

import osgeo.ogr as ogr
import osgeo.osr as osr
import sys
from colorgradient import *

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

#filename = 'data-ogr/shp2929_wo_greenland/shp2929.shp'
#datafieldname='Per Capita'
#layername='shp2929'

filename = 'data-ogr/shp1839/shp1839.shp'
datafieldname='i'
layername='shp1839'

class Prism:
   def __init__(self,height,cubic=False):
      self.height=height
      self.points=[]
      self.rgb=(1.0,0.0,0.0)
      self.cubic=cubic

   def addPoint(self,x,y):
      self.points.append((x,y))

   def setRGB(self,rgb):
      self.rgb=rgb

   def __repr__(self):
      if len(self.points)>2:
         if self.cubic: # needs some bug hunting - povray complains about unclosed splines
            rep="\nprism { cubic_spline\n 0, %f, %d" % (self.height,len(self.points)+2)
         else:
            rep="\nprism { linear_spline\n 0, %f, %d" % (self.height,len(self.points))
         for point in self.points:
            rep+=",\n <%f, %f>" % point
         if self.cubic:
            rep+=",\n <%f, %f>" % self.points[1]
            rep+=",\n <%f, %f>" % self.points[0]
         rep+="\ntexture { pigment { color rgbf <%f, %f, %f, 0.0> }}" % self.rgb
         rep+="\nfinish { phong 0.2 phong_size 40 }}"
      else:
         rep=''
      return rep


class OGR2PovrayParser:
   def __init__(self,filename,datafield,layer,gradient):
      self.datasource=ogr.Open(filename)
      if self.datasource==None:
         raise IOError('unable to open file.')
      self.datafield=datafield
      self.layer=layer
      self.gradient=gradient
      self.prisms=[]
      self.threshold_area=1 # only render features with an area bigger than this
      self.prism_maxheight=80
      self.prism_minheight=0.001
      self.maxvalue=self.getMaxvalue(filename)

   def getMaxvalue(self,filename):
      datasource=ogr.Open(filename)
      if datasource==None:
         raise IOError('unable to open file.')     
      # get maximal value of datafield
      sqllyr=datasource.ExecuteSQL('SELECT max("%s") FROM %s' % (self.datafield,self.layer))
      if not sqllyr:
         raise IOError("Failed to query layer %s." % self.layer)
      feat = sqllyr.GetNextFeature()
      maxvalue = float(feat.GetFieldAsDouble(0))
      datasource.ReleaseResultSet(sqllyr)
      return maxvalue

   def parse(self):
      self.prisms=[]
      lyr = self.datasource.GetLayer(layername)
      feat=lyr.GetNextFeature()
      fdfn=feat.GetDefnRef()
      df_idx=fdfn.GetFieldIndex(self.datafield)
      #maxvalue=10578947.4 
      while (feat):
         geom = feat.GetGeometryRef()
         thisheight = self.prism_maxheight*(feat.GetFieldAsDouble(df_idx)/self.maxvalue)
         if thisheight<self.prism_minheight: # features without/with small values should also be rendered
            thisheight=self.prism_minheight
         thisrgb = gradient.getColor(feat.GetFieldAsDouble(df_idx)/self.maxvalue).rgb()
         gt = geom.GetGeometryType()
         if gt==ogr.wkbPolygon:
            self.addPolygon(geom,thisheight,thisrgb)
         if gt==ogr.wkbMultiPolygon:
            self.addMultiPolygon(geom,thisheight,thisrgb)
         feat=lyr.GetNextFeature()

   def addPolygon(self,geom,height,rgb):
      if geom.GetArea()>self.threshold_area:
         prism = Prism(height)
         prism.setRGB(rgb)
         g2=geom.GetGeometryRef(0) # GetBoundary() does not return all ???
         for j in range(0,g2.GetPointCount()):
            x,y,z=g2.GetPoint(j)
            prism.addPoint(x,y)
         self.prisms.append(prism)

   def addMultiPolygon(self,geom,height,rgb):
      for i in range(0,geom.GetGeometryCount()):
         geom2 = geom.GetGeometryRef(i)
         self.addPolygon(geom2,height,rgb)

   def __repr__(self):
      return '\n'.join(map(str,self.prisms))

# colors
green = Color(rgb=[0.0,180.0/255.0,0.0])
red = Color(rgb=(180.0/255.0,0.0,0.0))
gradient = HSVGradient(c1=green,c2=red)

povparser=OGR2PovrayParser(filename,datafieldname,layername,gradient)
povparser.parse()

print pov_header
print str(povparser)
