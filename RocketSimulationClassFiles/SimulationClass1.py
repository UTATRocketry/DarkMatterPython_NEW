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
        #not implementing this until 6DOF is done
        pass

    def get6DOFflightDynamics(self):
    #   --------------------------------------------------------------------
    #   get 6DoF flight Dynamics
    #   Need to research furthur here
    #   --------------------------------------------------------------------
        pass


    def simulate(self):
        print("Running Simulation")