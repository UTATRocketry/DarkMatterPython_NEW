import RocketSimulationClassFiles as rocket
class PropulsionClass3:

    def __init__(self, input):
        self.input = input
        self.combustion = rocket.CombustionClass4(input)
        self.nozzle = rocket.NozzleClass4(input)