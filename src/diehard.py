from src.tests import *
from src.essentials.tools import binaryToArray, RESULT_OUTPUT


def runTests(from_random: bool = False):
    data = genNumbers(6500000, 32) if from_random else binaryToArray(RESULT_OUTPUT, True)   # using random lib to valid tests
    countOnes.init(data, True)
    squeezeTest.init(data, True)
    parkingLot.init(data, True)

    gc.collect()
