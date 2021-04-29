import math
import scipy.stats as sc

BINARY_OUTPUT = "binaryout.bin"

NO_TRIALS = 12000
NO_TESTS = 10
UNIMAX = 4294967296.  # unsigned max value of 32-bit
RATIO = 100 / UNIMAX


def park():
    with open(BINARY_OUTPUT, 'rb') as file:
        sum, ss = 0, 0
        p = [0.] * 100
        for test in range(1, NO_TESTS + 1):  # 100 testow

            x = [0.] * NO_TRIALS
            y = [0.] * NO_TRIALS
            '''first parking'''
            first = float(int.from_bytes(file.read(4), byteorder='big', signed=False) * RATIO)
            second = float(int.from_bytes(file.read(4), byteorder='big', signed=False) * RATIO)
            x[0] = first
            y[0] = second
            no_success = 1

            for attempt in range(0, NO_TRIALS):
                first = float(int.from_bytes(file.read(4), byteorder='big', signed=False) * RATIO)
                second = float(int.from_bytes(file.read(4), byteorder='big', signed=False) * RATIO)
                crashed = False
                for i in range(no_success):
                    if math.fabs(x[i - 1] - first) <= 1.0 and math.fabs(y[i - 1] - second) <= 1.0:
                        crashed = True
                        break
                if not crashed:
                    x[attempt] = first
                    y[attempt] = second
                    no_success += 1

            sum += no_success
            ss += no_success * no_success

            z = (no_success - 3523.0) / 21.9
            p[test - 1] = 1 - phi(z)

            print(f"No.{test}\t\t{no_success}\t{z}\t\t{p[test - 1]}")

    mean = sum / NO_TESTS
    var = ss / no_success - mean * mean
    print(f"Square side=100, avg no. parked={mean} "
          f"sample std={var ** 0.5}")

    pvalue = sc.kstest(p, 'norm')
    print(f"\t p-value of KSTEST for those {NO_TESTS} tests: {pvalue}")
    #=========================================================================================================#
    # Output for first 10 tests, idk what's wrong
    #---------------------------------------------------------------------------------------------------------#
    #    Test No.  no_success    z                     P[Test No.]
    #    No.1            4817    59.08675799086758               1
    #    No.2            4938    64.61187214611873               1
    #    No.3            4845    60.365296803652974              1
    #    No.4            4969    66.02739726027397               1
    #    No.5            4902    62.96803652968037               1
    #    No.6            4945    64.93150684931507               1
    #    No.7            4793    57.99086757990868               1
    #    No.8            4821    59.269406392694066              1
    #    No.9            4984    66.7123287671233                1
    #    No.10           4884    62.14611872146119               1
    #    Square side=100, avg no. parked=4889.8 sample std=(2.991071595380618e-13+4884.790614670481j)
    #             p-value of KSTEST for those 100: KstestResult(statistic=0.5, pvalue=1.2131434371817858e-23)
    #=========================================================================================================#

def phi(n):
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


park()
