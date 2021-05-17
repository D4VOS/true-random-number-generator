from essentials import *

NO_TRIALS = 12000
NO_TESTS = 100
UNIMAX = 4294967296.  # unsigned max value of 32-bit
RATIO = 100 / UNIMAX


def init(numbers: list[int], histogram: bool = False):
    sum, ss = 0, 0
    curent_index = 0
    p = []
    successes = []
    print(f"Parking Lot test: ", end="")
    for test in range(0, NO_TESTS):  # 100 testow
        x = [0.] * NO_TRIALS
        y = [0.] * NO_TRIALS

        first = float(numbers[curent_index] * RATIO)
        curent_index += 1
        second = float(numbers[curent_index] * RATIO)
        curent_index += 1
        x[0] = first
        y[0] = second
        no_success = 1

        for attempt in range(0, NO_TRIALS - 1):
            first = float(numbers[curent_index] * RATIO)
            curent_index += 1
            second = float(numbers[curent_index] * RATIO)
            curent_index += 1
            crashed = False
            for i in range(no_success):
                if math.fabs(x[i - 1] - first) <= 1.0 and math.fabs(y[i - 1] - second) <= 1.0:
                    crashed = True
                    break
            if not crashed:
                x[no_success] = first
                y[no_success] = second
                no_success += 1
        sum += no_success
        ss += no_success * no_success
        z_score = (no_success - 3523.0) / 21.9
        p_val = 1 - Phi(z_score)
        p.append(p_val)
        # print(f"No.{test + 1}\t\tNo.parked = {no_success} p_value= {round(p_val, 6)}")
        successes.append(no_success)
    _, pvalue = sc.kstest(p, 'uniform')
    print(f"after 100 tests: p-value={round(pvalue, 6)} ", end="")
    if 0.025 < pvalue < 0.975:
        print("PASSED")
    else:
        print("FAILED")
    if histogram:
        showHistogram(successes, "Empiryczny rozkład ilości udanych parkowań")
        showHistogram(p, "Empiryczny rozkład wartości p")


def showHistogram(freq: list[int], title: str) -> None:
    x_axis = np.linspace(1, len(freq), num=len(freq))
    plt.hist(freq, bins=20, stacked=True, weights=np.zeros_like(freq) + 1. / len(freq))
    plt.title(title)
    plt.xlabel("Wartość")
    plt.ylabel("Częstotliwość występowania")
    plt.show()
