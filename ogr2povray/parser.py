import osgeo.ogr as ogr
import osgeo.osr as osr
import sys
import math
from ogr2povray.gradient import *
from ogr2povray.object import *


class OGRParser:
   def __init__(self,filename,datafield,layer):
      self.datasource=ogr.Open(filename)
      if self.datasource==None:
         raise IOError('unable to open file.')
      self.datafield=datafield
      self.layer=layer
      self.povobjects=[]

   def getMaxvalueDouble(self,filename):
      datasource=ogr.Open(filename)
      if datasource==None:
         raise IOError('unable to open file.')     
      # get maximal value of datafield
      # opened datasource again because using the same datasource did not work...
      sqllyr=datasource.ExecuteSQL('SELECT max("%s") FROM %s' % (self.datafield,self.layer))
      if not sqllyr:
         raise IOError("Failed to query layer %s." % self.layer)
      feat = sqllyr.GetNextFeature()
      maxvalue = float(feat.GetFieldAsDouble(0))
      datasource.ReleaseResultSet(sqllyr)
      return maxvalue

   def parse(self):
      self.povobjects=[]
      lyr = self.datasource.GetLayer(self.layer)
      feat=lyr.GetNextFeature()
      fdfn=feat.GetDefnRef()
      df_idx=fdfn.GetFieldIndex(self.datafield)

      #prepare spatial reference for wgs84
      sr84=osr.SpatialReference()
      sr84.ImportFromEPSG(4326)

      while (feat):
         geom = feat.GetGeometryRef()

         # transform geom to wgs84 if possible. if no sr is assigned, no transformation is possible
         if not geom.GetSpatialReference() in (None,sr84):
            geom.TransformTo(sr84)

         self.processFeature(feat,geom,df_idx)
         feat=lyr.GetNextFeature()
         
   def processFeature(self,feat,geom,df_idx):
      pass

   def __repr__(self):
      return '\n'.join(map(str,self.povobjects))


class Polygon2PrismParser(OGRParser):
   """
   this parser converts polygon-geometries to povray-prisms
   """
   def __init__(self,filename,datafield,layer,gradient,log=False):
      OGRParser.__init__(self,filename,datafield,layer)
      self.gradient=gradient
      self.log=log # use logarithmic color curve
      self.threshold_area=1 # only render features with an area bigger than this
      self.prism_maxheight=80 # max height a prism can have
      self.prism_minheight=0.001 # min height a prism can have. 
      self.maxvalue=self.getMaxvalueDouble(filename)


   def processFeature(self,feat,geom,df_idx):
      OGRParser.processFeature(self,feat,geom,df_idx)

      # color
      if self.log: # logarithmic color curve
         fieldvalue=feat.GetFieldAsDouble(df_idx)+1.0
         if fieldvalue!=0.0:
            thislog=math.log(feat.GetFieldAsDouble(df_idx)+1.0,self.maxvalue+1)
         else:
            thislog=0.0
         thisrgb=self.gradient.getColor(thislog).rgb()
      else: # linear color curve
         thisrgb=self.gradient.getColor(feat.GetFieldAsDouble(df_idx)/self.maxvalue).rgb()

      # height of the prism
      thisheight = self.prism_maxheight*(feat.GetFieldAsDouble(df_idx)/self.maxvalue)
      if thisheight<self.prism_minheight: # features without/with small values shall also be rendered
         thisheight=self.prism_minheight

      gt=geom.GetGeometryType()
      if gt==ogr.wkbPolygon:
         self.addPolygon(geom,thisheight,thisrgb)
      if gt==ogr.wkbMultiPolygon:
         self.addMultiPolygon(geom,thisheight,thisrgb)

   def addPolygon(self,geom,height,rgb):
      if geom.GetArea()>self.threshold_area:
         prism = Prism(height)
         prism.setRGB(rgb)
         #g2=geom.GetBoundary() # ommit inner polygons ("holes")
         g2=geom.GetGeometryRef(0) # GetBoundary looses countries like italy and south africa which contain other countries
         for j in range(0,g2.GetPointCount()):
            x,y,z=g2.GetPoint(j)
            prism.addPoint(x,y)
         self.povobjects.append(prism)

   def addMultiPolygon(self,geom,height,rgb):
      for i in range(0,geom.GetGeometryCount()):
         geom2 = geom.GetGeometryRef(i)
         self.addPolygon(geom2,height,rgb)

