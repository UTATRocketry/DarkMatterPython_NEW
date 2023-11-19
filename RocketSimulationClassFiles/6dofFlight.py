import numpy as np
import RocketSimulationClassFiles as rocket


#helper functions

#setup empty dictionaries containing each property variables

class setup_dict(dict):
    #ease up the difficulty changing  values.
    __setattr__ = dict.__setattr__


#setup flight dynamic variables used for 6dof calcualtions
class dof_6_FlightDynamics():
    # -----------------------------------------------------------------------
    #   Class: dof_6_FlightDynamics 
    #        Performs calculation on the 6dof and simulates rocket movement
    #           includes 3 axis coordinates, moment around each axis
    #   INPUTS \..........................................................
    #     - <input> : NONE
    #   OUTPUTS ............................................................
    #       No outputs
    # -----------------------------------------------------------------------
    #file structure not decided yet
    def __init__(self, files):
        self.enable = False

    #set each property as the setup_dict class
    #stored in dict form, order only for readability 
        #contains axial force [0], side force [1], normal force [2]
        self.forces = setup_dict()
        
        #stores drag values could be deleted later
        self.aerodynamic_coe = setup_dict()
        
        #contains rolling moment [0], pitching moment [1], Yawing moment[2]
        self.moment = setup_dict()

        # x, y, z coordinate with respect to fixed ground axis [0:2]
        self.positions = setup_dict()

        # translational velocities [0:2] u, v, w 
        # rotational velocities [3:5] p, q, r
        self.velocities = setup_dict()

        # translational accelerations [0:2] du, dv, dw 
        # rotational accelerations [3:5] dp, dq, dr
        self.acceleration = setup_dict()

        # moment of inertia [0:2] Ixx, Iyy, Izz
        self.moment_inertia = setup_dict()

        #other helper variables: linear momentum, angular momentum, etc.
        self.momentum = setup_dict()

    #define variable in each property
    def enable(self):
        force = ['Axial','Side','Normal']
        #undefined right now
        aerodynamic_coe = []
        moment = ['Rollng', 'Pitching', 'Yawing']
        position = ['x','y','z']
        velocities = ['u','v','w','p','q','r']
        acceleration = ['du','dv','dw','dp','dq','dr']
        moment_inertia = ['Ix','Iy','Iz']
        momentum = ['L_','H_']

    #performs calculation and feeds to the variables
    def calculations(self):
        pass
    
    #loads in thrust 
    def load_variables(self, input_selector):
        #same as 2dof calculations for engine ignition
        pass

    #reports the value of each state at time = t, or pass on all values
    def states_repot(self,time):
        if time == None:
            pass
        else:
            pass
        pass

    #feedsback the value of a specific type
    def value(self, type, value):
        pass
