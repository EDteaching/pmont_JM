"""
Created: Tuesday 1st December 2020
@author: John Moncrieff (j.moncrieff@ed.ac.uk)
Last Modified on 3 March 2021 15:00 

DESCRIPTION
===========
This package contains the class object for the view in 
the pmont Jupyter notebook

"""
#from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.lines as mlines
import math
import numpy as np
import matplotlib.pyplot as plt


class View():    
    def __init__(self, rblist, eblist, tlist):
        self.RBlist = rblist
        self.EBlist = eblist
        self.Tlist = tlist
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
        self.airT = 288.15
        self.vp = 10.0
        self.svp = 17.04
        self.Td = 282.2     # 9999 fix
        self.Tw = 9.56 + 273.15   # initial dewpoint and wet-bulb temperatures
        self.esTw = 20  # temp to get MVC running
        self.esTd = 10
        self.figure = plt.figure(figsize=(7,5))
        self.figure.canvas.toolbar_visible = False
        self.axes1 = self.figure.add_subplot(222)
        self.axes2 = self.figure.add_subplot(224)
        self.axes3 = self.figure.add_subplot(121)
        #self.figure.tight_layout(h_pad=3)
        plt.subplots_adjust(left=0.1, 
                    bottom=0.1,  
                    right=0.9,  
                    top=0.9,  
                    wspace=0.4,  
                    hspace=0.4) 

        N = 4  # 4 fluxes to show necessary variables
        self.ind = np.arange(N)  # the x locations for the groups
        self.width = 0.8  # the width of the bars

        self.rects = self.axes1.bar(self.ind, self.RBlist, self.width, align='center')
        self.rects[0].set_color('yellow')
        self.rects[1].set_color('yellow')
        self.rects[2].set_color('black')
        self.rects[3].set_color('darkgray')
        self.axes1.set_xlim(None, len(self.ind) + self.width)
        self.axes1.set_ylim(-200, 1000)
        self.axes1.set_facecolor('lightgrey')
        self.axes1.grid(axis='both')
        self.axes1.set_title("Radiation Balance")
        self.axes1.set_ylabel('Radiative Flux Density \n (W m$^{-2}$)')
        fluxes = ('Sd', 'aSd', 'Ld', 'Lu')
        self.axes1.set_xticks(self.ind + self.width)
#         #xticknames = self.axes1.set_xticklabels(fluxes)
        self.axes1.set_xticklabels(fluxes,rotation=0, rotation_mode="anchor", ha="right", size=10)
 
