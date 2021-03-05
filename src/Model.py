"""
Created: Tuesday 1st December 2020
@author: John Moncrieff (j.moncrieff@ed.ac.uk)
Last Modified on 5 March 2021 14:00 

DESCRIPTION
===========
This package contains the model class object

"""

import numpy as np
import math

class Model():
    '''
    The main model class
    '''
    # Define all the instance variables
    def __init__(self, inpt):
        self.inpt = inpt
        self.sol = self.inpt["solar"]
        self.rn = 0
        self.u = self.inpt["wind"]
        self.airT = self.inpt["airt"]
        self.vp = self.inpt["vp"]
        self.rs = self.inpt["rs"]
        self.c1_svp = 6790.4985  # constant used in svp calculation
        self.c2_svp = 52.57633
        self.c3_svp = 5.02808
        self.absZero = 273.15        # Absolute zero
        self.svp = self.c_satVapPres(self.airT)
        self.Td = self.dewpoint()
        self.Tw = self.wetbulb()
        self.esTw = self.c_satVapPres(self.Tw)
        self.esTd = self.c_satVapPres(self.Td)
        self.NumSurfaceTypes = 11
        self.ustar = self.u/10   # rough rule of thumb
        self.vonKarman = 0.41
        self.sfcs = ["grass (dry)", "bare soil (dry)", "cereals (dry)", "conifers (dry)",
                     "upland (dry)","grass (wet)", "bare soil (wet)", "cereals (wet)",
                     "conifers (wet)", "upland (wet)", "water"]
        self.surface = self.inpt["sfc"]
        self.index = self.sfcs.index(self.inpt["sfc"])
        
        self.tlist = [self.airT + 273.15, self.Tw + 273.15, self.Td + 273.15, self.svp, self.vp, self.esTw, self.esTd]
        
        self.srftype={
        'grass (dry)':     {'albedo': 0.25, 'z': 0.05, 'z0': 0.03, 'd': 0.02, 'minrs': 40},
        'bare soil (dry)': {'albedo': 0.15, 'z': 0.05, 'z0': 0.03, 'd': 0.02, 'minrs': 100},
        'cereals (dry)':   {'albedo': 0.25, 'z': 0.35, 'z0': 0.06, 'd': 0.15, 'minrs': 40},
        'conifers (dry)':  {'albedo': 0.12, 'z': 10.0, 'z0': 0.80, 'd': 9, 'minrs': 70},
        'upland (dry)':    {'albedo': 0.25, 'z': 0.10, 'z0': 0.05, 'd': 0.05, 'minrs': 110},
        'grass (wet)':     {'albedo': 0.28, 'z': 0.05, 'z0': 0.03, 'd': 0.02, 'minrs': 0.001},
        'bare soil (wet)': {'albedo': 0.20, 'z': 0.05, 'z0': 0.03, 'd': 0.02, 'minrs': 0.001},
        'cereals (wet)':   {'albedo': 0.13, 'z': 0.35, 'z0': 0.06, 'd': 0.15, 'minrs': 0.001},
        'conifers (wet)':  {'albedo': 0.12, 'z': 10.0, 'z0': 0.80, 'd': 9, 'minrs': 0.001},
        'upland (wet)':    {'albedo': 0.22, 'z': 0.10, 'z0': 0.05, 'd': 0.05, 'minrs': 0.001},
        'water':           {'albedo': 0.05, 'z': 0.01, 'z0': 0.001, 'd': 0.001, 'minrs': 0.001}
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
        self.tallcrops = ['conifers (dry)', 'conifers (wet)']
        
       #  self.parcel = [                      # point coordinates:
#             [self.airT+273.15, self.vp],     # airT, vp
#             [self.airT+273.15, 17.04],       # airT, svp
#             [self.Tw+273.15, self.esTw],     # Tw, esTw
#             [self.Td+273.15, self.vp]        # Td, vp
#         ]
    
    def wind_profile(self,sfc):
        '''returns wind speed at the height of the canopy from a 
        2 m measured wind speed
        '''
        self.ustar = self.inpt["wind"]/10
        return (self.ustar/self.vonKarman) * math.log(self.srftype[sfc]["z"]/self.srftype[sfc]["z0"])
    
    def c_ra(self, sfc):
        '''calculates aerodynamic resistances
           using eqns. 4.36 and 4.38 of MORECS report
        '''
        u =self.wind_profile(sfc)
        if sfc in self.tallcrops:
            self.ra = 56.3/u
        else:    
            self.ra = (6.25 / u) * math.log(10 / self.srftype[sfc]["z0"]) \
                      * math.log(6 / self.srftype[sfc]["z0"])
        return self.ra
        
    def calculateLE(self, inpt):
        '''
        Returns radiation, energy balance, various temperatures and output
        parameters
        '''
        self.inpt = inpt
        self.sol = self.inpt["solar"]
        self.rn = 0
        self.u = self.inpt["wind"]
        self.airT = self.inpt["airt"]
        self.vp = self.inpt["vp"]
        self.index = self.sfcs.index(self.inpt['sfc'])
        self.rs = self.inpt["rs"]
        self.albedo = self.srftype[str(self.inpt['sfc'])]['albedo']
        self.reflectedS = self.albedo * self.sol
        self.ra = self.c_ra(self.inpt['sfc'])
        self.nets = self.c_netShortwave()
        self.netl = self.c_netLongwave()
        # 9999 Uses surface Air T not true surface T
        self.LUP = 0.95 * self.stefanC * math.pow(self.airT + self.absZero, 4)  
        self.LDOWN = self.LUP - self.netl
        self.rn = self.c_netRadiation()
        self.svp = self.c_satVapPres(self.airT)
        self.Tw = self.wetbulb()
        self.esTw = self.c_satVapPres(self.Tw)
        self.Td = self.dewpoint()
        self.esTd = self.c_satVapPres(self.Td)
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
        return self.rblist, self.eblist, self.tlist, self.olist

    def c_netShortwave(self):
        '''
        calculates net shortwave radiation
        '''
        return (1 - self.srftype[str(self.inpt['sfc'])]['albedo']) * self.sol

    def c_netLongwave(self):
        '''
        calculates net longwave radiation at surface
        using eqn 4.22 in MORECS and clear skies !
        '''
        factor = 0.95 * self.stefanC * math.pow(self.airT + self.absZero, 4)
        return factor * (1.28 * (math.pow(self.vp / (self.airT + self.absZero), 0.142857))-1)
 
    def c_netRadiation(self):
        '''
        calculates net all-wave radiation
        '''
        return self.nets + self.netl
      
    def c_satVapPres(self, airT):
        '''
        calculates saturation vapour pressure (mbar)
        '''
        return 10 * math.exp(self.c2_svp - ((self.c1_svp / (airT + self.absZero)) +
                                            self.c3_svp * math.log(airT + self.absZero)))

    def c_rh(self):
        '''
        calculates relative humidity
        '''
        if self.vp >= self.svp:
            return 100.0
        else:
            return (self.vp / self.svp) * 100

    def c_delta(self):
        '''
        calculates slope of svp curve
        '''
        tup = self.airT + 0.5  # add half a degree to air temperature
        tlo = self.airT - 0.5  # subtract half a degree from air temperature
        return self.c_satVapPres(tup) - self.c_satVapPres(tlo)
        
    def dewpoint(self):
        '''
        return dewpoint
        '''
        factor = math.log(self.vp / 6.112)
        return 243.5 * factor/(17.67-factor)

    
    def wetbulb(self):
        '''
        # Wet bulb from http://www.the-snowman.com/wetbulb2.html
        '''
        self.rh = (self.vp / self.svp) * 100
        return (-5.806 + 0.672 * self.airT - 0.006 * self.airT * self.airT +
                (0.061 + 0.004 * self.airT + 0.000099 * self.airT * self.airT) *
                self.rh + (-0.000033 - 0.000005 * self.airT
                           - 0.0000001 * self.airT * self.airT) * self.rh * self.rh)
