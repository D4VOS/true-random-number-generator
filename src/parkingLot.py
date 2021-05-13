import math
import pickle

import scipy.stats as sc

BINARY_OUTPUT = "trn.bin"
FAKE = "fake.bin"

NO_TRIALS = 12000
NO_TESTS = 100
UNIMAX = 4294967296.  # unsigned max value of 32-bit
RATIO = 100 / UNIMAX


def fakebin():
    with open(FAKE, 'wb') as file:
        for i in range(9600000):
            byte_arr = [1]
            binary_format = bytearray(byte_arr)
            file.write(binary_format)


def park():
    with open(BINARY_OUTPUT, 'rb') as file:
        sum, ss = 0, 0
        p = [0.] * NO_TESTS
        z = list()
        for test in range(1, NO_TESTS + 1):  # 100 testow
            x = [0.] * NO_TRIALS
            y = [0.] * NO_TRIALS

            '''first parking'''
            first = float(int(file.readline()) * RATIO)
            second = float(int(file.readline()) * RATIO)
            x[0] = first
            y[0] = second
            no_success = 1

            for attempt in range(0, NO_TRIALS - 1):
                first = float(int(file.readline()) * RATIO)
                second = float(int(file.readline()) * RATIO)
                crashed = False
                for i in range(no_success):
                    if math.fabs(x[i - 1] - first) <= 1.0 and math.fabs(y[i - 1] - second) <= 1.0:
                        crashed = True
                        break
                if not crashed:
                    x[no_success] = first
                    y[no_success] = second
                    no_success += 1

            z.append((no_success - 3523.0) / 21.9)
            print(f"No.{test}\t\tNo.parked = {no_success}")

    with open('./zout.txt', 'wb') as fp:
        pickle.dump(z, fp)

    z = kolomagsmirn()
    print(list(z))

    kstestres = sc.kstest(z, 'norm')
    print(f"\t p-value of KSTEST for those {NO_TESTS} tests: {kstestres}")

    # =============================================================================#
    #            dieharder version 3.31.1 Copyright 2003 Robert G. Brown          #
    # =============================================================================#
    # rng_name | filename | rands / second |
    # file_input | trn.bin | 5.47e+06 |
    # =============================================================================#
    # test_name | ntup | tsamples | psamples | p - value | Assessment
    # =============================================================================#
    # The file file_input was rewound 5 times
    # diehard_parking_lot | 0 | 12000 | 100 | 0.91403506 | PASSED                   <!---- 0.91403506 EXPECTED


def phi(n):  # todo
    amount = 0
    for k in range(1, int(n) + 1):
        if gcd(n, k) == 1:
            amount += 1
    return amount


def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def eof(x, y):
    return x == '' or y == ''


def kolomagsmirn():
    with open('./zout.txt', 'rb') as fp:
        return pickle.load(fp)


#park()
# fakebin()
print(sc.kstest(kolomagsmirn(), 'norm'))