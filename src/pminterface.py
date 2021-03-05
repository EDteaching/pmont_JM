"""
Created: Tuesday 1st December 2020
@author: John Moncrieff (j.moncrieff@ed.ac.uk)
Last Modified on 5 March 2021 15:40 

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
        
        self.inpt= {            # just the default to start with
                        "wind": 3,
                        "solar": 500,
                         "albedo": 0.25, 
                         "airt": 15,
                         "sfc": "grass (dry)",
                         "rs": 40,
                         "vp": 10,
                         "smd": 10
                        }
        self.rblist = [500.0, -30.0, 300.0, 200.0]
        self.eblist = [300.0, 100.0, 150.0, 200.0]
        # Polynomial fit to Graham Russell's smd fit for cereals
        # yfit = a*x**3+b*x+c   where x is smd in mm
        self.smdfit = [1.27791987e-04, -9.56796959e-02,  3.95338027e+01]
        self.mod = Model(self.inpt)
        self.tlist = self.mod.tlist
        self.vw = View(self.rblist, self.eblist, self.tlist)
        self.sfcs = ["grass (dry)","bare soil (dry)","cereals (dry)",
            "conifers (dry)","upland (dry)","grass (wet)", "bare soil (wet)",
            "cereals (wet)","conifers (wet)", "upland (wet)", "water"]
        self.bit_wind = widgets.BoundedIntText(value = self.inpt["wind"], min=1,  max=15, step=1, 
                                     description="u ($m \ s^{-1}$)", width=50)
        self.bit_solar = widgets.BoundedIntText(value = self.inpt["solar"], min=1, max=1000, step=10, 
                                        description="solar ($W m^{-2}$)", width=50)
        self.bit_vp = widgets.BoundedIntText(value =self.inpt["vp"], min=1, max=40, step=1, 
                                        description="vp (mbar)", width=50)
        self.dd_surface = widgets.Dropdown(value =self.inpt["sfc"], options=self.sfcs, 
                                       description="surface", width=50)
        self.bit_smd = widgets.BoundedIntText(value=self.inpt["smd"], min=1, max=180, step=5, 
                                       description="smd (mm)", width=50)
        self.bit_airt = widgets.BoundedIntText(value=self.inpt["airt"], min=-5, max=40, step=1, 
                                       description="air T (oC)", width=50)
        self.txt_rs = widgets.Text(description="rs")
        self.txt_rh  = widgets.Text(description="RH (%)")                              
        self.txt_le = widgets.Text(description="LE")
        self.txt_ra = widgets.Text(description="ra")
        # First time round to populate output boxes
        self.rblist, self.eblist, self.tlist, self.olist = self.mod.calculateLE(self.inpt)
        self.txt_rs.value = str('{0:.0f}'.format(self.olist[0]))
        self.txt_rh.value = str('{0:.1f}'.format(self.olist[1]))
        self.txt_le.value = str('{0:.1f}'.format(self.olist[2]))
        self.txt_ra.value = str('{0:.0f}'.format(self.olist[3]))
        
        self.bit_wind.observe(self.bit_wind_eventhandler, names='value')
        self.bit_solar.observe(self.bit_solar_eventhandler, names='value')
        self.bit_vp.observe(self.bit_vp_eventhandler, names='value')
        self.dd_surface.observe(self.dd_surface_eventhandler, names='value')
        self.bit_smd.observe(self.bit_smd_eventhandler, names='value')
        self.bit_airt.observe(self.bit_airt_eventhandler, names='value')
        self.h0 = widgets.HBox(children=[self.dd_surface, self.bit_smd])
        self.h1 = widgets.HBox(children=[self.bit_solar, self.bit_wind])
        self.h2 = widgets.HBox(children=[self.bit_airt, self.bit_vp, self.txt_rh])
        self.h3 = widgets.HBox(children=[self.txt_ra, self.txt_rs, self.txt_le])
        
    def reset_sfc(self,sfc):
        self.inpt= {            # just the default to start with
                        "wind": 3,
                        "solar": 500,
                         "albedo": self.mod.srftype[sfc]['albedo'], 
                         "airt": 15,
                         "sfc": sfc,
                         "rs": self.mod.srftype[sfc]['minrs'],
                         "vp": 10,
                         "smd": 10
                        }
        self.rblist = [500.0, -30.0, 300.0, 200.0]
        self.eblist = [300.0, 100.0, 150.0, 200.0]
        return self.inpt
        
    def func2(self, x, a, b, c):
        '''
        returns bulk surface resistance
        from a polynomial fit to Graham Russell's Data
        x is smd, a,b,c are polynomial fit
        '''
        return a*x**3+b*x+c
           
    def bit_wind_eventhandler(self,change):
        self.bit_wind.observe(self.bit_wind_eventhandler, names='value')
        self.inpt["wind"]=self.bit_wind.value
        self.rblist, self.eblist, self.tlist, self.olist = self.mod.calculateLE(self.inpt)
        self.txt_rs.value = str('{0:.0f}'.format(self.olist[0]))
        self.txt_rh.value = str('{0:.1f}'.format(self.olist[1]))
        self.txt_le.value = str('{0:.1f}'.format(self.olist[2]))
        self.txt_ra.value = str('{0:.0f}'.format(self.olist[3]))
        self.vw.redraw(self.rblist, self.eblist, self.tlist)
        
    def bit_smd_eventhandler(self,change):
        self.bit_smd.observe(self.bit_smd_eventhandler, names='value')
        self.inpt["smd"]=self.bit_smd.value
        # Use Russell fit to find rs from smd
        # Check that rs offset varies by surface
        self.inpt["rs"] = self.func2(self.inpt["smd"], self.smdfit[0],
            self.smdfit[1], self.mod.srftype[self.inpt["sfc"]]['minrs'])
        self.rblist, self.eblist, self.tlist, self.olist = self.mod.calculateLE(self.inpt)
        self.txt_rs.value = str('{0:.0f}'.format(self.olist[0]))
        self.txt_rh.value = str('{0:.1f}'.format(self.olist[1]))
        self.txt_le.value = str('{0:.1f}'.format(self.olist[2]))
        self.txt_ra.value = str('{0:.0f}'.format(self.olist[3]))
        self.vw.redraw(self.rblist, self.eblist, self.tlist)

    def dd_surface_eventhandler(self,change):
        self.dd_surface.observe(self.dd_surface_eventhandler, names='value')
        self.inpt["sfc"]=self.dd_surface.value
        self.inpt = self.reset_sfc(self.inpt["sfc"])
        self.bit_solar.value = self.inpt["solar"]
        self.bit_wind.value = self.inpt["wind"]
        self.bit_vp.value = self.inpt["vp"]
        self.bit_smd.value = self.inpt["smd"]
        self.bit_airt.value = self.inpt["airt"]
        self.rblist, self.eblist, self.tlist, self.olist = self.mod.calculateLE(self.inpt)
        self.txt_rs.value = str('{0:.0f}'.format(self.olist[0]))
        self.txt_rh.value = str('{0:.1f}'.format(self.olist[1]))
        self.txt_le.value = str('{0:.1f}'.format(self.olist[2]))
        self.txt_ra.value = str('{0:.0f}'.format(self.olist[3]))
        self.vw.redraw(self.rblist, self.eblist, self.tlist)
        
    def bit_solar_eventhandler(self,change):
        self.bit_solar.observe(self.bit_solar_eventhandler, names='value')
        self.inpt["solar"]=self.bit_solar.value
        self.rblist, self.eblist, self.tlist, self.olist = self.mod.calculateLE(self.inpt)
        self.txt_rs.value = str('{0:.0f}'.format(self.olist[0]))
        self.txt_rh.value = str('{0:.1f}'.format(self.olist[1]))
        self.txt_le.value = str('{0:.1f}'.format(self.olist[2]))
        self.txt_ra.value = str('{0:.0f}'.format(self.olist[3]))
        self.vw.redraw(self.rblist, self.eblist, self.tlist)

    def bit_vp_eventhandler(self,change):
        self.bit_vp.observe(self.bit_vp_eventhandler, names='value')
        self.inpt["vp"]=self.bit_vp.value
        self.rblist, self.eblist, self.tlist, self.olist = self.mod.calculateLE(self.inpt)
        self.txt_rs.value = str('{0:.0f}'.format(self.olist[0]))
        self.txt_rh.value = str('{0:.1f}'.format(self.olist[1]))
        self.txt_le.value = str('{0:.1f}'.format(self.olist[2]))
        self.txt_ra.value = str('{0:.0f}'.format(self.olist[3]))
        self.vw.redraw(self.rblist, self.eblist, self.tlist)

    def bit_airt_eventhandler(self,change):
        self.bit_airt.observe(self.bit_airt_eventhandler, names='value')
        self.inpt["airt"]=self.bit_airt.value
        self.rblist, self.eblist, self.tlist, self.olist = self.mod.calculateLE(self.inpt)
        self.txt_rs.value = str('{0:.0f}'.format(self.olist[0]))
        self.txt_rh.value = str('{0:.1f}'.format(self.olist[1]))
        self.txt_le.value = str('{0:.1f}'.format(self.olist[2]))
        self.txt_ra.value = str('{0:.0f}'.format(self.olist[3]))
        self.vw.redraw(self.rblist, self.eblist, self.tlist)
