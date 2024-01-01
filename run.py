import RocketSimulationClassFiles as Rocket

def main():
    rocketVersion = 'houbolt_jr_single'
    instance1 = Rocket.SimulationClass1(rocketVersion)
    instance1.simulate()
    print("Complete")

    # Uncomment the following lines if you want to use them
    # from RocketSimulationClassFiles.showOutputMenu import createAllPlots, showOutputMenu
    # createAllPlots()
    # showOutputMenu()

if __name__ == "__main__":
    main()