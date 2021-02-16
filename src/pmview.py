"""

"""
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.lines as mlines
import math
import matplotlib.pyplot as plt



class view():    
    def __init__():
         # Temporarily fill a list of energy balance values
        self.EBlist = [500.0, -30.0, 300.0, 200.0]
        self.rects = self.axes1.bar(self.ind, self.EBlist, self.width, align='center')
        self.rects[0].set_color('yellow')
        self.rects[1].set_color('yellow')
        self.rects[2].set_color('black')
        self.rects[3].set_color('darkgray')
        self.axes1.set_xlim(None, len(self.ind) + self.width)
        self.axes1.set_ylim(-200, 1000)
        self.axes1.set_facecolor('lightgrey')
        self.axes1.grid(axis='both')
        self.axes1.set_title('Radiation Balance')
        self.axes1.set_ylabel('Energy Flux Density (Wm-2)')
        fluxes = ('Incoming Solar', 'Reflected Solar', 'Downward Longwave', 'Emitted Longwave')
        self.axes1.set_xticks(self.ind + self.width)
        #xticknames = self.axes1.set_xticklabels(fluxes)
        self.axes1.set_xticklabels(fluxes,rotation=0, rotation_mode="anchor", ha="right", size=10)

        # Figure 2 - Energy Balance
        self.EBlist2 = [300.0, 100.0, 150.0, 200.0]
        self.rects2 = self.axes2.bar(self.ind, self.EBlist2, self.width, align='center')
        self.rects2[0].set_color('black')
        self.rects2[1].set_color('red')
        self.rects2[2].set_color('blue')
        self.rects2[3].set_color('brown')
        self.axes2.set_xlim(None, len(self.ind) + self.width)
        self.axes2.set_ylim(-200, 1000)
        self.axes2.set_facecolor('lightgrey')
        self.axes2.grid(axis='both')
        self.axes2.set_title('Energy Balance')
        self.axes2.set_ylabel('Energy Flux Density (Wm-2)')
        fluxes2 = ('Net Radiation', 'Sensible Heat', 'Latent Heat', 'Soil Heat')
        self.axes2.set_xticks(self.ind + self.width)
        # xticknames = self.axes1.set_xticklabels(fluxes)
        self.axes2.set_xticklabels(fluxes2, rotation=0, rotation_mode="anchor", ha="right", size=10)

        # Figure 3 - SVP Figure
        self.x_list = [l[0] for l in self.svpData]
        self.y_list = [l[1] for l in self.svpData]
        self.axes3.set_xlim(265, 310)
        self.axes3.set_ylim(4, 54)
        self.axes3.set_facecolor('lightgrey')
        self.axes3.grid(axis='both')
        self.axes3.set_title('Saturation Vapour Pressure vs Air Temperature')
        self.axes3.set_ylabel('SVP (hPa or mbar')
        self.axes3.plot(self.x_list, self.y_list)
        self.axes3.plot(self.airT, self.vp, 'bo')
        
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
        self.axes3.clear()
        self.axes3.set_xlim(265, 310)
        self.axes3.set_ylim(4, 54)
        self.axes3.set_facecolor('lightgrey')
        self.axes3.grid(axis='both')
        self.axes3.set_title('Saturation Vapour Pressure vs Air Temperature')
        self.axes3.set_ylabel('SVP (hPa or mbar')
        self.axes3.plot(self.x_list, self.y_list)
        self.axes3.plot(Tlist[0], Tlist[4], 'ro')    # T, vp
        self.axes3.annotate('T,e', xy=(Tlist[0], Tlist[4]))
        self.axes3.plot(Tlist[1], Tlist[5], 'go')    # Tw, svpTw
        self.axes3.annotate('Tw', xy=(Tlist[1], Tlist[5]))
        self.axes3.plot(Tlist[2], Tlist[4], 'bo')    # Td, svpTd
        self.axes3.annotate('Td', xy=(Tlist[2], Tlist[4]))
        line = mlines.Line2D([self.Tlist[0], self.Tlist[0]], [self.Tlist[3], self.Tlist[4]])
        line.set_color('red')
        self.axes3.add_line(line)
        line = mlines.Line2D([self.Tlist[2], self.Tlist[0]], [self.Tlist[4], self.Tlist[6]])
        line.set_color('blue')
        self.axes3.add_line(line)
        line = mlines.Line2D([self.Tlist[1], self.Tlist[0]], [self.Tlist[5], self.Tlist[4]])
        line.set_color('green')
        self.axes3.add_line(line)
        self.top_left_panel.canvas.draw_idle()