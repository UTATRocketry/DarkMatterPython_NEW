import numpy as np
import RocketSimulationClassFiles as rocket
from RocketSimulationClassFiles import rocketVersionFiles

import rocketVersionFiles


class SimulationClass1:
    def __init__(self, selectedInput):
        if not selectedInput:
            raise Exception('ERROR: no rocket input selected')
        else:
            print("Building Simulation")
            self.rocketSpecs = self.getRocketSpecs(selectedInput)
            print("No errors: RocketSpecs Retrieval successful")

            #get level 2 module (rocket and utility Class)
            self.rocket = rocket.rocketClass2(self.rocketSpecs)
            self.utilityClassInfo = rocket.utilityClass2(self.rocketSpecs)
    def getRocketSpecs(self, input_selector):
        if input_selector == "houbolt_jr_single":
            ####rocketInput.yaml file might need to be changed#### (IF CHANGING TO 3D)
            return rocketVersionFiles.houbolt_jr_single(
                'RocketSimulationClassFiles/rocketVersionFiles/rocketInput.yaml')
        # elif input_selector == ""
        else:
            raise Exception('Invalid rocket input')