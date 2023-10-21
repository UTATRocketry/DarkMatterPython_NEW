class SimulationClass1:
    def __init__(self, input_selector):
        if not input_selector:
            raise Exception('ERROR: simulationClass constructor executed without input arguments')
        else:
            rocket = input_selector