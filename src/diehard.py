from src.tests import *
from src.essentials.tools import binaryToArray, RESULT_OUTPUT


def runTests(from_random: bool = False):
    data = genNumbers(48000000, 32) if from_random else binaryToArray(RESULT_OUTPUT, True)
    countOnes.init(data, True)
    squeezeTest.init(data, True)
    parkingLot.init(data, True)

    gc.collect()
