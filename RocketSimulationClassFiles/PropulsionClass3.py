import RocketSimulationClassFiles as Rocket
import numpy as np
class PropulsionClass3:

    def __init__(self, input):
        print("Building Propulsion Class")
        self.input = input
        #utility class should be done
        self.util = Rocket.UtilityClass2(self.input)

        #variables below from spec
        self.info = self.input["engine"]


        self.settings = self.input['settings']
        ofi = self.settings['OF_i']  #Oxidizer-Fuel ratio initial
        off = self.settings['OF_f']  #Oxidizer-Fuel ratio final
        nf = self.settings['num_OF'] #number of Oxidizer-Fuel ratios
        self.settings['OF_Vec'] = np.linspace(ofi, off, num=nf) #create a vector
        ''' NP linspace
        np.linspace (startNumber, finalNumber, number of evenly spaced points)
        top and bottom inclusive
        start from ofi, ends at off. interval = nf
        '''

        #   --------------------------------------------------------------
        #   Did not change from 2DoF structure
        #
        #   Dictionary structure. in variable: self.performance
        #   self.performance =
        #       ("Mdotox", "Mdotf", "Mdot", "Mf",
        #       "Mox", "Mprop", "Pcc", "Tcc", "Te",
        #       "cstar", "Pe", "thrust", "Isp")
        #   All the getter functions are below
        #
        #   Attached to each variable is another dictionary of 0 arrays
        #   Each array row = 100, col = 1
        #
        #   --------------------------------------------------------------
        self.performance = {"Mdotox" : self.util.zeroArray(), "Mdotf" : self.util.zeroArray(),
                         "Mdot" : self.util.zeroArray(),
                         "Mf" : self.util.zeroArray(),
                         "Mox" : self.util.zeroArray(),
                         "Mprop" : self.util.zeroArray(),
                         "Pcc" : self.util.zeroArray(),
                         "Tcc" : self.util.zeroArray(),
                         "Te" : self.util.zeroArray(),
                         "cstar" : self.util.zeroArray(),
                         "Pe" : self.util.zeroArray(),
                         "thrust" : np.zeros(100),
                         "Isp" : self.util.zeroArray()}
        self.getPropellantTags()


        self.combustion = Rocket.CombustionClass4(input)
        self.nozzle = Rocket.NozzleClass4(input)

        self.propellants = Rocket.TankClass3(input)

        '''
        propellants.tanks is an 2D array. np.shape return size of array. 
        Gives number of rows in array, which is number of tanks
        '''
        self.settings['numTanks'] = np.shape(self.propellants.tanks)[0]

    #COPIED ALL METHODS ASSOCIATED WITH self.Performance()
    # -----------------------------------------------------------------------
    #   METHOD: getPropellantTags
    #   Selects and gets the appropriate tag structures for the propellant
    #   and oxider of the rocket.
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    # -----------------------------------------------------------------------
    def getPropellantTags(self):
        self.oxidizerTag = self.input['ox']
        self.fuelTag = self.input['fuel']

    # -----------------------------------------------------------------------
    #   METHOD: getCG
    #   Selects and gets propellant CG properties
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    # -----------------------------------------------------------------------
    def getCG(self):
        self.propellants.getCG()  # this method does not return anything, but adds cg, m, and l instance variables to self.propellants
        self.cg = self.propellants.cg
        self.m = self.propellants.m
        self.l = self.propellants.l

    # -----------------------------------------------------------------------
    #   METHOD: getMassFlowRates
    #   Selects and gets the mass flow rates for each tank in the system
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    # -----------------------------------------------------------------------
    def setMassFlowRates(self):

        for i in range(self.settings['numTanks']):
            tank_type = self.propellants.tank_inputs[i][0]
            if tank_type == 'Oxidizer':
                self.performance['Mdotox'] = self.propellants.tanks[i][0].propellant.mdot
            elif tank_type == 'Fuel':
                self.performance['Mdotf'] = self.propellants.tanks[i][0].propellant.mdot

            elif tank_type == 'Pressurant':
                continue
            else:
                raise Exception('propulsionClass --> setMassFlowRates(): Unknown propellant type.')

        self.performance['Mdot'] = self.performance['Mdotox'] + self.performance['Mdotf']

    # -----------------------------------------------------------------------
    #   METHOD: Mdotox
    #   Returns the Mdot for the oxidizer
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    # -----------------------------------------------------------------------
    def Mdotox(self):
        return self.performance.get('Mdotox')

    # -----------------------------------------------------------------------
    #   METHOD: Mdot
    #   Returns the Mdot for the whole system
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    # -----------------------------------------------------------------------
    def Mdot(self):
        return self.performance.get('Mdot')

    # -----------------------------------------------------------------------
    #   METHOD: Mox
    #   Returns the Mass of the oxidizer vs time
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    # -----------------------------------------------------------------------
    def Mox(self):
        return self.performance.get('Mox')

    # -----------------------------------------------------------------------
    #   METHOD: Mf
    #   Returns the Mass of the fuel vs time
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    # -----------------------------------------------------------------------
    def Mf(self):
        return self.performance.get('Mf')

    # -----------------------------------------------------------------------
    #   METHOD: Mox
    #   Returns the Mass of all propellant vs time
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    # -----------------------------------------------------------------------
    def Mprop(self):
        return self.performance.get('Mprop')

    # -----------------------------------------------------------------------
    #   METHOD: setOFratio
    #   Sets the oxidizer to fuel mass flow ratio
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    # -----------------------------------------------------------------------
    def setOFratio(self):

        self.performance['OF'] = self.performance["Mdotox"] / self.performance['Mdotf']

    # -----------------------------------------------------------------------
    #   METHOD: getOF
    #   Returns the calculated OF
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    # -----------------------------------------------------------------------
    def getOF(self):
        return self.performance['OF']

    # -----------------------------------------------------------------------
    #   METHOD: getCstar
    #   Returns the calculated characteristic velocity = for the system
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    # -----------------------------------------------------------------------
    def getCstar(self):
        Pcc = self.designVars.Pcc
        cstar = np.zeros((self.settings['num_OF']))

        for i in range(0, len(cstar)):
            self.combustion.get_CEA(self.settings['OF_Vec'][i], self.designVars.Pcc, 1)

            cstar[i] = self.combustion.output.cstar / 1000

        self.performance['cstar'] = np.polyfit(self.settings['OF_Vec'], cstar, 3)

    # -----------------------------------------------------------------------
    #   METHOD: setPropMasses
    #   Sets the propellant masses for the system
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    # -----------------------------------------------------------------------
    def setPropMasses(self):

        for i in range(self.settings['numTanks']):
            tank_type = self.propellants.tank_inputs[i][0]

            if tank_type == 'Oxidizer':
                self.performance['Mox'] = self.propellants.tanks[i][0].m[:]
            elif tank_type == 'Fuel':
                self.performance['Mf'] = self.propellants.tanks[i][0].m[:]
            elif tank_type == 'Pressurant':
                continue
            else:
                raise Exception('rocketClass --> setPropMasses(): Unknown propellant type')

    # -----------------------------------------------------------------------
    #   METHOD: setPropMasses
    #   Sets the blowdown characteristics of the system
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    # -----------------------------------------------------------------------
    def getBlowdown(self):

        tank_inputs = self.input['props']

        for i in range(0, self.settings['numTanks']):
            if tank_inputs[i][0] == 'Fuel' or tank_inputs[i][0] == 'Oxidizer':

                self.propellants.tanks[i][0].getBlowdown()

                if tank_inputs[i][2] > 0:
                    # propellants.tanks contains a list of objects of type propellantTankClass
                    self.propellants.tanks[tank_inputs[i][2]][0].pressurant.mdot = \
                    self.propellants.tanks[tank_inputs[i][2]][0].pressurant.mdot + self.propellants.tanks[i][
                        0].pressurant.mdot  # idk what's happening here with the tank inputs

            for i in range(self.settings['numTanks']):

                if tank_inputs[i][0] == 'Fuel' or tank_inputs[i][0] == 'Oxidizer':
                    self.propellants.tanks[i][0].getBlowdown()

                    if tank_inputs[i][2] > 0:
                        self.propellants.tanks[tank_inputs[i][2]][0].pressurant.mdot = \
                        self.propellants.tanks[tank_inputs[i][2]][0].pressurant.mdot + self.propellants.tanks[i][
                            0].pressurant.mdot

            for i in range(self.settings['numTanks']):
                if tank_inputs[i][0] == 'Pressurant':
                    self.propellants.tanks[i][0].getBlowdown()

        self.setMassFlowRates()
        self.setOFratio()
        self.setPropMasses()