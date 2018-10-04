# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 14:07:50 2016
@author: jbm

"""

#! /usr/bin/env python

# pmont.py

# Version 0.12 Model-View-Controller style
# Date 23 March 2016
# Author: jbm
# Latest 21/09/2018  18:25
# Python 3.6 compatible
# Need to get bar graph working

import wx
# http://wiki.wxpython.org/WxLibPubSub
# pubsub changed with latest wxPython
if "2.8" in wx.version():
    import wx.lib.pubsub.setupkwargs
    from wx.lib.pubsub import pub
else:
    from wx.lib.pubsub import pub
import wx.aui
import sys
import locale
import os
import numpy as np
from wx.lib.wordwrap import wordwrap
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import math
import matplotlib as mpl
if os.name =='posix':
    mpl.use( 'WXAgg' )  # otherwise gets a segmentation fault under Linux
import matplotlib.pyplot as plt
import pylab

locale.setlocale( locale.LC_ALL, '' )
ID_BUTTON1 = wx.NewId()
ID_BUTTON2 = wx.NewId()
listOfVars = []
hlist =[]

class Model():
    # Define all the instance variables
    def __init__(self):
        self.sol = 500
        self.rn = 0
        self.u = 3
        self.airT = 15
        self.vp = 8
        self.rs = 30
        self.svp=17.04
        self.Td = 3.77
        self.Tw = 9.56  # initial dewpoint and wet-bulb temperatures
        self.esTw = 20   # temp to get MVC running
        self.NumSurfaceTypes = 8
        self.one = 1
        self.thisChoice = 0
        self.index = 0
        self.c1_svp = 6790.4985  # constant used in svp calculation
        self.c2_svp = 52.57633
        self.c3_svp = 5.02808
        # Initialize the vegetation types and their characteristics
        # SurfaceD holds Zero-Plane displacements in m
        self.SurfaceD = [0.15, 0.75, 10, 0.05, 0.0005, 0.15, 0.15, 10]
        # SurfaceZo holds roughness lengths
        self.SurfaceZo = [0.015, 0.075, 1, 0.005, 0.0005, 0.015, 0.015, 1]
        # Surfacers holds bulk surface resistance in s m-1
        self.SurfaceRs = [40, 40, 70, 100, 0.005, 100, 0.0001, 0.0001]
        # SurfaceA holds albedo values
        self.SurfaceA = [0.25, 0.25, 0.12, 0.2, 0.05, 0.25, 0.25, 0.12]
        self.SurfaceType = ["grass (dry)", "cereals (dry)", "conifers (dry)",
                            "bare soil (dry)", "water", "upland", "grass (wet)", "conifers (wet)"]
        self.absZero = 273.15        # Absolute zero
        self.stefanC = 0.0000000567  # Stefan-Boltzmann
        self.gamma = 0.66
        # psychrometric constant for temperatures in
        # degrees C and vapour pressures in mbar
        # need to make the next three temperature dependent
        self.cp = 1005   # specific heat of air (J kg-1)
        self.lhv = 2465000    # latent heat of vapourisation (J kg-1)
        self.rho = 1.204   # kg m-3 at 20 C
        self.vgList = [0, 1, 3, 4, 5, 6]
        self.LEControl = 0.0
        self.leBarData = [0, 0]
        self.dataset3 = np.empty(shape=[4, 3])

        #  svp data from Monteith & Unsworth, PEP, (2014) Table A4
        self.svpData = [
            [268.2,  4.21],  [269.2,  4.55],  [270.2,  4.90],  [271.2,  5.28],
            [272.2,  5.68],  [273.2,  6.11],  [274.2,  6.57],  [275.2,  7.05],
            [276.2,  7.58],  [277.2,  8.13],  [278.2,  8.72],  [279.2,  9.35],
            [280.2,  10.01], [281.2,  10.72], [282.2,  11.47], [283.2,  12.27],
            [284.2,  13.12], [285.2,  14.02], [286.2,  14.97], [287.2,  15.98],
            [288.2,  17.04], [289.2,  18.17], [290.2,  19.37], [291.2,  20.63],
            [292.2,  21.96], [293.2,  23.37], [294.2,  24.86], [295.2,  26.43],
            [296.2,  28.09], [297.2,  29.83], [298.2,  31.67], [299.2,  33.61],
            [300.2,  35.65], [301.2,  37.80], [302.2,  40.06], [303.2,  42.43],
            [304.2,  44.93], [305.2,  47.55], [306.2,  50.31], [307.2,  53.20]
        ]
        '''
        self.jsonSurfaces = [
            [ "albedo": 0.25, "Rs": 40, "zo": 0.015, "D": 0.15, "SurfaceType": "grass (dry)"    ],
            [ "albedo": 0.25, "Rs": 40, "zo": 0.075, "D": 0.75, "SurfaceType": "cereals (dry)"  ],
            [ "albedo": 0.12, "Rs": 70, "zo": 1,     "D": 10,   "SurfaceType": "conifers (dry)" ],
            [ "albedo": 0.2,  "Rs": 100,"zo": 0.005, "D": 0.05, "SurfaceType": "bare soil (dry)"],
            [ "albedo": 0.05, "Rs": 0.0005, "zo": 0.015, "D": 0.0005, "SurfaceType": "water"    ],
            [ "albedo": 0.25, "Rs": 100, "zo": 0.015, "D": 0.15,  "SurfaceType": "upland"       ],
            [ "albedo": 0.25, "Rs": 0.0001, "zo": 0.015, "D": 0.15, "SurfaceType": "grass (wet)"],
            [ "albedo": 0.12, "Rs": 0.0001, "zo": 1, "D": 10,   "SurfaceType": "conifers (wet)" ]
        ]
        '''
        self.parcel = [                      # point coordinates:
            [self.airT+273.15, self.vp],     # airT, vp
            [self.airT+273.15, 17.04],       # airT, svp
            [self.Tw+273.15, self.esTw],     # Tw, esTw
            [self.Td+273.15, self.vp]        # Td, vp
        ]

        # Get the data from the various text boxes if they have been entered manually
        # in the VIEW and fire off a message to say things have changed.
        # You'll then need to recalculate all the related data.

    def setSOLAR(self, value):
        self.sol = float(value)
        # now tell anyone who cares that the value has been changed
        pub.sendMessage('SOLAR.CHANGED', value=self.sol)
        self.calculateLE(self.sol, self.airT, self.u, self.vp, self.rs)

    def setWIND(self, value):
        self.u = float(value)
        # now tell anyone who cares that the value has been changed
        pub.sendMessage('WIND.CHANGED', value=self.u)
        self.calculateLE(self.sol, self.airT, self.u, self.vp, self.rs)

    def setVP(self, value):
        self.vp = float(value)
        # now tell anyone who cares that the value has been changed
        pub.sendMessage('VP.CHANGED', value=self.vp)
        self.calculateLE(self.sol, self.airT, self.u, self.vp, self.rs)

    def setAIRT(self, value):
        self.airT = float(value)
        # now tell anyone who cares that the value has been changed
        pub.sendMessage('AIRT.CHANGED', value=self.airT)
        self.calculateLE(self.sol, self.airT, self.u, self.vp, self.rs)

    def setRS(self, value):
        self.rs = float(value)
        # now tell anyone who cares that the value has been changed
        pub.sendMessage('RESISTANCE.CHANGED', value=self.rs)
        self.calculateLE(self.sol, self.airT, self.u, self.vp, self.rs)

    def c_ra(self,index,u):
            # calculates aerodynamic resistances
            # using eqns. 4.36 and 4.38 of MORECS report
        if self.index in self.vgList:
            self.ra = (6.25/self.u)*math.log10(10/self.SurfaceZo[self.index])*math.log10(6/self.SurfaceZo[self.index])
        else:
            self.ra = 94/self.u
        return self.ra
        
    def calculateLE(self, sol, airT, u, vp, rs):
        self.sol = sol
        self.airT = airT
        self.rs = rs
        self.u = u
        self.vp = vp
        # thisChoice=adjustVeg();  console.log("index= ",thisChoice);
        self.albedo = self.SurfaceA[self.thisChoice]
        self.ra = self.c_ra(self.thisChoice, self.u)
        self.rs = self.SurfaceRs[self.thisChoice]
        self.nets = self.c_netShortwave()
        self.netl = self.c_netLongwave()
        self.rn = self.c_netRadiation()

        #print('Net Radiation = {0:6.0f}'.format(self.rn))
        self.svp = self.c_satVapPres(self.airT)
        self.rh =self. c_rh()
        self.delta = self.c_delta()
        #print('delta = {0:6.1f}'.format(self.delta))
        if self.vp >= self.svp:
            self.vp = self.svp
        self.vpd = self.svp - self.vp
        self.LE = (self.delta * self.rn + self.rho * self.cp * (self.svp - self.vp)/self.ra)\
            / (self.delta + self.gamma * (1 + self.rs / self.ra))
        self.mmPerDay = self.LE * 0.035
        self.hlist = [self.nets, self.netl, self.rn, self.LE]
        self.showStats()

        # Send message to View
        pub.sendMessage("LE.CHANGED", value=self.LE)
        pub.sendMessage("RA.CHANGED", value=self.ra)
        pub.sendMessage("RN.CHANGED", value=self.rn)
        pub.sendMessage("RH.CHANGED", value=self.rh)
        pub.sendMessage("SVP.CHANGED", value=self.svp)
        pub.sendMessage("NETS.CHANGED", value=self.nets)
        pub.sendMessage("NETL.CHANGED", value=self.netl)
        pub.sendMessage("DATA.CHANGED", value=self.hlist)

        self.leBarData[0] = round(self.LEControl)
        self.leBarData[1] = round(self.LE)
        # print("leBarData[0] =" ,self.leBarData[0])
        # print("leBarData[1] =" ,self.leBarData[1])
        self.dataset1=self.leBarData
        self.dataset3[0][0] = self.airT + 273.15
        self.dataset3[0][1] = self.vp
        self.dataset3[1][0] = self.airT + 273.15
        self.dataset3[1][1] = self.svp
        self.dataset3[2][0] = self.Tw + 273.15
        self.dataset3[2][1] = self.esTw
        self.dataset3[3][0] = self.Td + 273.15
        self.dataset3[3][1] = self.vp
        '''self.dataset4 = [
            ["x": self.airT+273.15, "y": self.vp ],
            ["x": self.airT+273.15, "y": self.svp ],
            ["x": self.airT+273.15, "y": self.vp ],
            ["x": self.Tw+273.15, "y": self.esTw ],
            ["x": self.airT+273.15, "y": self.vp ],
            ["x": self.Td+273.15, "y": self.vp ]
            ]
        '''
        # redrawLE()
        return

    def c_netShortwave(self):
        # calculates net shortwave radiation
        return (1 - self.SurfaceA[self.index]) * self.sol

    def c_netLongwave(self):
        # calculates net longwave radiation at surface
        # using eqn 4.22 in MORECS and clear skies !
        factor = 0.95 * self.stefanC * math.pow(self.airT+self.absZero,4)
        return factor * (1.28 * (math.pow(self.vp/(self.airT+self.absZero),0.142857))-1)
 
    def c_netRadiation(self):
            # calculates net all-wave radiation
        return self.nets + self.netl
      
    def c_satVapPres(self, airT):
        # calculates saturation vapour pressure (mbar)
        return 10 * math.exp(self.c2_svp - ((self.c1_svp / (airT + self.absZero)) +
                                            self.c3_svp * math.log(airT + self.absZero)))

    def c_rh(self):
        # calculates relative humidity
        if self.vp >= self.svp:
            return 100.0
        else:
            return (self.vp / self.svp) * 100

    def c_delta(self):
        # calculates slope of svp curve
        tup = self.airT + 0.5  # add half a degree to air temperature
        tlo = self.airT - 0.5  # subtract half a degree from air temperature
        return self.c_satVapPres(tup) - self.c_satVapPres(tlo)
        
    def dewpoint(self):
        factor = math.log(self.vp / 6.112)
        return 243.5 * factor/(17.67-factor)

    # Wet bulb from http://www.the-snowman.com/wetbulb2.html
    def wetbulb(self):
        self.rh = (self.vp / self.svp) * 100
        return (-5.806 + 0.672 * self.airT - 0.006 * self.airT * self.airT +
                (0.061 + 0.004 * self.airT + 0.000099 * self.airT * self.airT) *
                self.rh + (-0.000033 - 0.000005 * self.airT
                           - 0.0000001 * self.airT * self.airT) * self.rh * self.rh)
            
    def showStats(self):
        return


class View(wx.Frame):
    from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
    """The main frame of the application
    """

    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, -1)
        self.create_menu()
        # Main left hand panel housing the Figure and Output panels
        self.LH_main_panel = wx.Panel(self, -1, style=wx.RAISED_BORDER)
        self.LH_main_panel.SetBackgroundColour('white')
        # display panel ie where the graphics goes
        self.LH_display_panel = wx.Panel(self, -1, style=wx.RAISED_BORDER)
        self.LH_display_panel.SetBackgroundColour('red')
        # output panel ie the results of the calculation and below the figure
        self.LH_output_panel = wx.Panel(self, -1, style=wx.RAISED_BORDER)
        self.LH_output_panel.SetBackgroundColour('#DCDCDC')  # Gainsboro
        # control Panel -  i.e. the sliders, textboxes etc
        self.RH_control_panel = wx.Panel(self, -1, style=wx.RAISED_BORDER)
        self.RH_control_panel.SetBackgroundColour('#DCDCDC')  # Gainsboro
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(self.LH_main_panel, 5, wx.EXPAND, border=20)
        main_sizer.Add(self.RH_control_panel, 5, wx.EXPAND, border=20)

        self.SetSizer(main_sizer)
        # self.Maximize(True)

        self.btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.LH_display_panel.figure = Figure()
        self.LH_display_panel.canvas = FigureCanvas(self.LH_display_panel, 1, self.LH_display_panel.figure)
        self.axes1 = self.LH_display_panel.figure.add_subplot(111)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vboxOP = wx.BoxSizer(wx.VERTICAL)
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hboxCB = wx.BoxSizer(wx.HORIZONTAL)

        # Right-Hand CONTROL PANEL #

        self.gridSizer = wx.GridSizer(rows=5, cols=1, hgap=5, vgap=5)
        self.vboxCP = wx.BoxSizer(wx.VERTICAL)
        self.okBtn = wx.Button(self.RH_control_panel, wx.ID_ANY, 'OK')
        self.cancelBtn = wx.Button(self.RH_control_panel, wx.ID_ANY, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.onOK, self.okBtn)
        self.Bind(wx.EVT_BUTTON, self.onCancel, self.cancelBtn)
        # Declare Input text boxes
        self.SOLARText = wx.TextCtrl(self.RH_control_panel, style=wx.TE_PROCESS_ENTER)
        self.WINDText = wx.TextCtrl(self.RH_control_panel, style=wx.TE_PROCESS_ENTER)
        self.RSText = wx.TextCtrl(self.RH_control_panel, style=wx.TE_PROCESS_ENTER)
        self.AIRTText = wx.TextCtrl(self.RH_control_panel, style=wx.TE_PROCESS_ENTER)
        self.VPText = wx.TextCtrl(self.RH_control_panel, style=wx.TE_PROCESS_ENTER)

        # declare controls
        # wx.Slider(parent, id, value, minValue, maxValue, pos, size, style)
        self.solarSlider = wx.Slider(
            self.RH_control_panel, 100, 500, 1, 1000, (30, 60), (200, -1),
            wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
        )
        self.airTSlider = wx.Slider(
            self.RH_control_panel, 100, 15, -5, 35, (30, 60), (200, -1),
            wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
        )
        self.vpSlider = wx.Slider(
            self.RH_control_panel, 100, 5, 1, 45, (30, 60), (200, -1),
            wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
        )
        self.rsSlider = wx.Slider(
            self.RH_control_panel, 100, 5, 1, 95, (30, 60), (200, -1),
            wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
        )
        self.uSlider = wx.Slider(
            self.RH_control_panel, 100, 5, 1, 25, (30, 60), (200, -1),
            wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
        )

        self.inputSolarSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.inputairTSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.inputvpSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.inputrsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.inputuSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.labelSolar = wx.StaticText(self.RH_control_panel, wx.ID_ANY, 'Solar')
        self.inputSolarSizer.Add(self.labelSolar, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.inputSolarSizer.Add(self.SOLARText, 0, wx.ALL, 5)
        self.inputSolarSizer.Add(self.solarSlider, 0, wx.ALL, 5)
        self.labelairT = wx.StaticText(self.RH_control_panel, wx.ID_ANY, 'Air T')
        self.inputairTSizer.Add(self.labelairT, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.inputairTSizer.Add(self.AIRTText, 0, wx.ALL, 5)
        self.inputairTSizer.Add(self.airTSlider, 0, wx.ALL, 5)
        self.labelvp = wx.StaticText(self.RH_control_panel, wx.ID_ANY, 'VP')
        self.inputvpSizer.Add(self.labelvp, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.inputvpSizer.Add(self.VPText, 0, wx.ALL, 5)
        self.inputvpSizer.Add(self.vpSlider, 0, wx.ALL, 5)
        self.labelrs = wx.StaticText(self.RH_control_panel, wx.ID_ANY, 'RS')
        self.inputrsSizer.Add(self.labelrs, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.inputrsSizer.Add(self.RSText, 0, wx.ALL, 5)
        self.inputrsSizer.Add(self.rsSlider, 0, wx.ALL, 5)
        self.labelu = wx.StaticText(self.RH_control_panel, wx.ID_ANY, 'wind')
        self.inputuSizer.Add(self.labelu, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.inputuSizer.Add(self.WINDText, 0, wx.ALL, 5)
        self.inputuSizer.Add(self.uSlider, 0, wx.ALL, 5)

        self.gridSizer.Add(self.inputSolarSizer, 0, wx.ALIGN_RIGHT)
        self.gridSizer.Add(self.inputairTSizer, 0, wx.ALIGN_RIGHT)
        self.gridSizer.Add(self.inputvpSizer, 0, wx.ALIGN_RIGHT)
        self.gridSizer.Add(self.inputrsSizer, 0, wx.ALIGN_RIGHT)
        self.gridSizer.Add(self.inputuSizer, 0, wx.ALIGN_RIGHT)

        self.btnSizer.Add(self.okBtn, 0, wx.ALL, 5)
        self.btnSizer.Add(self.cancelBtn, 0, wx.ALL, 5)
        self.cbx = wx.ComboBox(self.RH_control_panel, -1, choices=listOfVars, style=wx.CB_READONLY)
        self.hboxCB.Add(self.cbx)
        self.vboxCP.Add(wx.StaticLine(self.RH_control_panel), 0, wx.ALL | wx.EXPAND, 5)
        self.vboxCP.Add(self.gridSizer, 0, wx.ALL | wx.EXPAND, 5)
        self.vboxCP.Add(wx.StaticLine(self.RH_control_panel), 0, wx.ALL | wx.EXPAND, 5)

        self.vboxCP.Add(wx.StaticLine(self.RH_control_panel), 0, wx.ALL | wx.EXPAND, 5)
        self.vboxCP.Add(self.btnSizer, 0, wx.ALL | wx.CENTER, 5)
        self.vboxCP.Add(wx.StaticLine(self.RH_control_panel), 0, wx.ALL | wx.EXPAND, 5)
        self.RH_control_panel.SetSizer(self.vboxCP)

        # OUTPUT PANEL #
        # # Declare Output text boxes
        self.LEText = wx.TextCtrl(self.LH_output_panel, style=wx.TE_PROCESS_ENTER)
        self.SVPText = wx.TextCtrl(self.LH_output_panel, style=wx.TE_PROCESS_ENTER)
        self.RHText = wx.TextCtrl(self.LH_output_panel, style=wx.TE_PROCESS_ENTER)
        self.RAText = wx.TextCtrl(self.LH_output_panel, style=wx.TE_PROCESS_ENTER)
        self.RNText = wx.TextCtrl(self.LH_output_panel, style=wx.TE_PROCESS_ENTER)
        self.NETSText = wx.TextCtrl(self.LH_output_panel, style=wx.TE_PROCESS_ENTER)
        self.NETLText = wx.TextCtrl(self.LH_output_panel, style=wx.TE_PROCESS_ENTER)

        # # horizontal boxsizer: http://www.rqna.net/qna/vtvnh-how-to-implement-a-wx-textctrl-in-a-wx-gridbagsizer.html
        def addWithLabel(parent, label, wxCtrl):
            sz_h1 = wx.BoxSizer(wx.HORIZONTAL)
            txt = wx.StaticText(parent, -1, label)
            sz_h1.Add(txt)
            sz_h1.Add(wxCtrl)
            return sz_h1

        self.vboxOP.Add(addWithLabel(self.LH_output_panel, "P-M Evaporation: ", self.LEText))
        self.vboxOP.Add(addWithLabel(self.LH_output_panel, "Relative Humidity: ", self.RHText))
        self.vboxOP.Add(addWithLabel(self.LH_output_panel, "Saturation Vapour Pressure: ", self.SVPText))
        self.vboxOP.Add(addWithLabel(self.LH_output_panel, "Aerodynamic Resistance: ", self.RAText))
        self.vboxOP.Add(addWithLabel(self.LH_output_panel, "Net Radiation: ", self.RNText))
        self.vboxOP.Add(addWithLabel(self.LH_output_panel, "Net Solar Radiation: ", self.NETSText))
        self.vboxOP.Add(addWithLabel(self.LH_output_panel, "Net Longwave Radiation: ", self.NETLText))
        self.LH_output_panel.SetSizer(self.vboxOP)

        self.vbox.Add(self.LH_display_panel, 4.0, wx.EXPAND | wx.ALL, 5)  # proportion 2
        self.hbox.Add(self.RH_control_panel, 1.0, wx.EXPAND | wx.ALL, 5)  # proportion 1
        self.vbox.Add(self.LH_output_panel, 4.0, wx.EXPAND | wx.ALL, 5)  # proportion 1

        self.SetSize((950, 700))
        self.SetTitle('Model of Penman Monteith Evaporation')
        self.SetSizer(self.hbox)
        self.SetSizer(self.vbox)
        self.Centre()
        self.statusbar = self.CreateStatusBar()
        #self.redraw_plot(hlist)

    def setSOLAR(self, text2):
        self.SOLARText.SetValue(str(text2))
        return

    def setAIRT(self, text2):
        self.AIRTText.SetValue('{:6.2}'.format(str(text2)))
        return

    def setRS(self, text2):
        self.RSText.SetValue(str(text2))
        return

    def setWIND(self, text3):
        self.WINDText.SetValue(str(text3))
        return

    def setVP(self, text3):
        self.VPText.SetValue(str(text3))
        return

    def setLE(self, text3):
        self.LEText.SetValue('{:6.4}'.format(str(text3)))
        return

    def setSVP(self, text3):
        self.SVPText.SetValue('{:6.4}'.format(str(text3)))
        return

    def setRH(self, text3):
        self.RHText.SetValue('{:6.4}'.format(str(text3)))
        return

    def setRN(self, text3):
        self.RNText.SetValue('{:8.4}'.format(str(text3)))
        return

    def setRA(self, text3):
        self.RAText.SetValue('{:8.4}'.format(str(text3)))
        return

    def setNETS(self, text3):
        self.NETSText.SetValue('{:8.4}'.format(str(text3)))
        return

    def setNETL(self, text3):
        self.NETLText.SetValue('{:8.4}'.format(str(text3)))
        return

    def setDATA(self, hlist):
        self.hlist = hlist
        #print('hlist = {:8.4} {:8.4} {:8.4} {:8.4}'.format(self.hlist))
        print('In View ', self.hlist)
        self.redraw_plot(self.hlist)
        return

    def create_menu(self):
        menubar = wx.MenuBar()
        file = wx.Menu()
        edit = wx.Menu()
        help = wx.Menu()
        file.Append(101, '&Open', 'Open a new document')
        file.Append(102, '&Save', 'Save the document')
        file.AppendSeparator()
        quit = wx.MenuItem(file, 105, '&Quit\tCtrl+Q', 'Quit the Application')
        # quit.SetBitmap(wx.Image('stock_exit-16.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        file.Append(quit)
        edit.Append(201, 'check item1', '', wx.ITEM_CHECK)
        edit.Append(202, 'check item2', kind=wx.ITEM_CHECK)
        submenu = wx.Menu()
        submenu.Append(301, 'radio item1', kind=wx.ITEM_RADIO)
        submenu.Append(302, 'radio item2', kind=wx.ITEM_RADIO)
        submenu.Append(303, 'radio item3', kind=wx.ITEM_RADIO)
        edit.Append(203, 'submenu', submenu)
        menubar.Append(file, '&File')
        menubar.Append(edit, '&Edit')
        menubar.Append(help, '&Help')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=105)
        return

    def OnNew(self, event):
        self.statusbar.SetStatusText('New Command')

    def OnOpen(self, event):
        self.statusbar.SetStatusText('Open Command')

    def OnSave(self, event):
        self.statusbar.SetStatusText('Save Command')

    def OnExit(self, event):
        self.Close()

    def init_plot(self):
        # The Radiation and Energy balance figures
        self.axes1.set_facecolor('lightgrey')
        self.axes1.set_title('Energy Balance', size=10)
        self.axes1.set_xlim(0, 4)
        self.axes1.set_ylim(-50, 800)
        x = range(4)
        self.axes1.set_xticks(x)
        self.axes1.set_xticklabels(['   NetS', '  Rn', '  NetL', '  LE'])
        self.axes1.set_ylabel(' Energy Flux Density (Wm-2)')
        pylab.setp(self.axes1.get_xticklabels(), fontsize=10)
        # plot the data as a bar, and save the reference
        # to the plotted bar series
        #
        #self.barplot1 = self.axes1.bar(range(len(self.data2)), self.data2)
        #self.barplot2 = self.axes2.bar(range(len(self.data3)), self.data3)
        plt.show()

    def redraw_plot(self, hlist):
        """ Redraws the plots
        """
        #fig = plt.figure()
        #self.axes1 = fig.gca()
        #self.axes1 = fig.add_subplot(111)
        N = 4    # 4 fluxes to show
        ## necessary variables
        ind = np.arange(N)  # the x locations for the groups
        width = 0.35  # the width of the bars
        self.hlist=hlist
        rects1 = self.axes1.bar(ind, self.hlist, width, align='center')
        self.axes1.set_xlim(-width, len(ind) + width)
        self.axes1.set_ylim(-50, 950)
        self.hlist = hlist
        print('In redraw plot ', self.hlist)
        self.axes1.set_title('Energy Balance')
        self.axes1.set_ylabel('Energy Flux Density (Wm-2)')
        fluxes = ('Net Solar', 'Net Longwave', 'Net Radiation', 'Evaporation')
        self.axes1.set_xticks(ind + width)
        xticknames = self.axes1.set_xticklabels(fluxes)
        plt.setp(xticknames, rotation=45, fontsize=10)
        # y_pos = np.arange(len(fluxes))
        # self.axes1.bar(y_pos, self.hlist, align='center', alpha=0.5)
        # self.axes1.set_xticks(y_pos, fluxes)
        # self.axes1.bar(y_pos, self.hlist, align='center', linewidth=10, color=(1, 0, 0))
        # self.axes1.set_ylabel('Energy Flux Density (Wm-2)')
        plt.show()

    def OnButton(self, event):
        """Called when the Reset Button is clicked"""
        event_id = event.GetId()
        event_obj = event.GetEventObject()
        if event_id == -2024:     # needs to be flexible 999999
            self.statusbar.SetStatusText("Reset Button Clicked")
            pub.sendMessage("RESET.CLICKED")
        print("ID=%d" % event_id)
        print("object=%s" % event_obj.GetLabel())

    def OnChoice(self, event):
        selection = self.choice.GetStringSelection()
        index = self.choice.GetSelection()
        print("Selected Item: %d '%s'" % (index, selection))

    def OnQuit(self, event):
        dlg = wx.MessageDialog(self, "Do you really want to close "
                                     "this application?",
                               "Confirm Exit",
                               wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()
            sys.exit(0)

    def onAboutDlg(self, event):
        info = wx.AboutDialogInfo()
        info.Name = "Penman-Monteith Evaporation Model"
        info.Version = "0.5"
        info.Copyright = "(C) 2016 School of GeoSciences"
        info.Description = wordwrap(
            "This is a Penman-Monteith model based on the FAO (1989), The model is written in Python "
            "(3.6) and wxPython (4.0)",
            350, wx.ClientDC(self))
        info.WebSite = ("http://www.geos.ed.ac.uk", "School Home Page")
        info.Developers = ["John Moncrieff"]
        info.License = wordwrap("GNU Open Source", 500,
                            wx.ClientDC(self))
        # Show the wx.AboutBox
        wx.AboutBox(info)

    def OnAbout2(self, event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, "Penman-Monteith Model",
                               "About PM", wx.OK)
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.

    def OnHowTo(self, event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, "Control is via the ComboBoxes ... ",
                               "About PM", wx.OK)
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.

    def vibrate(self, win, count=20, delay=50):
        if count == 0:
            return
        x, y = win.GetPositionTuple()
        # print x,y
        dx = 2 * count * (.5 - count % 2)
        win.SetPosition((x+dx, y))
        wx.CallLater(delay, vibrate, win, count-1, delay)

    def OnCloseWindow(self, event):
        # self.Destroy()
        sys.exit(0)

    def onOK(self, event):
        # Do something
        print('onOK handler')

    def onCancel(self, event):
        self.closeProgram()


class Controller:
    def __init__(self, app):
        # Create a new MODEL object
        self.model = Model()
        # Create a new VIEW object
        self.view = View()

        # Bind evts to sliders
        self.view.airTSlider.Bind(wx.EVT_SLIDER, self.airTSliderevent)
        self.view.solarSlider.Bind(wx.EVT_SLIDER, self.solarSliderevent)
        self.view.uSlider.Bind(wx.EVT_SLIDER, self.uSliderevent)
        self.view.vpSlider.Bind(wx.EVT_SLIDER, self.vpSliderevent)
        self.view.rsSlider.Bind(wx.EVT_SLIDER, self.rsSliderevent)

        # This is the V3 model for PubSub
        # First parameter = the name of the Handler function doing the work
        # Second parameter = the name of the Message being broadcast
        pub.subscribe(self.ResetClicked, 'RESET.CLICKED')
        pub.subscribe(self.SOLARChanged, 'SOLAR.CHANGED')
        pub.subscribe(self.WINDChanged, 'WIND.CHANGED')
        pub.subscribe(self.RSChanged, "RESISTANCE.CHANGED")
        pub.subscribe(self.AIRTChanged, "AIRT.CHANGED")
        pub.subscribe(self.VPChanged, "VP.CHANGED")
        pub.subscribe(self.LEChanged, "LE.CHANGED")
        pub.subscribe(self.RHChanged, "RH.CHANGED")
        pub.subscribe(self.SVPChanged, "SVP.CHANGED")
        pub.subscribe(self.RAChanged, "RA.CHANGED")
        pub.subscribe(self.RNChanged, "RN.CHANGED")
        pub.subscribe(self.NETSChanged, "NETS.CHANGED")
        pub.subscribe(self.DATAChanged, "DATA.CHANGED")

        self.view.Show(True)
    
    def solarSliderevent(self, event):
        sol = self.view.solarSlider.GetValue()
        self.model.setSOLAR(sol)

    def airTSliderevent(self, event):
        airT = self.view.airTSlider.GetValue()
        self.model.setAIRT(airT)

    def uSliderevent(self, event):
        u = self.view.uSlider.GetValue()
        self.model.setWIND(u)

    def vpSliderevent(self, event):
        vp = self.view.vpSlider.GetValue()
        self.model.setVP(vp)

    def rsSliderevent(self, event):
        rs = self.view.rsSlider.GetValue()
        self.model.setRS(rs)

    def ResetClicked(self):
        """
        This method is the handler for "START CLICKED" messages,
        which pubsub will call as messages are sent from the view Start button.
        """
        print('Reset Button detected - resetting to default model')
        self.model.onReset()

    def SOLARChanged(self, value):
        """
        This method is the handler for "SOLAR CHANGED" messages,
        which pubsub will call as messages are sent from the model.
        """
        self.view.setSOLAR(str(value))

    def WINDChanged(self, value):
        """
        This method is the handler for "WIND CHANGED" messages,
        which pubsub will call as messages are sent from the model.
        """
        self.view.setWIND(str(value))

    def RSChanged(self, value):
        """
        This method is the handler for "RESISTANCE CHANGED" messages,
        which pubsub will call as messages are sent from the model.
        """
        self.view.setRS(str(value))

    def AIRTChanged(self, value):
        """
        This method is the handler for "AIRT CHANGED" messages,
        which pubsub will call as messages are sent from the model.
        """
        self.view.setAIRT(str(value))

    def VPChanged(self, value):
        """
        This method is the handler for "AIRT CHANGED" messages,
        which pubsub will call as messages are sent from the model.
        """
        self.view.setVP(str(value))

    def LEChanged(self, value):
        """
        This method is the handler for "LE CHANGED" messages,
        which pubsub will call as messages are sent from the model.
        """
        self.view.setLE(str(value))

    def SVPChanged(self, value):
        """
        This method is the handler for "SVP CHANGED" messages,
        which pubsub will call as messages are sent from the model.
        """
        self.view.setSVP(str(value))

    def RHChanged(self, value):
        """
        This method is the handler for "RH CHANGED" messages,
        which pubsub will call as messages are sent from the model.
        """
        self.view.setRH(str(value))

    def RNChanged(self, value):
        """
        This method is the handler for "RN CHANGED" messages,
        which pubsub will call as messages are sent from the model.
        """
        self.view.setRN(str(value))

    def NETSChanged(self, value):
        """
        This method is the handler for "NETS CHANGED" messages,
        which pubsub will call as messages are sent from the model.
        """
        self.view.setNETS(str(value))

    def NETLChanged(self, value):
        """
        This method is the handler for "NETL CHANGED" messages,
        which pubsub will call as messages are sent from the model.
        """
        self.view.setNETL(str(value))

    def DATAChanged(self, value):
        """
        This method is the handler for "NETL CHANGED" messages,
        which pubsub will call as messages are sent from the model.
        """
        self.view.setDATA(str(value))

    def RAChanged(self, value):
        """
        This method is the handler for "RA CHANGED" messages,
        which pubsub will call as messages are sent from the model.
        """
        self.view.setRA(str(value))

if __name__ == "__main__":
    app = wx.App(False)
    controller = Controller(app)
    # open a splash screen if it exists

    #if os.path.exists(SPLASH_SCREEN_FILENAME):
    #    splash_image = wx.Image(SPLASH_SCREEN_FILENAME, wx.BITMAP_TYPE_ANY, -1)
    #    wx.SplashScreen(splash_image.ConvertToBitmap(),
    #                    wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
    #                    4000,
    #                    None, -1)
    app.MainLoop()