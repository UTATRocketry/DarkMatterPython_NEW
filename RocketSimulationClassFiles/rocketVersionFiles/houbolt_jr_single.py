import math
import yaml
import DMpkg as rocket
from DMpkg.utilitiesClass import cellss


# -----------------------------------------------------------------------
#   METHOD: houbolt_jr_single
#   Creates dictionary with inputs from input.yaml file
#
#   INPUTS \..........................................................
#     - <inp_path>  (String):     Path to input.yaml file
#   OUTPUTS ............................................................
#     - <inp_dic>   (Dictionary): Dictionary with inputs from input.yaml file and manual design parameters / calculations
# -----------------------------------------------------------------------
def houbolt_jr_single(inp_path):
    with open(inp_path, "r") as f:
        inp_dic = yaml.full_load(f)

    # conversions and calculations that cannot be handled in the input.yaml file
    inp_dic["design"]['tBurn'] = [8.4]  # Engine burn time                                  [s]
    inp_dic["design"]['mDotox'] = [0.8]  # Design Ox mdot                                    [kg/s]
    inp_dic["design"]['thetaL'] = [3]  # Launch angle                                      [degrees]
    inp_dic["design"]['diameter'] = [0.1524]  # Rocket diameter                                   [m]
    inp_dic["design"]['Pcc'] = [350]  # Design chamber pressure                           [psi]
    inp_dic["design"]['OF'] = [3]  # Design OF ratio                                   [double]
    inp_dic["design"]['injCd'] = [0.4]  # Injector discharge coeff.                         [double]

    inp_dic["fPres"]["Pinit"] = inp_dic["fPres"]["Pinit"] * inp_dic["settings"]["cnv"]  # converting from psi to Pa
    inp_dic["fPres"]["mInit"] = inp_dic["fPres"]["vTank"] * inp_dic["fPres"]["Rhoinit"]

    inp_dic["fuel"]["Pinit"] = inp_dic["fuel"]["Pinit"] * inp_dic["settings"]["cnv"]  # converting from psi to Pa
    inp_dic["fuel"]["vTank"] = inp_dic["fuel"]["mInit"] * (1 + inp_dic["fuel"]["ullage"]) / inp_dic["fuel"][
        "Rhoinit"]  # converting from psi to Pa
    inp_dic["fuel"]["lTank"] = inp_dic["fuel"]["vTank"] / (
                math.pi * (0.5 * inp_dic["design"]["diameter"][0] - inp_dic["fuel"]["tTank"]) ** 2)

    inp_dic["oxPres"]["Pinit"] = inp_dic["oxPres"]["Pinit"] * inp_dic["settings"]["cnv"]  # converting from psi to Pa
    inp_dic["oxPres"]["mInit"] = inp_dic["oxPres"]["vTank"] * inp_dic["oxPres"]["Rhoinit"]

    inp_dic["ox"]["Pinit"] = inp_dic["ox"]["Pinit"] * inp_dic["settings"]["cnv"]  # converting from psi to Pa
    inp_dic["ox"]["vTank"] = inp_dic["ox"]["mInit"] * (1 + inp_dic["ox"]["ullage"]) / inp_dic["ox"]["Rhoinit"]
    inp_dic["ox"]["lTank"] = inp_dic["ox"]["vTank"] / (
                math.pi * (0.5 * inp_dic["design"]["diameter"][0] - inp_dic["ox"]["tTank"]) ** 2)

    inp_dic["props"] = cellss(4, 3)
    inp_dic["props"][0][0] = 'Pressurant'
    inp_dic["props"][0][1] = inp_dic["fPres"]
    inp_dic["props"][0][2] = 0
    inp_dic["props"][1][0] = 'Fuel'
    inp_dic["props"][1][1] = inp_dic["fuel"]
    inp_dic["props"][1][2] = 1
    inp_dic["props"][2][0] = 'Pressurant'
    inp_dic["props"][2][1] = inp_dic["oxPres"]
    inp_dic["props"][2][2] = 2
    inp_dic["props"][3][0] = 'Oxidizer'
    inp_dic["props"][3][1] = inp_dic["ox"]
    inp_dic["props"][3][2] = 3

    return inp_dic