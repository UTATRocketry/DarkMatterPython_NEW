#Since in the run file, we need to create __init__ to individually import each class file
#so it can be called using Rocket in run file
#ask question in meeting, we need want to import it seperately or as a function

from .SimulationClass1 import SimulationClass1
from .RocketClass2 import RocketClass2
from .UtilityClass2 import UtilityClass2