from src.tests import *
from src.essentials.tools import binaryToArray, RESULT_OUTPUT

def runTests():
    #data = genNumbers(48000000, 32)  # gen 2.4 million 32-bit values
    data = binaryToArray(RESULT_OUTPUT, True)
    countOnes.init(data, True)
    squeezeTest.init(data, True)
    parkingLot.init(data, True)

    gc.collect()
