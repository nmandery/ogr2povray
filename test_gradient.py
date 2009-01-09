#!/usr/bin/python

from ogr2povray.gradient import *

green = Color(rgb=[0.0,1.0,0.0])
red = Color(rgb=(1.0,0.0,0.0))
orange = Color(rgb=(1.0,72.0/255.0,0.0))

gradient = HSVGradient(c1=green,c2=orange)

print "<html><head></head><body><table>"

for i in range(0,100):
   col = gradient.getColor(i/100.0)
   print "<tr><td bgcolor='%s'>Test %d </td></tr>" % (col.htmlhex(),i)

print "</table></body></html>"
