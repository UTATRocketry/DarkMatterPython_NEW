import RocketSimulationClassFiles as Rocket
import numpy as np
class PressurantTankClass4:
    #special added function for update motion (NOT SURE HOW TO INCORPORATE YET)
    def update_motion(self, linear_acceleration, angular_acceleration):
        # Update linear motion
        self.cg += self.velocity + 0.5 * linear_acceleration * self.input['sim']['time_step'] ** 2
        self.velocity += linear_acceleration * self.input['sim']['time_step']

        # Update angular motion
        self.angular_position += self.angular_velocity + 0.5 * angular_acceleration * self.input['sim'][
            'time_step'] ** 2
        self.angular_velocity += angular_acceleration * self.input['sim']['time_step']
    #from old file variable names
    '''
        Properties
        name            % Propellant name                           (str)
        type            % Propellant type                           (str)
        tank_input      % Tag for tank                              (str)
        input           % Input structure                           (struct)
        tank            % Tank body                                 (struct)
        pressurant      % Pressurant Gas                            (fluidClass)
        cg              % CG of propellant tank system              (double)
        m               % Mass of propellant tank system            (double)
        l               % length of propellant tank system          (double)
        offset          % Distance offset before tank system        (double)
        util            % Utilities                                 (utilitiesClass)
        designVars
    '''

    def __init__(self, input, inputTag):
        if not input or not inputTag:
            raise ValueError("Invalid inputs - PressurantTankClass > __init__")

        self.input = input
        self.tank_input = inputTag

        self.name = self.tank_input["name"]

        #not sure if we need to maintain 3D for gravity calculations
        self.cg = np.zeros((input['sim']['numpt'], 1))  #make it a 3 if need 3 D vector
        self.offset = self.tank_input["offset"]
        self.m = self.tank_input["mInit"] * np.ones((input['sim']['numpt'], 1))
        self.l = self.tank_input["lTank"]

        self.tank = Rocket.propertyClass()
        self.tank.m = self.tank_input["mTank"]
        self.tank.V = self.tank_input["vTank"]
        self.tank.cg = self.l/2
        #again
        #if need to change to 3D
        '''
        self.tank.cg = np.array([self.l / 2, self.w / 2, self.z / 2])
        W and Z variables not declared yet
        '''

        self.util = Rocket.utilitiesClass(input)

        self.pressurant = Rocket.fluidClass(self.input, self.tank_input)

        self.initstruct = Rocket.propertyClass()


        self.initstruct.m = self.tank_input["mInit"]
        self.initstruct.T = self.tank_input["Tinit"]
        self.initstruct.P = self.tank_input["Pinit"]
        self.initstruct.rho = self.util.cp('D', 'P', self.initstruct.P, 'T', self.initstruct.T, self.tank_input["name"])

        self.pressurant.setInitialConditions(self.initstruct)
        self.setBlowdownCharacteristics(input)

        # Additional VARIABLES 6DoF
        self.angular_position = np.zeros((input['sim']['numpt'], 3))  # Roll, pitch, yaw
        self.angular_velocity = np.zeros((input['sim']['numpt'], 3))  # Angular velocities in roll, pitch, yaw
        self.angular_acceleration = np.zeros((input['sim']['numpt'], 3))  # Angular accelerations in roll, pitch, yaw

    def getCG(self):
        self.cg = np.divide(self.pressurant.l, 2)
        self.m = self.pressurant.m + self.tank.m
    #this is the same as before
    #other functions calling down and fetches the CoG
    #not called within this function


    #no need to change. works for 6DoF
    def getBlowdown(self):
        '''
        -----------------------------------------------------------------------
           METHOD: getBlowdown
           Selects and calls appropriate blowdown function depending on the
           type of blowdown specified in the input file.

           INPUTS: NONE
           OUTPUTS: NONE
        -----------------------------------------------------------------------
        '''

        if self.name == "N2":
            self.PRES_blowdown()
        else:
            raise Exception(
                "pressurantTankClass > getBlowdown(): Function has not been specialized for fluid name" + self.name)

    def setBlowdownCharacteristics(self, input):
        '''
        -----------------------------------------------------------------------
           METHOD: setBlowdownCharacteristics
           Selects the functions that computes the blowdown characteristics for
           the given pressurant.

           INPUTS: NONE
           OUTPUTS: NONE
        -----------------------------------------------------------------------
        '''

        if self.name == 'N2':
            self.pressurant.bdChars = self.bd_Chars_NITROGEN
        else:
            raise Exception(
                "pressurantTankClass > getBlowdown(): Function has not been specialized for fluid name" + self.name)

    def bd_Chars_NITROGEN(self, input):
        '''
        -----------------------------------------------------------------------
           METHOD: bd_Chars_NITROGEN
           Function that details the blowdown characteristics of the selected
           pressurant.

           INPUTS \..........................................................
           - <input> (struct): A structure that contains all input variables
           OUTPUTS ............................................................
            NONE
        -----------------------------------------------------------------------
        '''
        ma = input.m
        V = input.V
        T = input.T
        P = input.P
        mdot = input.mdot
        qdot = input.qdot

        R = self.util.n2R
        cnv = self.util.cnv

        Zt = self.util.get_dZdT_N2(T, P / cnv)
        Zp = self.util.get_dZdP_N2(T, P / cnv) / cnv
        Z = self.util.coolprop('Z', 'P', P, 'T', T, 'N2')
        cv = self.util.coolprop('O', 'P', P, 'T', T, 'N2')

        dPdt = (ma * R * Z ** 2 + P * V * Zt) * qdot / (V * cv * (ma * (Z - P * Zp))) - mdot * (
                    (cv + Z * R) * ma * Z + P * V * Zt) * (P / (ma * cv)) / (ma * (Z - P * Zp))
        dZdt = (ma * R * Z ** 2 * Zp + V * Z * Zt) * dPdt / (ma * R * Z ** 2 + Zt * P * V) - Zt * (
                    P * V * Z / ma) * mdot / (ma * R * Z ** 2 + Zt * P * V)
        dTdt = V * (dPdt / (ma * Z) - dZdt * P / (ma * Z ** 2) - mdot * P / (ma ** 2 * Z)) / R

        self.dPdt = dPdt
        self.dTdt = dTdt
        return self

    def setPressurantMdot(self, mdot):
        '''
        -----------------------------------------------------------------------
           METHOD: setPressurantMdot
            Initializes the Mdot of the selected pressurant using the inputted
            mdot. It initializes said mdot and associates it with the
            pressurantClass object.

           INPUTS .............................................................
            - mdot (list float): A list of floats containing the mdot evolution
            of the pressurant over time. It is a part of the input structure.
           OUTPUTS: NONE
        -----------------------------------------------------------------------
        '''
        self.pressurant.mdot = mdot


#PRES_BLOWDOWN needs to be changed for 6DoF
#need rewrite