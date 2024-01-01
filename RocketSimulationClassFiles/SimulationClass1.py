import numpy as np
import RocketSimulationClassFiles as Rocket
import rocketVersionFiles


class SimulationClass1:
    # -----------------------------------------------------------------------
    #   METHOD: SimulationClass1 (1 means layer 1)
    #   Top layer
    #
    #   INPUTS \..........................................................
    #     - <input> (struct): Selected Rocket (from run file)
    #     - Calls rocketVersionFiles to access rocket info
    #     - Calls next level (level 2): rocketClass, utilityClass
    #   OUTPUTS ............................................................
    #       No outputs
    # -----------------------------------------------------------------------
    def __init__(self, selectedInput):
        if not selectedInput:
            raise Exception('ERROR: no rocket input selected')
        else:
            print("Building Simulation")
            #loading variables
            self.rocketSpecs = self.getRocketSpecs(selectedInput)
            print("No errors: RocketSpecs Retrieval successful")

            # get level 2 module (rocket and utility Class)
            # add parameters to rocketClass2
            #not fill in yet, so will give an error
            self.rocket = Rocket.RocketClass2(self.rocketSpecs)
            self.utility = Rocket.UtilityClass2(self.rocketSpecs)

            #still need the 3 variables here (add later)

            #load rocket properties - PropertyClass2
            self.flight = Rocket.PropertyClass2()
            #listing out properties (WITH 6DOF)

            #time
            self.flight.t = self.utility.zeroArray()
            #position
            self.flight.x = self.utility.zeroArray()
            self.flight.y = self.utility.zeroArray()
            self.flight.z = self.utility.zeroArray()
            #velocity
            self.flight.u = self.utility.zeroArray()
            self.flight.v = self.utility.zeroArray()
            self.flight.w = self.utility.zeroArray()
            #total velocity
            self.flight.V = self.utility.zeroArray()
            #acceleration
            self.flight.ax = self.utility.zeroArray()
            self.flight.ay = self.utility.zeroArray()
            self.flight.az = self.utility.zeroArray()
            #angle
            self.flight.phi = self.utility.zeroArray()  # Roll angle
            self.flight.theta = self.utility.zeroArray()  # Pitch angle
            self.flight.psi = self.utility.zeroArray()  # Yaw angle
            #angle velocity
            self.flight.p = self.utility.zeroArray()  # Roll rate
            self.flight.q = self.utility.zeroArray()  # Pitch rate
            self.flight.r = self.utility.zeroArray()  # Yaw rate

            #Mach
            self.flight.Ma = self.utility.zeroArray()
            #gravitational velocity?? (not sure)
            self.flight.g = self.utility.zeroArray()

            self.flight.altBO = self.rocketSpecs["sim"]["altBO"]

            # make sure that this exists in the input later
            #self.flight.type     = self.input["settings"]["flightType"]
            self.flight.type = self.rocket.get_flight_type()



    #load variable fucntion in old file
    def getRocketSpecs(self, input_selector):
        if input_selector == "houbolt_jr_single":
            # rocketInput.yaml file might need to be changed (IF CHANGING TO 3D)
            return rocketVersionFiles.houbolt_jr_single(
                'RocketSimulationClassFiles/rocketVersionFiles/rocketInput.yaml')
        # elif input_selector == ""
        else:
            raise Exception('Invalid rocket input')


    def setSimulationDynamicsType(self):
    # -----------------------------------------------------------------------
    #   Previous code only has 2dof
    #   Now chnaged to 6DOF
    #   Only code in 6DoF, leave the 2DoF for later
    # -----------------------------------------------------------------------
        if self.flight.type == '6DOF':
            self.flight.get = self.get6DOFflightDynamics
        elif self.flight.type == '2DOF':
            self.flight.get = self.get2DOFflightDynamics
        else:
            raise ValueError(f"Undefined flight type: {self.flight.type}")

    def get2DOFflightDynamics(self):
        '''#-----------------------------------------------------------------------
        #   METHOD: get2DOFflightDynamics
        #   Compute the 2D trajectory of the rocket's flight
        #
        #   INPUTS: NONE
        #   OUTPUTS: NONE
        #-----------------------------------------------------------------------'''

        # Make a copy of propulsion, utilities and flight
        prop = self.rocket.propulsion
        nozzle = prop.nozzle
        perf = prop.performance
        u = self.util
        fl = self.flight

        # Setup masses
        mdry = self.input['mass']['dry'] * np.ones(self.input['sim']['numpt'])
        mprop = prop.Mprop()
        mdot = prop.Mdot()
        m = mdry + mprop

        # Misc.
        Cd = self.rocket.airframe.cd  # Cd curve
        dt = self.designVars.dt  # Time step
        A = np.pi * (self.designVars.diameter / 2) ** 2  # Frontal area
        eff = prop.settings['efficiency']  # Combustion efficiency
        OF = prop.getOF()  # OF Ratios
        cnv = self.input['settings']['cnv']

        # Beginning of 2DOF flight dynamics
        atmos = u.stdAtmos(fl.y[0][0])

        # After engine ignition
        perf['Pcc'][0][0] = np.polyval(perf['cstar'], OF[0][0]) * mdot[0][0] / nozzle.throat.A / cnv  # Chamber Pressure
        prop.combustion.get_CEA(OF[0][0], perf['Pcc'][0][0], nozzle.exp)  # Compute combustion
        perf['Tcc'][0][0] = prop.combustion.output.Tcc
        perf['Pe'][0][0] = prop.combustion.output.Pe
        perf['Te'][0][0] = prop.combustion.output.Te

        alt_corr = (prop.combustion.output.Pe - atmos['P']) * nozzle.exit.A  # Altitude correction

        perf['thrust'][0] = prop.performance['Mdot'][0][0] * prop.settings[
            'efficiency'] * prop.combustion.output.Isp * u.g0 + alt_corr

        fl.Ay = self.util.zeroArray()
        fl.Ax = self.util.zeroArray()
        fl.drag = self.util.zeroArray()
        fl.u = self.util.zeroArray()
        fl.v = self.util.zeroArray()
        fl.V = self.util.zeroArray()
        fl.force = self.util.zeroArray()

        fl.Ay[0][0] = perf['thrust'][0] * np.cos(np.deg2rad(fl.theta[0][0])) / m[0][0] - u.g0
        fl.Ax[0][0] = perf['thrust'][0] * np.sin(np.deg2rad(fl.theta[0][0])) / m[0][0]
        fl.theta[0][0] = self.designVars.thetaL

        # Time stepping
        for i in range(1, self.input['sim']['numpt']):

            # Atmospheric conditions
            atmos = u.stdAtmos(fl.y[i - 1][0])  # Get atmospheric conditions

            # Combustion
            perf['Pcc'][i][0] = (np.polyval(perf['cstar'], OF[i][0]) * mdot[i][
                0] / nozzle.throat.A) / cnv  # Chamber pressure (Pa)
            combustion = prop.combustion.get_CEA(OF[i][0], perf['Pcc'][i][0], nozzle.exp)  # Compute combustion

            perf['Isp'][i][0] = prop.combustion.output.Isp  # Isp
            perf['Pe'][i][0] = prop.combustion.output.Pe  # Exit pressure
            perf['Te'][i][0] = prop.combustion.output.Te
            perf['Tcc'][i][0] = prop.combustion.output.Tcc

            # Compute forces on rocket
            alt_corr = (perf['Pe'][i][0] - atmos['P']) * nozzle.exit.A  # Altitude correction

            perf['thrust'][i] = perf['Mdot'][i][0] * perf['Isp'][i][0] * u.g0 * eff + alt_corr  # Thrust
            fl.drag[i][0] = 0.5 * atmos['rho'] * Cd(fl.Ma[i - 1][0]) * (fl.V[i - 1][0] ** 2) * A  # Drag

            # Accelerations
            fl.Ay[i][0] = (perf['thrust'][i] - fl.drag[i][0]) * np.cos(np.deg2rad(fl.theta[i - 1][0])) / m[i][0] - u.g0
            fl.Ax[i][0] = (perf['thrust'][i] - fl.drag[i][0]) * np.sin(np.deg2rad(fl.theta[i - 1][0])) / m[i][0]
            print('v:')
            print(fl.v[i - 1])
            print(fl.V[i - 1])
            #            print(Cd(fl.Ma[i-1][0]))
            #           print(perf['thrust'][i])
            #          print(fl.drag)
            print(fl.Ma[i - 1][0])
            # Speeds
            fl.u[i][0] = fl.u[i - 1][0] + fl.Ax[i][0] * dt  # Velocity in x direction at time t
            fl.v[i][0] = fl.v[i - 1][0] + fl.Ay[i][0] * dt  # Velocity in y direction at time t
            fl.V[i][0] = np.sqrt(fl.u[i][0] ** 2 + fl.v[i][0] ** 2)  # Total velocity at time t

            # Positions
            fl.y[i][0] = fl.y[i - 1][0] + fl.v[i][0] * dt + 0.5 * fl.Ay[i][0] * dt ** 2
            fl.x[i][0] = fl.x[i - 1][0] + fl.u[i][0] * dt + 0.5 * fl.Ax[i][0] * dt ** 2
            fl.s[i][0] = np.sqrt(fl.x[i][0] ** 2 + fl.y[i][0] ** 2)  # Total distance at time t

            # Loads and mach number
            fl.Ma[i][0] = fl.V[i][0] / atmos['a']  # Mach number at time t
            fl.g[i][0] = np.sqrt(fl.Ay[i][0] ** 2 + fl.Ax[i][0] ** 2) / u.g0  # Acceleration (G)
            fl.force[i][0] = m[i][0] * (np.sqrt(fl.Ay[i][0] ** 2 + fl.Ax[i][0] ** 2)) + fl.drag[i][0]

            # Gravity turn
            if (i > 1) and (fl.s[i][0] > self.input['settings']['LRail']):  # If clear from launch rail

                vt = [fl.u[i - 1][0], fl.v[i - 1][0]]  # Velocity at i-1
                vtp = [fl.u[i][0], fl.v[i][0]]  # Velocity at i
                mag = abs(fl.V[i][0]) * abs(fl.V[i - 1][0])  # Product of total velocitues
                dtheta = np.arccos(min(np.dot(vt, vtp) / mag, 1))  # delta theta
                fl.theta[i][0] = fl.theta[i - 1][0] + dtheta  # Update theta
            else:

                fl.theta[i][0] = fl.theta[i - 1][0]  # Update theta

        # Write to classes
        fl.m = m
        fl.altBO = fl.y[: 0]
        self.flight = fl
        prop.performance = perf

    def get6DoFflightDynamics(self):
        '''#-----------------------------------------------------------------------
        #   METHOD: get6DOFflightDynamics
        #   Compute the 3D trajectory of the rocket's flight
        #
        #   INPUTS: NONE
        #   OUTPUTS: NONE
        #-----------------------------------------------------------------------'''

        #   --------------------------------------------------------------------
        #   get 6DoF flight Dynamics
        #   Need to research further here
        #   useful tips:
        #   self.util.zeroArray() --->
        #       def zeroArray(self):return np.zeros((self.input["sim"]["numpt"], 1))
        #       -- numpy array of zeros
        #   property class supposed to be empty
        #   Note: a lot of the called classes are not implemented
        #   Dont worry about those, maintain the same function calls
        #   focus on adding the 6DoF aspect
        #   --------------------------------------------------------------------
        pass



    def simulate(self):
        print("Running Simulation")