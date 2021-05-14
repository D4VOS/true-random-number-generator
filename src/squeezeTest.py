from scipy.stats import chisquare
import random
import matplotlib.pyplot as plt

NO_SAMPLES = 100000

def squeezeTest():
    more = 0
    less = 0
    results = []

    floats = genNumbers(NO_SAMPLES, 32)  # generate 100k 32-bit numbers
    floats = [floats[i] / 4294967295 for i in range(len(floats))]  # -> [0;1)

    for i in range(len(floats)):
        k = 2147483647
        j = 0
        while k >= 1:
            k *= floats[i]
            j += 1

        if j < 6:
            less += 1
            results.append(j)
        elif j > 48:
            more += 1
            results.append(j)
    results.sort()
    plt.hist(results, bins=30)
    plt.show()

    print(f'j > 48: {more} times.\nj < 6: {less} times.\n'
          f'chisquare={chisquare(results)}')


def genNumbers(count: int, bits: int) -> list[int]:
    return [random.randrange(0, 2 ** bits) for _ in range(count)]


if __name__ == "__main__":
    squeezeTest()
