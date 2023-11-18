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
            self.utilityClassInfo = Rocket.UtilityClass2(self.rocketSpecs)


            #load rocket properties - PropertyClass2
            self.flight = Rocket.PropertyClass2()
            #listing out properties

            #make sure that this exists in the input later
            self.flight.type = self.rocket.get_flight_type()





    def getRocketSpecs(self, input_selector):
        if input_selector == "houbolt_jr_single":
            # rocketInput.yaml file might need to be changed (IF CHANGING TO 3D)
            return rocketVersionFiles.houbolt_jr_single(
                'RocketSimulationClassFiles/rocketVersionFiles/rocketInput.yaml')
        # elif input_selector == ""
        else:
            raise Exception('Invalid rocket input')

    def simulate(self):
        print("Running Simulation")

    def setSimulationDynamicsType(self):
    # -----------------------------------------------------------------------
    #   Previous code only has 2dof
    #   Now chnaged to 6DOF
    # -----------------------------------------------------------------------
        if self.flight.type == '6DOF':
            self.flight.get = self.get6DOFflightDynamics
        elif self.flight.type == '2DOF':
            self.flight.get = self.get2DOFflightDynamics
        else:
            raise ValueError(f"Undefined flight type: {self.flight.type}")

    def get2DOFflightDynamics(self):
        pass

    def get6DOFflightDynamics(self):
        pass