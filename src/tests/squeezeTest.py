from src.essentials import *

NO_SAMPLES = 2400000  # should be at least 2.3 million 32 bit numbers
NO_TESTS = 100000  # don't change this
RATIO = NO_TESTS / 1000000
PI = 3.14159265359

EXPECTED = [21.03, 57.79, 175.54, 467.32, 1107.83, 2367.84,
            4609.44, 8241.16, 13627.81, 20968.49, 30176.12, 40801.97, 52042.03,
            62838.28, 72056.37, 78694.51, 82067.55, 81919.35, 78440.08, 72194.12,
            63986.79, 54709.31, 45198.52, 36136.61, 28000.28, 21055.67, 15386.52,
            10940.20, 7577.96, 5119.56, 3377.26, 2177.87, 1374.39, 849.70, 515.18,
            306.66, 179.39, 103.24, 58.51, 32.69, 18.03, 9.82, 11.21]


def init(numbers: list[int], histogram: bool = False):
    print(f"\n\nSqueeze Test:")

    current_index = 0
    p_vals = []

    exp_freq = [RATIO * EXPECTED[i] for i in range(len(EXPECTED))]
    floats = [numbers[i] / 4294967296 for i in range(len(numbers))]  # -> [0;1)

    for test in range(16):
        freq = [0] * 43  # init empty freq array
        for _ in range(NO_TESTS):
            k = 2147483647
            j = 0
            while k != 1 and j < 48:
                k = math.ceil(floats[current_index] * k)
                j += 1
                current_index += 1
            j = 6 if j < 6 else j
            freq[j - 6] += 1

        chsq = chiCalc(freq, exp_freq)
        p = 1 - Chisq(42, chsq)
        p_vals.append(p)
        print(f"{test + 1}. p-value={round(p, 6)}")

    _, p_value = sc.kstest(p_vals, 'uniform')

    print(f"Result of 16 tests: p-value={round(p_value, 6)} ", end="")
    if 0.025 < p_value < 0.975:
        print("PASSED")
    else:
        print("FAILED")
    if histogram:
        showHistogram(freq)
        showBars(p_vals)


def G(z):
    tmp = 2 * z
    if tmp != 2 * z or z == 0: print("Error in calling G(z)!!!")
    if tmp == 1:
        return math.sqrt(PI)
    elif tmp == 2:
        return 1

    return (z - 1) * G(z - 1)


def Chisq(df: int, x: float):
    if df == 1:
        return 2 * Phi(math.sqrt(x))
    elif df == 2:
        return 1 - math.exp(-x / 2)

    return Chisq(df - 2, x) - 2 * chisq(df, x)


def chisq(df: int, x: float):
    return math.pow(x / 2, (df - 2) / 2.) * math.exp(-x / 2) / (2 * G(df / 2.))


def showHistogram(freq: list[int]) -> None:
    total = sum(freq)
    total_exp = sum(EXPECTED)
    x_axis = np.linspace(6, len(freq) - 1 + 6, num=len(freq))
    y_axis = [freq[i] / total for i in range(len(freq))]
    plt.bar(x_axis, y_axis)
    y_axis = [EXPECTED[i] / total_exp for i in range(len(EXPECTED))]
    plt.plot(x_axis, y_axis, 'orange', label="Rozkład normalny")
    plt.title("Empiryczny rozkład ilości iteracji")
    plt.ylabel("Częstotliwość występowania")
    plt.legend(loc="upper right")
    plt.show()


def showBars(freq: list[int]) -> None:
    x_axis = np.linspace(0, len(freq) - 1, num=len(freq))
    plt.hist(freq, bins=len(freq) // 2, weights=np.zeros_like(freq) + 1. / len(freq))
    plt.title("Empiryczny rozkład wartości p")
    plt.xlabel("Wartość")
    plt.ylabel("Częstotliwość występowania")
    plt.show()


def chiCalc(result: list[int], exp_freq: list[int]) -> float:
    chsq = 0
    for i in range(len(exp_freq)):
        tmp = (result[i] - exp_freq[i]) / math.sqrt(exp_freq[i])
        chsq += tmp * tmp
    return chsq
