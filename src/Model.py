"""
Created: Tuesday 1st December 2020
@author: John Moncrieff (j.moncrieff@ed.ac.uk)
Last Modified on 3 March 2021 15:00 

DESCRIPTION
===========
This package contains the model class object

"""

import numpy as np
import math

class Model():
    # Define all the instance variables
    def __init__(self, inpt):
        self.sol = inpt["solar"]
        self.rn = 0
        self.u = inpt["wind"]
        self.airT = inpt["airt"]
        self.vp = inpt["vp"]
        self.rs = inpt["rs"]
        self.c1_svp = 6790.4985  # constant used in svp calculation
        self.c2_svp = 52.57633
        self.c3_svp = 5.02808
        self.absZero = 273.15        # Absolute zero
        self.svp = self.c_satVapPres(self.airT)
        self.Td = self.dewpoint()
        self.Tw = self.wetbulb()
        self.esTw = self.c_satVapPres(self.Tw)
        self.esTd = self.c_satVapPres(self.Td)
        self.NumSurfaceTypes = 9
        self.one = 1
        self.sfcs = ["grass (dry)", "bare soil (dry)", "cereals (dry)", "conifers (dry)",
                     "grass (wet)", "bare soil (wet)", "cereals (wet)", "conifers (wet)",
                     "water"]
        self.surface = inpt["sfc"]
        self.index = 0
        
        self.tlist = [self.airT + 273.15, self.Tw + 273.15, self.Td + 273.15, self.svp, self.vp, self.esTw, self.esTd]
        # Initialize the vegetation types and their characteristics
        # SurfaceD holds Zero-Plane displacements in m
        # self.SurfaceD = [0.15, 0.75, 10, 0.05, 0.0005, 0.15, 0.15, 10]
#         # SurfaceZo holds roughness lengths
        self.SurfaceZo = [0.015, 0.075, 1, 0.005, 0.0005, 0.015, 0.015, 1]
#         # Surfacers holds bulk surface resistance in s m-1         
        self.SurfaceRs = [40, 40, 70, 100, 0.005, 100, 0.0001, 0.0001]
#         # SurfaceA holds albedo values

        self.SurfaceA = [0.25, 0.25, 0.12, 0.2, 0.05, 0.25, 0.25, 0.12]

        self.srftype={
        'grass (dry)':     {'albedo': 0.25, 'z0': 0.03, 'd': 0.05, 'minrs': 40},
        'bare soil (dry)': {'albedo': 0.25, 'z0': 0.03, 'd': 0.05, 'minrs': 100},
        'cereals (dry)':   {'albedo': 0.27, 'z0': 0.06, 'd': 0.1, 'minrs': 40},
        'conifers (dry)':  {'albedo': 0.12, 'z0': 1, 'd': 10, 'minrs': 70},
        'upland (dry)':    {'albedo': 0.30, 'z0': 1, 'd': 10, 'minrs': 110},
        'grass (wet)':     {'albedo': 0.28, 'z0': 0.03, 'd': 0.05, 'minrs': 0.001},
        'bare soil (wet)': {'albedo': 0.20, 'z0': 0.03, 'd': 0.05, 'minrs': 0.001},
        'cereals (wet)':   {'albedo': 0.25, 'z0': 0.06, 'd': 0.75, 'minrs': 0.001},
        'conifers (wet)':  {'albedo': 0.12, 'z0': 1, 'd': 10, 'minrs': 0.001},
        'water':           {'albedo': 0.05, 'z0': 0.001, 'd': 0, 'minrs': 0.001}
        }
        # print(self.srftype['grass (dry)']['z0'])
#         print(self.srftype['conifers (wet)']['albedo'])
        
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

        self.parcel = [                      # point coordinates:
            [self.airT+273.15, self.vp],     # airT, vp
            [self.airT+273.15, 17.04],       # airT, svp
            [self.Tw+273.15, self.esTw],     # Tw, esTw
            [self.Td+273.15, self.vp]        # Td, vp
        ]
        
    def c_ra(self,index,u):
            # calculates aerodynamic resistances
            # using eqns. 4.36 and 4.38 of MORECS report
        if self.index in self.vgList:
            self.ra = (6.25 / self.u) * math.log10(10 / self.SurfaceZo[self.index]) \
                      * math.log10(6 / self.SurfaceZo[self.index])
        else:
            self.ra = 94/self.u
        return self.ra
        
    def calculateLE(self, inpt):
        self.sol = inpt["solar"]
        self.rn = 0
        self.u = inpt["wind"]
        self.airT = inpt["airt"]
        self.vp = inpt["vp"]
        self.rs = inpt["rs"]
        self.albedo = inpt["albedo"]
        self.index = self.sfcs.index(inpt["sfc"])
        self.reflectedS = self.albedo * self.sol
        self.ra = self.c_ra(self.index, self.u)
        #self.rs = self.SurfaceRs[self.thisChoice]
        self.nets = self.c_netShortwave()
        self.netl = self.c_netLongwave()
        self.LUP = 0.95 * self.stefanC * math.pow(self.airT + self.absZero, 4)  # 9999 Uses surface Air T not true surface T
        self.LDOWN = self.LUP - self.netl
        self.rn = self.c_netRadiation()
        self.svp = self.c_satVapPres(self.airT)
        self.Tw = self.wetbulb()
        self.esTw = self.c_satVapPres(self.Tw)
        self.Td = self.dewpoint()
        self.esTd = self.c_satVapPres(self.Td)
        #print(self.Tw, '    ', self.esTw)
        self.rh =self.c_rh()
        if self.rh <100:
            self.delta = self.c_delta()
            if self.vp >= self.svp:
                self.vp = self.svp
            self.vpd = self.svp - self.vp
            self.LE = (self.delta * self.rn + self.rho * self.cp * (self.svp - self.vp)/self.ra)\
                / (self.delta + self.gamma * (1 + self.rs / self.ra))
            self.G = 0.1 * self.rn
            self.H = self.rn - self.LE - self.G
            self.mmPerDay = self.LE * 0.035
            self.tlist = [self.airT + 273.15, self.Tw + 273.15, self.Td + 273.15, self.svp, self.vp, self.esTw, self.esTd]
            self.rblist = [self.sol, self.reflectedS, self.LDOWN, self.LUP]
            self.eblist = [self.rn, self.H, self.LE, self.G]
            self.olist = [self.rs, self.rh, self.LE, self.ra]
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
        return self.rblist, self.eblist, self.tlist, self.olist

    def c_netShortwave(self):
        # calculates net shortwave radiation
        return (1 - self.SurfaceA[self.index]) * self.sol

    def c_netLongwave(self):
        # calculates net longwave radiation at surface
        # using eqn 4.22 in MORECS and clear skies !
        factor = 0.95 * self.stefanC * math.pow(self.airT + self.absZero, 4)
        return factor * (1.28 * (math.pow(self.vp / (self.airT + self.absZero), 0.142857))-1)
 
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

        