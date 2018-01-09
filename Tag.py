# -*- coding: ascii -*-
# $Id: Tag.py,v 0.1 2014/10/15 15:03:49 bnv Exp $
#
# Author: mrremmers@gmail.com
# Date: 1-Jan-2018

import untangle
import os
from os import listdir
from os.path import isfile, join
from collections import namedtuple
import Utils
##==============================================================================
## Tag class
##==============================================================================
class NamePlate():
    numTag = 0
    text = ''

class Fixture(object):
    #perimiter
    tag = []
    def __init__(self, template):
        tagPath = os.path.join(Utils.prgpath, 'template')
        templatefiles = [f for f in listdir(tagPath) if isfile(join(tagPath, f)) and f.endswith(".xml")]

        doc = untangle.parse(join(tagPath,templatefiles[0]))
        self.perimeter = {'x0': float(doc.JigTemplate.Perimeter.X0.cdata), 'y0':float(doc.JigTemplate.Perimeter.Y0.cdata), 
                          'x1':float(doc.JigTemplate.Perimeter.X1.cdata), 'y1':float(doc.JigTemplate.Perimeter.Y1.cdata)}
        for st in doc.JigTemplate.Tags.cavity:
            try:
                rect = {'x0': float(st.X0.cdata), 'y0': float(st.Y0.cdata), 'x1': float(st.X1.cdata), 'y1': float(st.Y1.cdata)}
                self.tag.append(rect)
            except AttributeError:
                break

#class Tag(object):

#    rect =  namedtuple('rectangle', ['x0', 'y0','x1','y1'])

#    def __init__(self, template):
#        tagPath = os.path.join(Utils.prgpath, 'template')
#        templatefiles = [f for f in listdir(tagPath) if isfile(join(tagPath, f)) and f.endswith(".xml")]

#        self.name = template  #name of the template
#        #self.stringValues = []
#        #self.tagloc = []
#        self.tags = {}
#        #i for j in templatefiles:
#        #    if i = template:
#        doc = untangle.parse(join(tagPath,templatefiles[0]))
#        self.perimeter = Tag.rect
#        self.perimeter.x0 = float(doc.JigTemplate.Perimeter.X0.cdata)
#        self.perimeter.y0 = float(doc.JigTemplate.Perimeter.Y0.cdata)
#        self.perimeter.x1 = float(doc.JigTemplate.Perimeter.X1.cdata)
#        self.perimeter.y1 = float(doc.JigTemplate.Perimeter.Y1.cdata)

#        for st in doc.JigTemplate.Tags.cavity:
#            try:
#                #self.stringValues.append("1")
#                #self.tagloc.append(Tag.rect(x0= float(st.X0.cdata), y0= float(st.Y0.cdata), x1= float(st.X1.cdata), y1= float(st.Y1.cdata)))
#                self.tags.keys().
#            except AttributeError:
#                break


