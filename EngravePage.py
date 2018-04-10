# -*- coding: ascii -*-
# $Id$
#
# Author: vvlachoudis@gmail.com
# Date: 18-Jun-2015

__author__ = "Vasilis Vlachoudis"
__email__  = "vvlachoudis@gmail.com"

import os
from os import listdir
from os.path import isfile, join

try:
	from Tkinter import *
	import ttk
	import ConfigParser
except ImportError:
	from tkinter import *
	import configparser as ConfigParser

import tkExtra

import Utils
import Ribbon
import CNCRibbon
from CNC import CNC,Block

#===============================================================================
# Calculate Group
#===============================================================================
class CalculateGroup(CNCRibbon.ButtonGroup):
    def __init__(self, master, app):
        CNCRibbon.ButtonGroup.__init__(self, master, N_("Calculate"), app)
        self.grid3rows()

#		# ---
#		col,row=0,0
#		b = Ribbon.LabelButton(self.frame, #self.page, "<<Config>>",
#				text=_("Config"),
#				image=Utils.icons["config32"],
##				command=self.app.preferences,
#				state=DISABLED,
#				compound=TOP,
#				anchor=W,
#				background=Ribbon._BACKGROUND)
#		b.grid(row=row, column=col, rowspan=3, padx=0, pady=0, sticky=NS)
#		tkExtra.Balloon.set(b, _("Open configuration dialog"))

        # ===
        col,row=0,0
        b = Ribbon.LabelButton(self.frame,
                text=_("Calculate"),
                image=Utils.icons["gear32"],
                compound=TOP,
                anchor=W,
                command = app.drawText,
                background=Ribbon._BACKGROUND)
        b.grid(row=row, column=col, rowspan=3, padx=10, pady=10, sticky=NSEW)
        tkExtra.Balloon.set(b, _("Calculate G code"))	
        self.addWidget(b)	

        #col,row=1,0
        #b = Ribbon.LabelButton(self.frame,
        #        text=_("Engrave"),
        #        image=Utils.icons["gantry"],
        #        compound=TOP,
        #        anchor=W,
        #        #command = app.calculateGcode,
        #        background=Ribbon._BACKGROUND)
        #b.grid(row=row, column=col, rowspan=3, padx=10, pady=10, sticky=NSEW)
        #tkExtra.Balloon.set(b, _("Engrave"))	
        #self.addWidget(b)

#===============================================================================
# Font Frame
#===============================================================================
class FontFrame(CNCRibbon.PageLabelFrame):
    def __init__(self, master, app):
        CNCRibbon.PageLabelFrame.__init__(self, master, "Font", app)

        self.fontfile = StringVar()
        charspacing = IntVar()
        #wordspacing = IntVar()
        self.templateFile = StringVar()

        tagPath = os.path.join(Utils.prgpath, 'template')

        col,row=0,0
        b = Label(self, text=_("Template:"))
        b.grid(row=row,column=col,sticky=E)
        self.addWidget(b)

        templatefiles = [f for f in listdir(tagPath) if isfile(join(tagPath, f)) and f.endswith(".xml")]
        self.TemplateCombo = ttk.Combobox(self, width=16, textvariable=self.templateFile, values = templatefiles)
        self.TemplateCombo.grid(row=row, column=col+1, sticky=EW)
        tkExtra.Balloon.set(self.TemplateCombo, _("Select Template"))
        self.TemplateCombo.set(Utils.getStr("Text", 'selectedtemplate'))

        # ---
        row += 1
        col = 0
        b = Label(self, text=_("Font:"))
        b.grid(row=row,column=col,sticky=E)
        self.addWidget(b)

        #self.fontCombo = tkExtra.Combobox(self, False, background="White", width=16)
        fontPath = os.path.join(Utils.prgpath, 'fonts')
        fontFiles = [f for f in listdir(fontPath) if isfile(join(fontPath, f)) and f.endswith(".ttf")]
        #self.portCombo = tkExtra.Combobox(self, False, background="White", width=16)
        self.fontCombo = ttk.Combobox(self, width=16, textvariable=self.fontfile, values = fontFiles)
        self.fontCombo.grid(row=row, column=col+1, sticky=EW)
        tkExtra.Balloon.set(self.fontCombo, _("Select Font"))
        #self.portCombo.set(Utils.getStr("Connection","port"))
        self.fontCombo.set(Utils.getStr("Text", 'selectedfont'))
        self.addWidget(self.fontCombo)

        # ---
        #row += 1
        #col = 0
        #b = Label(self, text=_("Character Spacing:"))
        #b.grid(row=row,column=col,sticky=E)

        #col += 1
        ##self.charspacingentry = tkExtra.IntegerEntry(self, background="White", width=1, textvariable= charspacing)
        #self.charspacingentry = Entry(self, width=1, textvariable= charspacing)
        #self.charspacingentry.grid(row=row, column=col, sticky=EW)
        #tkExtra.Balloon.set(self.charspacingentry, _("Adjust Spacing between Characters"))
        ##self.charspacingentry.set(Utils.getStr("Text", 'charspacing'))
        #charspacing.set(Utils.getStr("Text", 'charspacing'))
        #self.addWidget(self.charspacingentry)

        ## ---
        #row += 1
        #col = 0
        #b = Label(self, text=_("Word Spacing:"))
        #b.grid(row=row,column=col,sticky=E)

        #col += 1
        #self.wordspacingentry = tkExtra.IntegerEntry(self, background="White", width=1)
        #self.wordspacingentry.grid(row=row, column=col, sticky=EW)
        #tkExtra.Balloon.set(self.wordspacingentry, _("Adjust Spacing between Words"))
        #self.wordspacingentry.set(Utils.getStr("Text", 'wordspacing'))
        #self.addWidget(self.wordspacingentry)

