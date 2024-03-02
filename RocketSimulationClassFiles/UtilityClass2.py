import RocketSimulationClassFiles as Rocket
import math
from CoolProp.CoolProp import PropsSI
import numpy as np


def cellss(x, y):

    output = [[[] for _ in range(y)] for _ in range(x)]
    print("Cells x:", x, "y:", y, "output:", output)
    return output
class UtilityClass2:

    #optimized cellss function
    #-----------------------------------------------------------------------
    #   METHOD: cellss
    #   Creates 2D python list
    #
    #   INPUTS \..........................................................
    #     - <x> (numeric):    Number of rows
    #     - <y> (numeric):    Number of columns
    #   OUTPUTS ............................................................
    #     - <output> (list):    Returns list with x rows and y columns
    #-----------------------------------------------------------------------
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

        self.noxProp = Rocket.propertyClass()
        self.noxProp.rho_c = 452
        self.noxProp.Tc = 309.57
        self.noxProp.Pc = 7.251e6

        self.noxProp.Coefs = Rocket.propertyClass()
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

        self.nitrogen = Rocket.propertyClass()
        self.nitrogen.Coefs = Rocket.propertyClass()
        self.nitrogen.Coefs.C1 = 0.28883e5
        self.nitrogen.Coefs.C2 = 0
        self.nitrogen.Coefs.C3 = 0
        self.nitrogen.Coefs.C4 = 0
        self.nitrogen.Coefs.C5 = 0

        self.nitrogen.h = Rocket.propertyClass()
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

        self.nitrogen.l = Rocket.propertyClass()

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



    #Below 3 Functions does not need to be changed
    #Same in 6DoF as 2DoF
    def stdAtmos(self, altitude) -> dict:

        Ru = self.R / 1000  # universal gas constant (J/mol/K)
        Ra = self.airR

        if (0 <= altitude) and (altitude < 11000):
            Lb = -0.0065  # Lapse rate (K/m)
            Tb = 288.15  # Standard temperature (K)
            Pb = 101325  # Static pressure (Pa)
            h0 = 0
            P = Pb * (Tb / (Tb + Lb * (altitude - h0))) ** (self.g0 * self.airM / Ru / Lb)
            T = Tb + Lb * (altitude - h0)

        elif (11000 <= altitude) and (altitude < 20000):
            Lb = 0
            Tb = 216.65
            Pb = 22632.1
            h1 = 11000
            P = Pb * math.exp(-self.g0 * self.airM * (altitude - h1) / Ru / Tb)
            T = Tb + Lb * (altitude - h1)

        elif (20000 <= altitude) and (altitude < 32000):
            Lb = 0.001
            Tb = 216.65
            Pb = 5474.89
            h2 = 20000
            P = Pb * (Tb / (Tb + Lb * (altitude - h2))) ** (self.g0 * self.airM / Ru / Lb)
            T = Tb + Lb * (altitude - h2)

        elif (32000 <= altitude) and (altitude < 47000):
            Lb = 0.0028
            Tb = 228.65
            Pb = 868.02
            h3 = 32000
            P = Pb * (Tb / (Tb + Lb * (altitude - h3))) ** (g * self.airM / Ru / Lb)
            T = Tb + Lb * (altitude - h3)

        elif (47000 <= altitude) and (altitude < 51000):
            Lb = 0
            Tb = 270.65
            Pb = 110.91
            h4 = 47000
            P = Pb * math.exp(-self.g0 * self.airM * (altitude - h4) / Ru / Tb)
            T = Tb + Lb * (altitude - h4)

        elif (51000 <= altitude) and (altitude < 71000):
            Lb = -0.0028
            Tb = 270.65
            Pb = 66.94
            h5 = 51000
            P = Pb * (Tb / (Tb + Lb * (altitude - h5))) ** (self.g0 * self.airM / Ru / Lb)
            T = Tb + Lb * (altitude - h5)

        elif (71000 <= altitude) and (altitude < 86000):
            Lb = -0.002
            Tb = 214.65
            Pb = 3.96
            h6 = 71000
            P = Pb * (Tb / (Tb + Lb * (altitude - h6))) ** (self.g0 * self.airM / Ru / Lb)
            T = Tb + Lb * (altitude - h6)

        else:
            P = 0
            print(altitude)

        rho = P / (Ra * T)
        a = math.sqrt(1.4 * Ra * T)
        output = {}
        output['P'] = P
        output['T'] = T
        output['rho'] = rho
        output['a'] = a
        return output

    # -----------------------------------------------------------------------
    #   METHOD: get_dZdT_N2
    #   Calculates dZ/dT partial derivative for nitrogen
    #
    #   INPUTS \..........................................................
    #     - <T> (numeric):  Temperature
    #     - <P> (numeric):  Pressure
    #   OUTPUTS ............................................................
    #     - <dZdT> (numeric):    Returns value of partial derivative of Z wrt temperature
    # -----------------------------------------------------------------------
    def get_dZdT_N2(self, T, P):

        if (T >= 220 and T <= 320) and (P >= 800 and P <= 4500):

            nh = self.nitrogen.h
            T = T / self.nitrogen.Tc
            P = P / self.nitrogen.Pc

            dZdTr = nh.theta[1] * nh.alpha[1] * T ** (nh.alpha[1] - 1) * P ** 0.7 \
                    + nh.theta[2] * nh.alpha[2] * T ** (nh.alpha[2] - 1) * P ** 0.5 \
                    + nh.theta[3] * nh.alpha[3] * T ** (nh.alpha[3] - 1) * P ** 0.3 \
                    + nh.theta[4] * nh.alpha[4] * T ** (nh.alpha[4] - 1) * P \
                    + nh.theta[5] * nh.alpha[5] * T ** (nh.alpha[5] - 1) * P \
                    + nh.theta[6] * nh.alpha[6] * T ** (nh.alpha[6] - 1) * P \
                    + nh.theta[8] * nh.alpha[8] * T ** (nh.alpha[8] - 1)

            dZdT = dZdTr / self.nitrogen.Tc

        elif (T >= 180 and T < 220) and (P >= 800 and P <= 4500):

            nl = self.nitrogen.l
            T = T / self.nitrogen.Tc
            P = P / self.nitrogen.Pc

            dZdTr = nl.theta[1] * nl.alpha[1] * T ** (nl.alpha[1] - 1) * P ** 0.7 \
                    + nl.theta[2] * nl.alpha[2] * T ** (nl.alpha[2] - 1) * P ** 0.5 \
                    + nl.theta[3] * nl.alpha[3] * T ** (nl.alpha[3] - 1) * P ** 0.3 \
                    + nl.theta[4] * nl.alpha[4] * T ** (nl.alpha[4] - 1) * P \
                    + nl.theta[5] * nl.alpha[5] * T ** (nl.alpha[5] - 1) * P \
                    + nl.theta[6] * nl.alpha[6] * T ** (nl.alpha[6] - 1) * P \
                    + nl.theta[8] * nl.alpha[8] * T ** (nl.alpha[8] - 1)

            dZdT = dZdTr / self.nitrogen.Tc

        else:
            if (T < 180 or T > 320):
                T = 180
                nl = self.nitrogen.l
                T = T / self.nitrogen.Tc
                P = P / self.nitrogen.Pc

                dZdTr = nl.theta[1] * nl.alpha[1] * T ** (nl.alpha[1] - 1) * P ** 0.7 \
                        + nl.theta[2] * nl.alpha[2] * T ** (nl.alpha[2] - 1) * P ** 0.5 \
                        + nl.theta[3] * nl.alpha[3] * T ** (nl.alpha[3] - 1) * P ** 0.3 \
                        + nl.theta[4] * nl.alpha[4] * T ** (nl.alpha[4] - 1) * P \
                        + nl.theta[5] * nl.alpha[5] * T ** (nl.alpha[5] - 1) * P \
                        + nl.theta[6] * nl.alpha[6] * T ** (nl.alpha[6] - 1) * P \
                        + nl.theta[8] * nl.alpha[8] * T ** (nl.alpha[8] - 1)

                dZdT = dZdTr / self.nitrogen.Tc

            elif (P < 800 or P > 4500):
                raise Exception('utilitiesClass > get_dZdP(): Pressure is out off acceptable bounds (P = %f)', P)

        return dZdT

    # -----------------------------------------------------------------------
    #   METHOD: get_dZdP_N2
    #   Calculates dZ/dP partial derivative for nitrogen
    #
    #   INPUTS \..........................................................
    #     - <T> (numeric):  Temperature
    #     - <P> (numeric):  Pressure
    #   OUTPUTS ............................................................
    #     - <dZdP> (numeric):    Returns value of partial derivative of Z wrt pressure
    # -----------------------------------------------------------------------
    def get_dZdP_N2(self, T, P):

        if (T >= 220 and T <= 320) and (P >= 800 and P <= 4500):

            nh = self.nitrogen.h
            T = T / self.nitrogen.Tc
            P = P / self.nitrogen.Pc

            dZdPr = 0.7 * nh.theta[1] * T ** nh.alpha[1] * P ** (-0.3) \
                    + 0.5 * nh.theta[2] * T ** nh.alpha[2] * P ** (-0.5) \
                    + 0.3 * nh.theta[3] * T ** nh.alpha[3] * P ** (-0.7) \
                    + nh.theta[4] * T ** nh.alpha[4] \
                    + nh.theta[5] * T ** nh.alpha[5] \
                    + nh.theta[6] * T ** nh.alpha[6] \
                    + nh.theta[7] * nh.alpha[7] * P ** (nh.alpha[7] - 1)

            dZdP = dZdPr / self.nitrogen.Pc

        elif (T >= 180 and T < 220) and (P >= 800 and P <= 4500):

            nl = self.nitrogen.l
            T = T / self.nitrogen.Tc
            P = P / self.nitrogen.Pc

            dZdPr = 0.7 * nl.theta[1] * T ** nl.alpha[1] * P ** (-0.3) \
                    + 0.5 * nl.theta[2] * T ** nl.alpha[2] * P ** (-0.5) \
                    + 0.3 * nl.theta[3] * T ** nl.alpha[3] * P ** (-0.7) \
                    + nl.theta[4] * T ** nl.alpha[4] \
                    + nl.theta[5] * T ** nl.alpha[5] \
                    + nl.theta[6] * T ** nl.alpha[6] \
                    + nl.theta[7] * nl.alpha[7] * P ** (nl.alpha[7] - 1)

            dZdP = dZdPr / self.nitrogen.Pc

        else:
            if (T < 180 or T > 320):
                T = 180
                nl = self.nitrogen.l
                T = T / self.nitrogen.Tc
                P = P / self.nitrogen.Pc

                dZdPr = 0.7 * nl.theta[1] * T ** nl.alpha[1] * P ** (-0.3) \
                        + 0.5 * nl.theta[2] * T ** nl.alpha[2] * P ** (-0.5) \
                        + 0.3 * nl.theta[3] * T ** nl.alpha[3] * P ** (-0.7) \
                        + nl.theta[4] * T ** nl.alpha[4] \
                        + nl.theta[5] * T ** nl.alpha[5] \
                        + nl.theta[6] * T ** nl.alpha[6] \
                        + nl.theta[7] * nl.alpha[7] * P ** (nl.alpha[7] - 1)

                dZdP = dZdPr / self.nitrogen.Pc
            elif (P < 800 or P > 4500):
                raise Exception('utilitiesClass > get_dZdP(): Pressure is out off acceptable bounds (P = %f)', P)

        return dZdP
