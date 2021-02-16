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
        self.mod = Model(self.surface)
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
        
        #self.sumtotal = widgets.Text(value=self.sumtt,description="Total should be 100%", width=50, color='red')
        
        self.bit_wind.observe(self.bit_wind_eventhandler, names='value')
        self.bit_solar.observe(self.bit_solar_eventhandler, names='value')
        self.bit_vp.observe(self.bit_vp_eventhandler, names='value')
        self.dd_surface.observe(self.dd_surface_eventhandler, names='value')
        self.bit_rs.observe(self.bit_rs_eventhandler, names='value')
        self.bit_airt.observe(self.bit_airt_eventhandler, names='value')
        
        #self.btn = widgets.Button(description='Run RLINE', width=100)
        #self.btn.style.button_color = 'tomato'
        #self.btn.on_click(self.btn_eventhandler)
        self.h1 = widgets.HBox(children=[self.bit_wind, self.dd_surface,self.bit_rs])
        self.h2 = widgets.HBox(children=[self.bit_solar, self.bit_airt, self.bit_vp])
           
    def bit_wind_eventhandler(self,change):
        self.bit_wind.observe(self.bit_wind_eventhandler, names='value')
        self.surface["wind"]=self.bit_wind.value
        #def calculateLE(self, sol, airT, u, vp, rs, surface):
        self.mod.calculateLE(self.surface)
        
    def bit_rs_eventhandler(self,change):
        self.bit_rs.observe(self.bit_rs_eventhandler, names='value')
        self.surface["rs"]=self.bit_rs.value
        self.mod.calculateLE(self.surface)

    def dd_surface_eventhandler(self,change):
        self.dd_surface.observe(self.dd_surface_eventhandler, names='value')
        self.surface["sfc"]=self.dd_surface.value
        self.mod.calculateLE(self.surface)

    def bit_solar_eventhandler(self,change):
        self.bit_solar.observe(self.bit_solar_eventhandler, names='value')
        self.surface["solar"]=self.bit_solar.value
        self.mod.calculateLE(self.surface)

    def bit_vp_eventhandler(self,change):
        self.bit_vp.observe(self.bit_vp_eventhandler, names='value')
        self.surface["vp"]=self.bit_vp.value
        self.mod.calculateLE(self.surface)

    def bit_airt_eventhandler(self,change):
        self.bit_airt.observe(self.bit_airt_eventhandler, names='value')
        self.surface["airt"]=self.bit_airt.value
        self.mod.calculateLE(self.surface) 
        
