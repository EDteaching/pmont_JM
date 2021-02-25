"""
Created: Tuesday 1st December 2020
@author: John Moncrieff (j.moncrieff@ed.ac.uk)
Last Modified on 23 Feb 2021 21:08 

DESCRIPTION
===========
This package contains the class object for the view in 
the pmont Jupyter notebook

"""
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.lines as mlines
import math
import numpy as np
import matplotlib.pyplot as plt


class View():    
    def __init__(self, rblist, eblist):
        self.svpData = [
            [268.2, 4.21], [269.2, 4.55], [270.2, 4.90], [271.2, 5.28],
            [272.2, 5.68], [273.2, 6.11], [274.2, 6.57], [275.2, 7.05],
            [276.2, 7.58], [277.2, 8.13], [278.2, 8.72], [279.2, 9.35],
            [280.2, 10.01], [281.2, 10.72], [282.2, 11.47], [283.2, 12.27],
            [284.2, 13.12], [285.2, 14.02], [286.2, 14.97], [287.2, 15.98],
            [288.2, 17.04], [289.2, 18.17], [290.2, 19.37], [291.2, 20.63],
            [292.2, 21.96], [293.2, 23.37], [294.2, 24.86], [295.2, 26.43],
            [296.2, 28.09], [297.2, 29.83], [298.2, 31.67], [299.2, 33.61],
            [300.2, 35.65], [301.2, 37.80], [302.2, 40.06], [303.2, 42.43],
            [304.2, 44.93], [305.2, 47.55], [306.2, 50.31], [307.2, 53.20]
        ]
        # Just some temporary values to provide initial plot
        # Does this go here or in Model?
        self.airT = 292.2
        self.vp = 11.47
        self.svp = 21.96
        self.Td = 282.2
        self.Tw = 9.56 + 273.15   # initial dewpoint and wet-bulb temperatures
        self.esTw = 20  # temp to get MVC running
        self.esTd = 10
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3)
        N = 4  # 4 fluxes to show
        ## necessary variables
        self.ind = np.arange(N)  # the x locations for the groups
        self.width = 0.8  # the width of the bars
         # Temporarily fill a list of energy balance values
        self.RBlist = rblist
        self.rects = self.ax1.bar(self.ind, self.RBlist, self.width, align='center')
        self.rects[0].set_color('yellow')
        self.rects[1].set_color('yellow')
        self.rects[2].set_color('black')
        self.rects[3].set_color('darkgray')
        self.ax1.set_xlim(None, len(self.ind) + self.width)
        self.ax1.set_ylim(-200, 1000)
        self.ax1.set_facecolor('lightgrey')
        self.ax1.grid(axis='both')
        self.ax1.set_title('Radiation Balance')
        self.ax1.set_ylabel('Energy Flux Density (W m$^{-2}$)')
        fluxes = ('Incoming Solar', 'Reflected Solar', 'Downward Longwave', 'Emitted Longwave')
        self.ax1.set_xticks(self.ind + self.width)
        #xticknames = self.axes1.set_xticklabels(fluxes)
        self.ax1.set_xticklabels(fluxes,rotation=0, rotation_mode="anchor", ha="right", size=10)

        # Figure 2 - Energy Balance
        self.EBlist = eblist
        self.rects2 = self.ax2.bar(self.ind, self.EBlist, self.width, align='center')
        self.rects2[0].set_color('black')
        self.rects2[1].set_color('red')
        self.rects2[2].set_color('blue')
        self.rects2[3].set_color('brown')
        self.ax2.set_xlim(None, len(self.ind) + self.width)
        self.ax2.set_ylim(-200, 1000)
        self.ax2.set_facecolor('lightgrey')
        self.ax2.grid(axis='both')
        self.ax2.set_title('Energy Balance')
        self.ax2.set_ylabel('Energy Flux Density (W m$^{-2}$)')
        fluxes2 = ('Net Radiation', 'Sensible Heat', 'Latent Heat', 'Soil Heat')
        self.ax2.set_xticks(self.ind + self.width)
        # xticknames = self.axes1.set_xticklabels(fluxes)
        self.ax2.set_xticklabels(fluxes2, rotation=0, rotation_mode="anchor", ha="right", size=10)

        # Figure 3 - SVP Figure
        self.x_list = [l[0] for l in self.svpData]
        self.y_list = [l[1] for l in self.svpData]
        self.ax3.set_xlim(265, 310)
        self.ax3.set_ylim(4, 54)
        self.ax3.set_facecolor('lightgrey')
        self.ax3.grid(axis='both')
        self.ax3.set_title('Saturation Vapour Pressure vs Air Temperature')
        self.ax3.set_ylabel('SVP (hPa or mbar')
        self.ax3.plot(self.x_list, self.y_list)
        self.ax3.plot(self.airT, self.vp, 'bo')
        
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

    def setCBX(self, text3):
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

    def setTW(self, text3):
        self.TWText.SetValue('{:8.4}'.format(str(text3)))
        return

    def setTD(self, text3):
        self.TDText.SetValue('{:8.4}'.format(str(text3)))
        return

    def setDATA(self, EBlist, Tlist):
        self.EBlist = EBlist
        self.Tlist = Tlist
        self.redraw_plot(self.EBlist, self.Tlist)
        return

    def redraw_plot(self, EBlist, Tlist):
        """ Redraws the plots
        """
        # See https://stackoverflow.com/questions/44412296/update-bar-chart-using-a-slider-in-matplotlib
        self.rects[0].set_height(self.EBlist[0])
        self.rects[1].set_height(self.EBlist[1])
        self.rects[2].set_height(self.EBlist[2])
        self.rects[3].set_height(self.EBlist[3])
        # Figure 2 - Energy Balance
        self.rects2[0].set_height(self.EBlist[4])
        self.rects2[1].set_height(self.EBlist[5])
        self.rects2[2].set_height(self.EBlist[6])
        self.rects2[3].set_height(self.EBlist[7])
        # Figure 3 - SVP
        #self.tlist = [self.airT + 273.15, self.Tw + 273.15, self.Td + 273.15, self.svp, self.vp, self.svpTw, self.svpTd]
        self.ax3.clear()
        self.ax3.set_xlim(265, 310)
        self.ax3.set_ylim(4, 54)
        self.ax3.set_facecolor('lightgrey')
        self.ax3.grid(axis='both')
        self.ax3.set_title('Saturation Vapour Pressure vs Air Temperature')
        self.ax3.set_ylabel('SVP (hPa or mbar')
        self.ax3.plot(self.x_list, self.y_list)
        self.ax3.plot(Tlist[0], Tlist[4], 'ro')    # T, vp
        self.ax3.annotate('T,e', xy=(Tlist[0], Tlist[4]))
        self.ax3.plot(Tlist[1], Tlist[5], 'go')    # Tw, svpTw
        self.ax3.annotate('Tw', xy=(Tlist[1], Tlist[5]))
        self.ax3.plot(Tlist[2], Tlist[4], 'bo')    # Td, svpTd
        self.ax3.annotate('Td', xy=(Tlist[2], Tlist[4]))
        line = mlines.Line2D([self.Tlist[0], self.Tlist[0]], [self.Tlist[3], self.Tlist[4]])
        line.set_color('red')
        self.ax3.add_line(line)
        line = mlines.Line2D([self.Tlist[2], self.Tlist[0]], [self.Tlist[4], self.Tlist[6]])
        line.set_color('blue')
        self.ax3.add_line(line)
        line = mlines.Line2D([self.Tlist[1], self.Tlist[0]], [self.Tlist[5], self.Tlist[4]])
        line.set_color('green')
        self.ax3.add_line(line)
        self.top_left_panel.canvas.draw_idle()