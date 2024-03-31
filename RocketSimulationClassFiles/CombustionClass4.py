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



