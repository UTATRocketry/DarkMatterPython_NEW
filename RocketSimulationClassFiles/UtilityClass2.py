import RocketSimulationClassFiles as Rocket
import math
import numpy as np

class UtilityClass2:
    def __init__(self, input):
        print("Building Utility Class")

        #copied from old code, assuming no changed need to be made
        self.g0 = 9.8056
        self.earthR = 6371e3
        self.input = input

        self.R = 8314
        self.airR = 287.05
        self.n2R = 8314 / 28
        self.airM = 0.0289644  # molar mass of air (kg/mol)
        self.airGamma = 1.4

        self.cnv = 6894.76

        self.coolProp_conversions = ('C2H5OH', 'Ethanol')

        self.noxProp = rocket.propertyClass()
        self.noxProp.rho_c = 452
        self.noxProp.Tc = 309.57
        self.noxProp.Pc = 7.251e6

        self.noxProp.Coefs = rocket.propertyClass()
        self.noxProp.Coefs.V1 = 96.512
        self.noxProp.Coefs.V2 = -4045
        self.noxProp.Coefs.V3 = -12.277
        self.noxProp.Coefs.V4 = 2.886e-5
        self.noxProp.Coefs.V5 = 2

        self.noxProp.Coefs.T1 = 2.3215e7
        self.noxProp.Coefs.T2 = 0.384
        self.noxProp.Coefs.T3 = 0
        self.noxProp.Coefs.T4 = 0

        self.noxProp.Coefs.Q1 = 2.781
        self.noxProp.Coefs.Q2 = 0.27244
        self.noxProp.Coefs.Q3 = 309.57
        self.noxProp.Coefs.Q4 = 0.2882

        self.noxProp.Coefs.D1 = 0.2934e5
        self.noxProp.Coefs.D2 = 0.3236e5
        self.noxProp.Coefs.D3 = 1.1238e3
        self.noxProp.Coefs.D4 = 0.2177e5
        self.noxProp.Coefs.D5 = 479.4

        self.noxProp.Coefs.E1 = 6.7556e4
        self.noxProp.Coefs.E2 = 5.4373e1
        self.noxProp.Coefs.E3 = 0
        self.noxProp.Coefs.E4 = 0
        self.noxProp.Coefs.E5 = 0

        self.noxProp.Coefs.b1 = 1.72328
        self.noxProp.Coefs.b2 = -0.8395
        self.noxProp.Coefs.b3 = 0.5106
        self.noxProp.Coefs.b4 = 0.10412

        self.noxProp.Coefs.q1 = -6.71893
        self.noxProp.Coefs.q2 = 1.35966
        self.noxProp.Coefs.q3 = 1.3779
        self.noxProp.Coefs.q4 = -4.051

        self.nitrogen = rocket.propertyClass()
        self.nitrogen.Coefs = rocket.propertyClass()
        self.nitrogen.Coefs.C1 = 0.28883e5
        self.nitrogen.Coefs.C2 = 0
        self.nitrogen.Coefs.C3 = 0
        self.nitrogen.Coefs.C4 = 0
        self.nitrogen.Coefs.C5 = 0

        self.nitrogen.h = rocket.propertyClass()
        self.nitrogen.h.theta = np.array([0.90370032155133, \
                                          -3.99164830787538, \
                                          4.44554878990612, \
                                          -1.68387394930366, \
                                          1.84282855081908, \
                                          -2.71807522455834, \
                                          1.80658523674363, \
                                          -0.00026662830718, \
                                          0.16405364316350])

        self.nitrogen.h.alpha = np.array([1, \
                                          0.45607085009281, \
                                          0.99224794564113, \
                                          1.58495789262624, \
                                          0.53133147588636, \
                                          1.29132167947510, \
                                          1.44008913900161, \
                                          2.74997487910292, \
                                          2.36611999082672])

        self.nitrogen.l = rocket.propertyClass()

        self.nitrogen.l.theta = np.array([0.46742656471647, \
                                          -0.53799565472298, \
                                          -9.22454428760102, \
                                          9.15603503101003, \
                                          3.18808664459882, \
                                          0.30163700042055, \
                                          -0.27300234680706, \
                                          -1.00749719408221, \
                                          -1.49106816983329])

        self.nitrogen.l.alpha = np.array([1, \
                                          1.41102397459172, \
                                          0.33562799290636, \
                                          0.79810083070486, \
                                          0.01008992455881, \
                                          2.53968667359886, \
                                          2.51281397715323, \
                                          1.20879498088509, \
                                          1.69572064361084])

        self.nitrogen.Tc = 126.2
        self.nitrogen.Pc = 492.314

        self.cp = PropsSI

        self.coolprop_alias = cellss(1, 2)
        self.coolprop_alias[0][0] = 'C2H5OH'
        self.coolprop_alias[0][1] = 'Ethanol'
    def zeroArray(self):
        return np.zeros((self.input["sim"]["numpt"], 1))