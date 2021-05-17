from tests import *


def main():
    data = genNumbers(48000000, 32)  # gen 2.4 million 32-bit values

    countOnes.init(data, True)
    squeezeTest.init(data, True)
    parkingLot.init(data, True)

    gc.collect()


if __name__ == "__main__":
    main()
