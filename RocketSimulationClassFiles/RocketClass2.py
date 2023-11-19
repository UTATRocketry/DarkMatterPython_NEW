import RocketSimulationClassFiles as rocket
import numpy as np

class RocketClass2:
    def __init__(self, input):
        #no need to check input is there, already checked in upper levels
        print("Building Rocket Class")
        self.input = input
        self.propulsion = rocket.PropulsionClass3(input)

        #add airfram and utilities later

    def get_flight_type(self):
        #   Settings' is attribute storing a dict-like object : 'flightType'
        #   Add later
        return self.settings['flightType']