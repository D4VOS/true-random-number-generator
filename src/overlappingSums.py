import matplotlib.pyplot as plt
from scipy.stats import *

BINARY_OUTPUT = "binaryout.bin"


def overlap():
    with open(BINARY_OUTPUT, 'rb') as f:
        floats = []
        [floats.append(int(i.strip()) / 4294967295) for i in f.readlines()]
    '''for i in range(2400000):
        number = random.randint(0, 255)
        floats.append(number/255)'''

    tmp = []
    [tmp.append(sum([floats[j]/100 for j in range(i, i + 100)])) for i in range(len(floats) - 100)]
    tmp.sort()
    print(len(tmp), np.mean(tmp))
    x = np.linspace(tmp[0], tmp[len(tmp) - 1], num=len(tmp) - 1)
    print(f'x={x}, len={len(tmp)},\n{normaltest(tmp)}')
    y_axis = np.ones_like(tmp) / len(tmp)
    plt.hist(tmp, bins=300, weights=y_axis)
    plt.show()


def shittyoverlappingsums():
    print("\n\n\nOverlapping sums:")
    try:
        with open(BINARY_OUTPUT, 'rb') as f:
            floats = []
            [floats.append(int(i.strip()) / 4294967295) for i in f.readlines() if i.strip()]

        f.close()

        tmp = []
        [tmp.append(sum([floats[j] for j in range(i, i + 100)])) for i in range(len(floats) - 100)]
        tmp.sort()
        x = np.linspace(tmp[0], tmp[len(tmp) - 1], num=len(tmp) - 1)
        print(f'x={x}, len={len(tmp)},\n{kstest(x, "norm")}')

        # return [sum([floats[j] for j in range(i, i + 100)]) for i in range(len(floats) - 100)] # if u want to use them (rocket science here, fuck u PEP8.)
        plt.hist(tmp)
        plt.show()
    except Exception as e:
        print(e)

    return


overlap()
