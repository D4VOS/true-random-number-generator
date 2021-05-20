from pylab import *

from src.essentials import *

LETTERS_PROBE = [37 / 256, 56 / 256, 70 / 256, 56 / 256, 37 / 256]
LETTERS = ['A', 'B', 'C', 'D', 'E']

MEAN = 2500
STD = math.sqrt(5000)


def init(numbers: list[int], histogram: bool = False):
    p_vals = []
    counts4, counts5 = 0, 0
    cdf = []
    print(f"\n\nCount-the-1's test: ")
    for test in range(24):
        bits = []
        letters = []

        for item in numbers[test * 64000:test * 64000 + 64000]:  # 64k 32-bit -> 256k 8-bit -> array of 2.048M bits
            for byte in int32_to_int8(item)[::-1]:
                for bit in np.binary_repr(byte, 8):
                    bits.append(bit)

        for i in range(0, 256000 + 5):  # array of 2.048M bits -> 256k letters
            counter = 0
            for bit in bits[i * 8:i * 8 + 8]:
                counter += 1 if bit == '1' else 0
            if counter <= 2:
                letters.append('A')
            elif counter == 3:
                letters.append('B')
            elif counter == 4:
                letters.append('C')
            elif counter == 5:
                letters.append('D')
            elif counter >= 6:
                letters.append('E')

        expected_freq = getExpectedProbs(4) | getExpectedProbs(5)

        words4, counts4 = connectLetters(letters, word_length=4)  # get 4-letters words and occurrences for every unique one
        words5, counts5 = connectLetters(letters, word_length=5)  # get 5-letters words and occurrences for every unique one

        chi4 = chiCalc(words4, counts4, expected_freq)  # sum(obs-exp)**2/exp for 4-letter words
        chi5 = chiCalc(words5, counts5, expected_freq)  # sum(obs-exp)**2/exp for 5-letter words

        chsq = chi5 - chi4
        z = (chsq - MEAN) / STD
        p = 1 - Phi(z)
        print(f"{test + 1}. chisquare={round(chsq, 2)}\tz-score={round(z, 3)}\tp-value={round(p, 6)}")

        p_vals.append(p)
    _, p_value = sc.kstest(p_vals, 'uniform')
    print(f"Result of 24 tests: p-value={round(p_value, 6)} ", end="")
    if 0.025 < p_value < 0.975:
        print("PASSED")
    else:
        print("FAILED")
    if histogram:
        showHistogram(counts4, expected_freq, "Empiryczny rozkład wystąpień wyrazów 4-literowych", 4)
        showHistogram(counts5, expected_freq, "Empiryczny rozkład wystąpień wyrazów 5-literowych", 5)
        showBars(p_vals)
        makeCDF(p_vals)



def makeCDF(x, plot=True, *args, **kwargs):
    x, y = sorted(x), np.arange(len(x)) / len(x)
    ideal_x = [0.5] * len(x)
    ideal_y = np.arange(len(ideal_x)) / len(ideal_x)
    plt.title("Empiryczny CDF p")
    plt.xlabel("Wartość p")
    plt.ylabel("Częstotliwość występowania")
    plt.plot(x, y, *args, **kwargs) if plot else (x, y)
    plt.plot(ideal_x, ideal_y, 'orange') if plot else (ideal_x, ideal_y)
    plt.show()


def getExpectedProbs(word_length) -> dict[str, int]:
    """Calc expected prob for every possible word"""
    expected_freq = {}
    for possible_word in range(5 ** word_length):
        word = possible_word
        chars = []
        freq = 256000
        for _ in range(word_length):
            chars.append(LETTERS[word % 5])
            freq *= LETTERS_PROBE[word % 5]
            word = math.floor(word / 5)
        expected_freq[''.join(chars)] = freq
    return expected_freq


def connectLetters(list_of_letters: list, word_length: int) -> tuple[list[str], list[int]]:
    """Connect letters to n-letter words"""
    words = list()
    for letter in range(0, 256000):
        word = "".join(list_of_letters[letter:letter + word_length])
        words.append(word)
    result = sortDict(Counter(words))
    return list(result.keys()), list(result.values())


def showBars(freq: list[int]) -> None:
    """Display pvals hist"""
    x_axis = np.linspace(0, len(freq) - 1, num=len(freq))
    plt.hist(freq, bins=len(freq) // 2, weights=np.zeros_like(freq) + 1. / len(freq))
    plt.title("Empiryczny rozkład wartości p")
    plt.xlabel("Wartość")
    plt.ylabel("Częstotliwość występowania")
    plt.show()


def sortDict(dictionary):
    res = {}
    for key in sorted(dictionary):
        res[key] = dictionary[key]
    return res


def showHistogram(data, expected, title: str, word_length: int) -> None:
    total = sum(data)
    x_axis = np.linspace(0, len(data) - 1, num=len(data))
    y_axis = [data[i] / total for i in range(len(data))]
    if word_length == 4:
        start = 0
        end = 625
    else:
        start = 625
        end = 3750
    expected_y = []
    for k, v in expected.items():
        expected_y.append(v / total)

    plt.plot(x_axis, expected_y[start:end], 'orange', alpha=0.4)
    plt.plot(x_axis, y_axis)
    plt.title(title)
    plt.xlabel("Wartość")
    plt.ylabel("Częstotliwość występowania")
    plt.show()
