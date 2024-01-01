import RocketSimulationClassFiles as rocket
import numpy as np

class RocketClass2:
    def __init__(self, input):
        #no need to check input is there, already checked in upper levels
        print("Building Rocket Class")
        self.input = input
        self.propulsion = rocket.PropulsionClass3(input)
        self.airframe = rocket.airframeClass3()
        self.utilities = rocket.UtilityClass2(input)
        self.airframe.drag_file = "DMpkg/Drag_Data_Houbolt_Jr.csv"
        self.drag_model()



    def get_flight_type(self):
        #   Settings' is attribute storing a dict-like object : 'flightType'
        #   Add later
        return self.settings['flightType']
    def drag_model(self):
        drag_data = np.genfromtxt(self.airframe.drag_file, delimiter = ',')
        self.airframe.cd = np.polynomial.Polynomial.fit(drag_data[:,0], drag_data[:,1], deg=3)