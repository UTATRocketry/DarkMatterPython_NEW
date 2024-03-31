import RocketSimulationClassFiles as Rocket
import math
from CoolProp.CoolProp import PropsSI
import numpy as np

#When calling for rocket information. Use rocketVersionFiles.(fileName)
from RocketSimulationClassFiles import rocketVersionFiles

class CombustionClass4:
    '''properties (Access = public)

        input           # Input structure                           (dictionary)
        fuelTag         # Fuel inputs                               (dictionary)
        oxidizerTag     # Oxidizer inputs                           (dictionary)

        util            # Utilities                                 (utilitiesClass)

        output          # Combustion outputs                        (struct)
    '''
    def __init__(self, input):
        #from rocket spec in simulation class
        self.input = input
        #from utilities class
        self.util = Rocket.UtilityClass2(self.input)

        '''
        Similar to the one in PropulsionClass3
        Also needs its own propellantTags
        '''
    def getPropellantTags(self):
        self.oxidizerTag = self.input['ox']
        self.fuelTag = self.input['fuel']


#No changes needed for 6DoF
        # -----------------------------------------------------------------------
        #   METHOD: get_CEA
        #   Creates CEA object and calculates CEA outputs determines
        #
        #   INPUTS \..........................................................
        #     - <OF> (numeric):     Oxidizer fuel ratio
        #     - <Pcc> (numeric):    Combustion chamber pressure
        #     - <exp> (numeric):    Nozzle expansion area ratio
        #   OUTPUTS ............................................................
        #     - <self> (class):    Returns combustionClass with exit gamma,
        #                           mach number, specific impulse,
        #                           exit temperature and pressure, chamber gamma,
        #                           cstar, and chamber temperature
        # -----------------------------------------------------------------------
    def get_CEA(self, OF, Pcc, exp):
        if exp == None:
            exp = 3.887
        houbolt_jr = Rocket.CEA(Pcc=Pcc, OF=OF, area_ratio=exp, Pamb=14.7,
                                    oxName=self.input["ox"]["name"], fuelName=self.input["fuel"]["name"])
        # area ratio is throat area / nozzle area (from nozzleClass)
        self.output = Rocket.PropertyClass2()
        self.output.gamm_e = houbolt_jr.exit_MolWt_gamma  # return the tuple (mw, gam) for the nozzle exit (lbm/lbmole, -)
        self.output.rho_e = houbolt_jr.MachNumber
        self.output.Isp = houbolt_jr.Isp
        self.output.Te = houbolt_jr.T_e
        self.output.Pe = houbolt_jr.P_e
        self.output.Re = self.output.Pe / (self.output.rho_e * self.output.Te)
        self.output.gamm = houbolt_jr.Chamber_MolWt_gamma  # return the tuple (mw, gam) for the chamber (lbm/lbmole, -)
        self.output.cstar = houbolt_jr.Cstar
        self.output.Tcc = houbolt_jr.Temperatures[0]