#         # Figure 2 - Energy Balance
        self.EBlist = eblist
        #ax2 = fig.add_subplot(3,2,1)
        self.rects2 = self.axes2.bar(self.ind, self.EBlist, self.width, align='center')
        self.rects2[0].set_color('black')
        self.rects2[1].set_color('red')
        self.rects2[2].set_color('blue')
        self.rects2[3].set_color('brown')
        self.axes2.set_xlim(None, len(self.ind) + self.width)
        self.axes2.set_ylim(-200, 1000)
        self.axes2.set_facecolor('lightgrey')
        self.axes2.grid(axis='both')
        self.axes2.set_title('Energy Balance')
        self.axes2.set_ylabel('Energy Flux Density \n (W m$^{-2}$)')
        fluxes2 = ('Rn', 'H', 'LE', 'G')
        self.axes2.set_xticks(self.ind + self.width)
        # xticknames = self.axes1.set_xticklabels(fluxes)
        self.axes2.set_xticklabels(fluxes2, rotation=0, rotation_mode="anchor", ha="right", size=10)

        # Figure 3 - SVP Figure
        #ax3 = fig.add_subplot(3,3,1)
        self.x_list = [l[0] for l in self.svpData]
        self.y_list = [l[1] for l in self.svpData]
        self.axes3.set_xlim(265, 310)
        self.axes3.set_ylim(4, 54)
        self.axes3.set_facecolor('lightgrey')
        self.axes3.grid(axis='both')
        self.axes3.set_title('SVP vs Air Temperature')
        self.axes3.set_ylabel('SVP (hPa or mbar)')
        self.axes3.set_xlabel('Air temperature (K)')
        self.axes3.plot(self.x_list, self.y_list)
        #tlist = [airT, Tw, Td, svp, vp, esTw, esTd]
        self.axes3.plot(self.airT, self.vp, 'bo')
        self.axes3.annotate('$T, e_s$', xy=(self.Tlist[0], self.Tlist[3]))
        self.axes3.plot(self.Tlist[0], self.Tlist[3], 'ro') 
        self.axes3.annotate('$T,e$', xy=(self.Tlist[0], self.Tlist[4]))
        self.axes3.plot(self.Tlist[1], self.Tlist[5], 'go')    # Tw, svpTw
        self.axes3.annotate('$T_w$', xy=(self.Tlist[1], self.Tlist[5]))
        self.axes3.plot(self.Tlist[2], self.Tlist[4], 'bo')    # Td, svpTd
        self.axes3.annotate('$T_d$', xy=(self.Tlist[2], self.Tlist[4]))
        line = mlines.Line2D([self.Tlist[0], self.Tlist[0]], [self.Tlist[3], self.Tlist[4]])
        line.set_color('red')
        self.axes3.add_line(line)
        line = mlines.Line2D([self.Tlist[2], self.Tlist[0]], [self.Tlist[4], self.Tlist[6]])
        line.set_color('blue')
        self.axes3.add_line(line)
        line = mlines.Line2D([self.Tlist[1], self.Tlist[0]], [self.Tlist[5], self.Tlist[4]])
        line.set_color('green')
        self.axes3.add_line(line)


    def redraw(self, rblist, eblist, tlist):
        """ Redraws the plots
        """
        self.RBlist = rblist
        self.EBlist = eblist
        self.Tlist = tlist
        # See https://stackoverflow.com/questions/44412296/update-bar-chart-using-a-slider-in-matplotlib
        #self.rects = self.ax1.bar(self.ind, self.RBlist, self.width, align='center')
        self.rects[0].set_height(self.RBlist[0])
        self.rects[1].set_height(self.RBlist[1])
        self.rects[2].set_height(self.RBlist[2])
        self.rects[3].set_height(self.RBlist[3])

        self.rects2[0].set_height(self.EBlist[0])
        self.rects2[1].set_height(self.EBlist[1])
        self.rects2[2].set_height(self.EBlist[2])
        self.rects2[3].set_height(self.EBlist[3])

        self.axes3.clear()       
        self.axes3.set_xlim(265, 310)
        self.axes3.set_ylim(4, 54)
        self.axes3.set_facecolor('lightgrey')
        self.axes3.grid(axis='both')
        self.axes3.set_title('SVP vs Air Temperature')
        self.axes3.set_ylabel('SVP (hPa or mbar)')
        self.axes3.set_xlabel('Air temperature (K)')
        self.x_list = [l[0] for l in self.svpData]
        self.y_list = [l[1] for l in self.svpData]
        self.axes3.plot(self.x_list, self.y_list)
        self.axes3.annotate('$T, e_s$', xy=(self.Tlist[0], self.Tlist[3]))
        self.axes3.plot(self.Tlist[0], self.Tlist[3], 'ro')    #
        self.axes3.plot(self.Tlist[0], self.Tlist[4], 'ro')    # T, vp
        self.axes3.annotate('$T,e$', xy=(self.Tlist[0], self.Tlist[4]))
        self.axes3.plot(self.Tlist[1], self.Tlist[5], 'go')    # Tw, svpTw
        self.axes3.annotate('$T_w$', xy=(self.Tlist[1], self.Tlist[5]))
        self.axes3.plot(self.Tlist[2], self.Tlist[4], 'bo')    # Td, svpTd
        self.axes3.annotate('$T_d$', xy=(self.Tlist[2], self.Tlist[4]))
        line = mlines.Line2D([self.Tlist[0], self.Tlist[0]], [self.Tlist[3], self.Tlist[4]])
        line.set_color('red')
        self.axes3.add_line(line)
        line = mlines.Line2D([self.Tlist[2], self.Tlist[0]], [self.Tlist[4], self.Tlist[6]])
        line.set_color('blue')
        self.axes3.add_line(line)
        line = mlines.Line2D([self.Tlist[1], self.Tlist[0]], [self.Tlist[5], self.Tlist[4]])
        line.set_color('green')
        self.axes3.add_line(line)
        self.figure.canvas.toolbar_visible = False
        self.figure.canvas.draw()
