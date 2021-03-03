"""
Created: Tuesday 1st December 2020
@author: John Moncrieff (j.moncrieff@ed.ac.uk)
Last Modified on 3 March 2021 15:00 

DESCRIPTION
===========
This package contains the class object for configuring and running 
the pmont Jupyter notebook

"""

import ipywidgets as widgets
from IPython.display import display
import math
from src.Model import Model
from src.View import View

class pminterface():

    def __init__(self):
        
        self.surface = {
                        "wind": 5,
                        "solar": 500,
                         "albedo": 0.2, 
                         "airt": 15,
                         "sfc": "grass (dry)",
                         "rs": 40,
                         "vp": 10,
                         "smd": 10
                        }
        self.rblist = [300, 300, 300, 300]
        self.eblist = [300, 300, 300, 300]
        self.olist = []
        self.mod = Model(self.surface)
        self.tlist = self.mod.tlist
        self.vw = View(self.rblist, self.eblist, self.tlist)
        self.sfcs = ["grass (dry)","bare soil (dry)","cereals (dry)", "conifers (dry)","grass (wet)", "cereals (wet)","conifers (wet)", "water"]
        self.bit_wind = widgets.BoundedIntText(value = self.surface["wind"], min=1,  max=15, step=1, 
                                     description="u ($m \ s^{-1}$)", width=50)
        self.bit_solar = widgets.BoundedIntText(value = self.surface["solar"], min=1, max=1000, step=10, 
                                        description="solar ($W m^{-2}$)", width=50)
        self.bit_vp = widgets.BoundedIntText(value =self.surface["vp"], min=1, max=40, step=1, 
                                        description="vp (mbar)", width=50)
        self.dd_surface = widgets.Dropdown(value =self.surface["sfc"], options=self.sfcs, 
                                       description="surface", width=50)
        self.bit_smd = widgets.BoundedIntText(value=self.surface["smd"], min=1, max=180, step=5, 
                                       description="smd (mm)", width=50)
        self.bit_airt = widgets.BoundedIntText(value=self.surface["airt"], min=-5, max=40, step=1, 
                                       description="air T (oC)", width=50)
        self.txt_rs = widgets.Text(description="rs")
        self.txt_rh  = widgets.Text(description="RH (%)")                              
        self.txt_le = widgets.Text(description="LE")
        
        self.bit_wind.observe(self.bit_wind_eventhandler, names='value')
        self.bit_solar.observe(self.bit_solar_eventhandler, names='value')
        self.bit_vp.observe(self.bit_vp_eventhandler, names='value')
        self.dd_surface.observe(self.dd_surface_eventhandler, names='value')
        self.bit_smd.observe(self.bit_smd_eventhandler, names='value')
        self.bit_airt.observe(self.bit_airt_eventhandler, names='value')
        self.h0 = widgets.HBox(children=[self.dd_surface, self.bit_smd, self.txt_rs])
        self.h1 = widgets.HBox(children=[self.bit_solar, self.bit_wind, self.txt_rh])
        self.h2 = widgets.HBox(children=[self.bit_airt, self.bit_vp, self.txt_le])
           
    def bit_wind_eventhandler(self,change):
        self.bit_wind.observe(self.bit_wind_eventhandler, names='value')
        self.surface["wind"]=self.bit_wind.value
        self.rblist, self.eblist, self.tlist, self.olist = self.mod.calculateLE(self.surface)
        self.txt_rs.value = str('{0:.0f}'.format(self.olist[0]))
        self.txt_rh.value = str('{0:.1f}'.format(self.olist[1]))
        self.txt_le.value = str('{0:.1f}'.format(self.olist[2]))
        self.vw.redraw(self.rblist, self.eblist, self.tlist)
        
    def bit_smd_eventhandler(self,change):
        self.bit_smd.observe(self.bit_smd_eventhandler, names='value')
        self.surface["smd"]=self.bit_smd.value
        self.rblist, self.eblist, self.tlist, self.olist = self.mod.calculateLE(self.surface)
        self.txt_rs.value = str('{0:.0f}'.format(self.olist[0]))
        self.txt_rh.value = str('{0:.1f}'.format(self.olist[1]))
        self.txt_le.value = str('{0:.1f}'.format(self.olist[2]))
        self.vw.redraw(self.rblist, self.eblist, self.tlist)

    def dd_surface_eventhandler(self,change):
        self.dd_surface.observe(self.dd_surface_eventhandler, names='value')
        self.surface["sfc"]=self.dd_surface.value
        self.rblist, self.eblist, self.tlist, self.olist = self.mod.calculateLE(self.surface)
        self.txt_rs.value = str('{0:.0f}'.format(self.olist[0]))
        self.txt_rh.value = str('{0:.1f}'.format(self.olist[1]))
        self.txt_le.value = str('{0:.1f}'.format(self.olist[2]))
        self.vw.redraw(self.rblist, self.eblist, self.tlist)
        
    def bit_solar_eventhandler(self,change):
        self.bit_solar.observe(self.bit_solar_eventhandler, names='value')
        self.surface["solar"]=self.bit_solar.value
        self.rblist, self.eblist, self.tlist, self.olist = self.mod.calculateLE(self.surface)
        self.txt_rs.value = str('{0:.0f}'.format(self.olist[0]))
        self.txt_rh.value = str('{0:.1f}'.format(self.olist[1]))
        self.txt_le.value = str('{0:.1f}'.format(self.olist[2]))
        self.vw.redraw(self.rblist, self.eblist, self.tlist)

    def bit_vp_eventhandler(self,change):
        self.bit_vp.observe(self.bit_vp_eventhandler, names='value')
        self.surface["vp"]=self.bit_vp.value
        self.rblist, self.eblist, self.tlist, self.olist = self.mod.calculateLE(self.surface)
        self.txt_rs.value = str('{0:.0f}'.format(self.olist[0]))
        self.txt_rh.value = str('{0:.1f}'.format(self.olist[1]))
        self.txt_le.value = str('{0:.1f}'.format(self.olist[2]))
        self.vw.redraw(self.rblist, self.eblist, self.tlist)

    def bit_airt_eventhandler(self,change):
        self.bit_airt.observe(self.bit_airt_eventhandler, names='value')
        self.surface["airt"]=self.bit_airt.value
        self.rblist, self.eblist, self.tlist, self.olist = self.mod.calculateLE(self.surface)
        self.txt_rs.value = str('{0:.0f}'.format(self.olist[0]))
        self.txt_rh.value = str('{0:.1f}'.format(self.olist[1]))
        self.txt_le.value = str('{0:.1f}'.format(self.olist[2]))
        self.vw.redraw(self.rblist, self.eblist, self.tlist)
