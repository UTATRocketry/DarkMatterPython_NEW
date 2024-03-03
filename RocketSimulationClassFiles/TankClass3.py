import RocketSimulationClassFiles as rocket
from RocketSimulationClassFiles.UtilityClass2 import cellss
import numpy as np

class TankClass3:

    # -----------------------------------------------------------------------
    #   METHOD: tankSystemClass
    #   Constructs tankSystemClass given required inputs.
    #
    #   INPUTS \..........................................................
    #     - <input> (dictionary): A dictionary that contains all input variables
    #   OUTPUTS ............................................................
    #     - <self> (class):    Returns created tankSystemClass with inputs
    #                           and empty tanks attribute
    # -----------------------------------------------------------------------
    def __init__(self, input):
        self.input = input
        self.designVars = input["design"]
        #calls utility class, changed call structure
        self.tanks = cellss(np.shape(input['props'])[0],
                            1)  # can't change to numpy array as elmts of array are propellant tank class objects (line 19)
        self.tank_inputs = input["props"]
        self.create_tanks()
        # other properties m,cg,l should not need to be initialized as they are arrays

    # --------------------------------------------------------------------------------------------
    #   METHOD: create_tanks
    #   Creates tanks in tankSystemClass attributes with data from input dictionary
    #
    #   INPUTS  : NONE
    #   OUTPUTS : NONE
    # --------------------------------------------------------------------------------------------
    def create_tanks(self):
    #Note: propellant Tank class and pressurant tank class not implemented yet
        for i in range(0, len(self.tank_inputs)):
            type = self.tank_inputs[i][0]
            if (type == 'Fuel') or (type == 'Oxidizer'):
                self.tanks[i][0] = rocket.PropellantTankClass4(self.input, self.input['props'][i][1])
            elif (type == 'Pressurant'):
                self.tanks[i][0] = rocket.PressurantTankClass4(self.input, self.input['props'][i][1])
            else:
                raise Exception('Incorrect tank type.')

    # --------------------------------------------------------------------------------------------
    #   METHOD: getCG
    #   Calculates center of gravity of tanks using mass and position of tanks
    #   Loops through all tanks -- variable self.tanks
    #   self.tanks = [[[]]]   <- definied in utility class
    #   INPUTS  : NONE
    #   OUTPUTS ............................................................
    #     - <self> (class):    Returns center of gravity, mass, and length
    #                           of tanks
    # --------------------------------------------------------------------------------------------
    def getCG(self):
        totalLength = totalMass = totalMoment = 0
        # run getCG for each tank
        for i in range(1, np.size(self.tanks)):
            self.tanks[i][0].getCG()
            momCurr = np.multiply(self.tanks[i][0].m, (totalLength + self.tanks[i][0].offset + self.tanks[i][
                0].cg))  # have to make sure m, offset, and cg are numpy arrays in propellantTankClass

            totalLength += self.tanks[i][0].l + self.tanks[i][0].offset
            totalMoment += + momCurr
            totalMass += self.tanks[i][0].m

        self.cg = np.divide(totalMoment, totalMass)
        self.m = totalMass
        self.l = totalLength