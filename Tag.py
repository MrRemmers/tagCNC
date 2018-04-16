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
        #templatefiles = [f for f in listdir(tagPath) if isfile(join(tagPath, f)) and f.endswith(".xml")]
        templatefile = template

        doc = untangle.parse(join(tagPath,templatefile))
        self.origin = {'X': float(doc.JigTemplate.Origin.X.cdata), 'Y': float(doc.JigTemplate.Origin.Y.cdata),'Z': float(doc.JigTemplate.Origin.Z.cdata)}
        self.perimeter = {'x0': float(doc.JigTemplate.Perimeter.X0.cdata), 'y0':float(doc.JigTemplate.Perimeter.Y0.cdata), 
                          'x1':float(doc.JigTemplate.Perimeter.X1.cdata), 'y1':float(doc.JigTemplate.Perimeter.Y1.cdata)}
        for st in doc.JigTemplate.Tags.cavity:
            try:
                rect = {'x0': float(st.X0.cdata), 'y0': float(st.Y0.cdata), 'x1': float(st.X1.cdata), 'y1': float(st.Y1.cdata)}
                self.tag.append(rect)
            except AttributeError:
                break


def drawText(self):
    fontPath = os.path.join(Utils.prgpath, 'fonts')
    fontFileName   = join(fontPath, self.pfont.fontCombo.get())
    if fontFileName == "":
        self.setStatus(_("Text abort: please select a font file"))
        return
    depth = -float(self.engrave.depth.get())
    retractZ = float(self.engrave.retractZ.get())
    clearanceZ = float(self.engrave.clearanceZ.get())
    CNC.vars["safe"] = clearanceZ
        

    #clear out any old tag information
    self.initializeGcodeforText(self.localtags.origin['X'], self.localtags.origin['Y'], self.localtags.origin['Z'])

    try:
        import ttf
        font = ttf.TruetypeInfo(fontFileName)
    except:
        self.setStatus(_("Text abort: That embarrassing, I can't read this font file!"))
        return
        
    for plate in self.itemstoEngrave:
            
        t = self.localtags.tag[plate.numTag]
        ##Get inputs
        tagHeight = abs(t['y1']-t['y0'])
        tagWidth = abs(t['x1']-t['x0'])
        textToWrite   = plate.text.get()

        #charsWidth    = self["CharsWidth"]
        #charsWidth     = int(self.font.charspacing.get())

        #Check parameters!!!
        if textToWrite == "":
            textToWrite = "Nel mezzo del cammin di nostra vita..."
            continue

        #Init blocks
        blocks = []
        n = textToWrite
        if not n or n == "default": n = "Text"
        block = Block(n)
        if(u'\n' in  textToWrite):
            block.append("(Text:)")
            for line in textToWrite.splitlines():
                block.append("(%s)" % line)
        else:
            block.append("(Text: %s)" % textToWrite)

        cmap = font.get_character_map()
        kern = None
        try:
            kern = font.get_glyph_kernings()
        except:
            pass
        adv = font.get_glyph_advances()

        #xOffset = 0
        #yOffset = 0
        dx= float(t['x0'])
        dy= float(t['y0'])
        #If there are only a few characters, 
        #the fontsize being the height of the tag works
        #however, longer tags need to be resized
        glyphLength = 0
        for c in textToWrite:
            if c == u'\n':
                xOffset = 0.0
                yOffset -= 1#offset for new line
                continue
            if c in cmap:
                glyphIndx = cmap[c]
            glyphLength += adv[glyphIndx]

        fontSize = 0
        if (glyphLength*tagHeight )> tagWidth:
            fontSize = tagWidth/glyphLength
        else:
            fontSize = tagHeight
        #offset the height difference
        dy = dy + (tagHeight-fontSize)/2
        #offset to center the text
        dx = dx + (tagWidth - glyphLength*fontSize)/2

        glyphIndxLast = cmap[' ']
        xOffset = dx/fontSize
        yOffset = dy/fontSize
        #create the characters
        for c in textToWrite:
	        #New line
            if c == u'\n':
                xOffset = 0.0
                yOffset -= 1#offset for new line
                continue

            if c in cmap:
                glyphIndx = cmap[c]

                if (kern and (glyphIndx,glyphIndxLast) in kern):
                    k = kern[(glyphIndx,glyphIndxLast)] #FIXME: use kern for offset??

	            #Get glyph contours as line segmentes and draw them
                gc = font.get_glyph_contours(glyphIndx)
                if(not gc):
                    gc = font.get_glyph_contours(0)#standard glyph for missing glyphs (complex glyph)
                if(gc and not c==' '): #FIXME: for some reason space is not mapped correctly!!!
                    self.writeGlyphContour(block, font, gc, fontSize, depth, xOffset, yOffset, retractZ)
                if glyphIndx < len(adv):
                    xOffset += adv[glyphIndx]
                else:
                    xOffset += 1
                glyphIndxLast = glyphIndx
        #Gcode Zsafe
        block.append(CNC.zexit(clearanceZ))

        #self.gcode.moveLines(block.path, dx, dy)
        blocks.append(block)
        #active = self.activeBlock()
        #if active==0: active=1
        if (len(self.gcode.blocks) == 0):
            index = 1 
        else:
            index = len(self.gcode.blocks)-1
        self.gcode.insBlocks(index, blocks, "Text")
        self.refresh()

    #Remember to close Font
    font.close()
    self.notebook.select(1)
    self.canvas.fit2Screen()
    self.refresh()

    #Write GCode from glyph conrtours
def writeGlyphContour(self,block,font,contours,fontSize,depth,xO, yO, retractZ):
    #width = font.header.x_max - font.header.x_min
    #height = font.header.y_max - font.header.y_min
    scale = fontSize / font.header.units_per_em
    xO = xO * fontSize
    yO = yO * fontSize
    for cont in contours:
        #block.append(CNC.zsafe())
        block.append(CNC.zexit(retractZ))
        block.append(CNC.grapid(xO + cont[0].x * scale , yO + cont[0].y * scale))
        block.append(CNC.zenter(depth))
        block.append(CNC.gcode(1, [("f",CNC.vars["cutfeed"])]))
        for p in cont:
            block.append(CNC.gline(xO + p.x * scale, yO + p.y * scale))

def initializeGcodeforText(self, originX, originY, originZ):
    #custom header just for tags
    #headGcode = "$H \n $G \n G10L20P0X%sY%sZ%s \n G0X%s \n M3 \n S12000" %(originX, originY, originZ, (originX/2))
    # $H = means home the machine.  $G means View gcode parser state
    #headGcode = "$G \n G10L20P0X%sY%sZ%s \n G0X%s \n M3 \n S12000" %(originX, originY, originZ, (originX/2))

    #G10 L2 move a coordinate system relative to G53
    # P1 equals G54.
    headGcode = "$H \n $G \n G10L2P1X%sY%s \n G0X%s \n M3 \n S12000" %(-originX, -originY, (originX/2))
    self.gcode.header = headGcode
    #clear out any old tag information
    self.newFile(prompt = FALSE)

#def saveTagConfig(self):
#    Utils.setStr("Text", 'selectedfont', self.pfont.fontCombo.get())
#    Utils.setStr("Engraving", 'depth', self.engrave.depth.get())
#    Utils.setStr("Engraving", 'clearance', self.engrave.clearanceZ.get())
#    Utils.setStr("Engraving", 'retract', self.engrave.retractZ.get())























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


