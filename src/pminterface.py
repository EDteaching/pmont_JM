"""
Created: Tuesday 1st December 2020
@author: John Moncrieff (j.moncrieff@ed.ac.uk)
Last Modified on 15 Feb 2021 21:08 

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
                         "albedo": 0.35, 
                         "airt": 15,
                         "sfc": "grass",
                         "rs": 20,
                         "vp": 10
                        }
        self.rblist = [300, 300, 300, 300]
        self.eblist = [300, 300, 300, 300]
        
        self.mod = Model(self.surface)
        self.tlist = self.mod.tlist
        #print(self.mod.tlist)
        self.vw = View(self.rblist, self.eblist, self.tlist)
        self.sfcs = ["grass","bare Soil","conifers","water"]
        self.bit_wind = widgets.BoundedIntText(value = self.surface["wind"], min=1,  max=15, step=1, 
                                     description="wind speed $m \ s^{-1}$", width=50)
        self.bit_solar = widgets.BoundedIntText(value = self.surface["solar"], min=1, max=1000, step=10, 
                                        description="solar ($W m^{-2}$)", width=50)
        self.bit_vp = widgets.BoundedIntText(value =self.surface["vp"], min=1, max=40, step=1, 
                                        description="vapour pressure (mbar)", width=50)
        self.dd_surface = widgets.Dropdown(value =self.surface["sfc"], options=self.sfcs, 
                                       description="surface", width=50)
        self.bit_rs = widgets.BoundedIntText(value=self.surface["rs"], min=1, max=120, step=5, 
                                       description="canopy resistance ( $s m^{-1}$)", width=50)
        self.bit_airt = widgets.BoundedIntText(value=self.surface["airt"], min=-5, max=40, step=1, 
                                       description="air temperature", width=50)
       
        self.bit_wind.observe(self.bit_wind_eventhandler, names='value')
        self.bit_solar.observe(self.bit_solar_eventhandler, names='value')
        self.bit_vp.observe(self.bit_vp_eventhandler, names='value')
        self.dd_surface.observe(self.dd_surface_eventhandler, names='value')
        self.bit_rs.observe(self.bit_rs_eventhandler, names='value')
        self.bit_airt.observe(self.bit_airt_eventhandler, names='value')

        self.h1 = widgets.HBox(children=[self.bit_wind, self.dd_surface,self.bit_rs])
        self.h2 = widgets.HBox(children=[self.bit_solar, self.bit_airt, self.bit_vp])
           
    def bit_wind_eventhandler(self,change):
        self.bit_wind.observe(self.bit_wind_eventhandler, names='value')
        self.surface["wind"]=self.bit_wind.value
        self.rblist, self.eblist, self.tlist = self.mod.calculateLE(self.surface)
        self.vw.redraw(self.rblist, self.eblist, self.tlist)
        
    def bit_rs_eventhandler(self,change):
        self.bit_rs.observe(self.bit_rs_eventhandler, names='value')
        self.surface["rs"]=self.bit_rs.value
        self.rblist, self.eblist, self.tlist = self.mod.calculateLE(self.surface)
        self.vw.redraw(self.rblist, self.eblist, self.tlist)

    def dd_surface_eventhandler(self,change):
        self.dd_surface.observe(self.dd_surface_eventhandler, names='value')
        self.surface["sfc"]=self.dd_surface.value
        self.rblist, self.eblist, self.tlist = self.mod.calculateLE(self.surface)
        self.vw.redraw(self.rblist, self.eblist, self.tlist)
        
    def bit_solar_eventhandler(self,change):
        self.bit_solar.observe(self.bit_solar_eventhandler, names='value')
        self.surface["solar"]=self.bit_solar.value
        self.rblist, self.eblist, self.tlist = self.mod.calculateLE(self.surface)
        self.vw.redraw(self.rblist, self.eblist, self.tlist)

    def bit_vp_eventhandler(self,change):
        self.bit_vp.observe(self.bit_vp_eventhandler, names='value')
        self.surface["vp"]=self.bit_vp.value
        self.rblist, self.eblist, self.tlist = self.mod.calculateLE(self.surface)
        self.vw.redraw(self.rblist, self.eblist, self.tlist)

    def bit_airt_eventhandler(self,change):
        self.bit_airt.observe(self.bit_airt_eventhandler, names='value')
        self.surface["airt"]=self.bit_airt.value
        self.rblist, self.eblist, self.tlist = self.mod.calculateLE(self.surface)
        self.vw.redraw(self.rblist, self.eblist, self.tlist)
