import numpy as np
import RocketSimulationClassFiles as rocket
from RocketSimulationClassFiles import rocketVersionFiles

import rocketVersionFiles


class SimulationClass1:
    def __init__(self, selectedInput):
        if not selectedInput:
            raise Exception('ERROR: no rocket input selected')
        else:
            print()
            rocket = self.getRocketSpecs(selectedInput)

    def getRocketSpecs(self, input_selector):
        if input_selector == "houbolt_jr_single":
            ####rocketInput.yaml file might need to be changed#### (IF CHANGING TO 3D)
            return rocketVersionFiles.houbolt_jr_single(
                'RocketSimulationClassFiles/rocketVersionFiles/rocketInput.yaml')
        # elif input_selector == ""
        else:
            raise Exception('Invalid rocket input')