#===============================================================================
# Engraving Frame
#===============================================================================
class EngravingFrame(CNCRibbon.PageLabelFrame):
    def __init__(self, master, app):
        CNCRibbon.PageLabelFrame.__init__(self, master, "Engraving", app)

        self.clearanceZ = DoubleVar()
        self.retractZ = DoubleVar()
        self.depth = DoubleVar()
        
        # populate gstate dictionary
        self.gstate = {}	# $G state results widget dictionary
        #for k,v in DISTANCE_MODE.items():
        #    self.gstate[k] = (self.distance, v)

        # ---feedrate
        col,row=0,0
        b = Label(self, text=_("Feed Rate:"))
        b.grid(row=row,column=col,sticky=E)
        self.addWidget(b)

        col += 1
        self.feedrateentry = tkExtra.FloatEntry(self, background="White", width=20)
        self.feedrateentry.grid(row=row, column=col, sticky=EW)
        tkExtra.Balloon.set(self.feedrateentry, _("How Fast Tool moves while cutting"))
        self.feedrateentry.set(CNC.vars["cutfeed"])
        self.addWidget(self.feedrateentry)
        #TODO
        #for k,v in FEED_MODE.items(): self.gstate[k] = (self.feedMode, v)
        b = Label(self, text=_("mm/min"))
        b.grid(row=row,column=col+1,sticky=E)
        self.addWidget(b)

        # ---plungerate
        col=0
        row+=1
        b = Label(self, text=_("Plunge Rate:"))
        b.grid(row=row,column=col,sticky=E)
        self.addWidget(b)

        col += 1
        self.plungerateentry = tkExtra.FloatEntry(self, background="White", width=20)
        self.plungerateentry.grid(row=row, column=col, sticky=EW)
        tkExtra.Balloon.set(self.plungerateentry, _("How Fast Tool moves when plunging"))
        self.plungerateentry.set(CNC.vars["cutfeedz"])
        self.addWidget(self.plungerateentry)
        #TODO
        #for k,v in FEED_MODE.items(): self.gstate[k] = (self.feedMode, v)
        b = Label(self, text=_("mm/min"))
        b.grid(row=row,column=col+1,sticky=E)
        self.addWidget(b)

        # ---clearanceZ
        col=0
        row+=1
        b = Label(self, text=_("Clearance Height:"))
        b.grid(row=row,column=col,sticky=E)
        self.addWidget(b)

        col += 1
        self.clearanceZentry = tkExtra.FloatEntry(self, background="White", width=10, textvariable=self.clearanceZ)
        self.clearanceZentry.grid(row=row, column=col, sticky=EW)
        tkExtra.Balloon.set(self.clearanceZentry, _("Height above tag between letters"))
        self.clearanceZentry.set(Utils.getStr("Engraving", 'clearanceZ'))
        self.addWidget(self.clearanceZentry)
        #TODO
        #for k,v in FEED_MODE.items(): self.gstate[k] = (self.feedMode, v)
        b = Label(self, text=_("mm"))
        b.grid(row=row,column=col+1,sticky=E)
        self.addWidget(b)

        # ---retractZ
        col=0
        row+=1
        b = Label(self, text=_("Retract Height:"))
        b.grid(row=row,column=col,sticky=E)
        self.addWidget(b)

        col += 1
        self.retractZentry = tkExtra.FloatEntry(self, background="White", width=5, textvariable=self.retractZ)
        self.retractZentry.grid(row=row, column=col, sticky=EW)
        tkExtra.Balloon.set(self.retractZentry, _("Height above between Tags"))
        self.retractZentry.set(Utils.getStr("Engraving", 'retractZ'))
        self.addWidget(self.retractZentry)
        #TODO
        #for k,v in FEED_MODE.items(): self.gstate[k] = (self.feedMode, v)
        b = Label(self, text=_("mm"))
        b.grid(row=row,column=col+1,sticky=E)
        self.addWidget(b)

        # ---Engraving Depth
        col=0
        row+=1
        b = Label(self, text=_("Depth:"))
        b.grid(row=row,column=col,sticky=E)
        self.addWidget(b)

        col += 1
        self.depth = tkExtra.FloatEntry(self, background="White", width=5, textvariable=self.depth)
        self.depth.grid(row=row, column=col, sticky=EW)
        tkExtra.Balloon.set(self.depth, _("How Far to carve into piece"))
        self.depth.set(Utils.getStr("Engraving", 'depth'))
        self.addWidget(self.depth)
        #TODO
        #for k,v in FEED_MODE.items(): self.gstate[k] = (self.feedMode, v)
        b = Label(self, text=_("mm"))
        b.grid(row=row,column=col+1,sticky=E)
        self.addWidget(b)

#===============================================================================
# Tool Frame
#===============================================================================
#TODO

#===============================================================================
# Engrave Page
#===============================================================================
class EngravePage(CNCRibbon.Page):
	__doc__ = _("Engraving")
	_name_  = N_("Engraving")
	_icon_  = "gantry"

	#----------------------------------------------------------------------
	# Add a widget in the widgets list to enable disable during the run
	#----------------------------------------------------------------------
	def register(self):
		self._register((CalculateGroup, ),
			(FontFrame, EngravingFrame))