import RocketSimulationClassFiles as rocket
import numpy as np

class RocketClass2:

    #--------------------------------------------------------------------------------------------
    #   METHOD: rocketClass
    #   Constructs rocketClass given required inputs.
    #
    #   INPUTS \..........................................................
    #     - <input> (struct)        : A structure that contains all input variables
    #     - <utilities> (stuct)     : A structure that contains all necessary utilities
    #     - <propulsion> (struct)   : A structure that contains all necessary propulsion data
    #     - <airframe> (struct)     : A structure containing all necessary airframe data
    #   OUTPUTS ............................................................
    #     - <self> (class):    Returns created rocketClass
    #--------------------------------------------------------------------------------------------

    def __init__(self, input):
        #no need to check input is there, already checked in upper levels
        print("Building Rocket Class")
        self.input = input
        self.propulsion = rocket.PropulsionClass3(input)
        self.airframe = rocket.propertyClass2()
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