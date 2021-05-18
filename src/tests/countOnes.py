from src.essentials import *

LETTERS_PROBE = [37 / 256, 56 / 256, 70 / 256, 56 / 256, 37 / 256]
LETTERS = ['A', 'B', 'C', 'D', 'E']

MEAN = 2500
STD = math.sqrt(5000)


def init(numbers: list[int], histogram: bool = False):
    p_vals = []
    counts4, counts5 = 0, 0
    print(f"Count-the-1's test: ", end="")
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
        expected_freq = getExpectedProbs()

        words4, counts4 = connectLetters(letters, word_length=4)    # get 4-letters words and occurrences for every unique one
        words5, counts5 = connectLetters(letters, word_length=5)    # get 5-letters words and occurrences for every unique one

        chi4 = chiCalc(words4, counts4, expected_freq)  # sum(obs-exp)**2/exp for 4-letter words
        chi5 = chiCalc(words5, counts5, expected_freq)  # sum(obs-exp)**2/exp for 5-letter words

        chsq = chi5 - chi4
        z = (chsq - MEAN) / STD
        p = 1 - Phi(z)
        # print(f"chisquare={round(chsq, 2)}\tz-score={round(z, 3)}\tp-value={round(p, 6)}")

        p_vals.append(p)
    _, p_value = sc.kstest(p_vals, 'uniform')
    print(f"after 24 tests: p-value={round(p_value, 6)} ", end="")
    if 0.025 < p_value < 0.975:
        print("PASSED")
    else:
        print("FAILED")
    if histogram:
        showHistogram(counts4, "Empiryczny rozkład wystąpień wyrazów 4-literowych", 4)
        showHistogram(counts5, "Empiryczny rozkład wystąpień wyrazów 5-literowych", 5)
        showBars(p_vals)


def getExpectedProbs() -> dict[str, int]:
    """Calc expected prob for every possible word"""
    expected_freq = {}
    for word_length in [4, 5]:
        for possible_word in range(5 ** word_length):
            freq = 256000
            word = possible_word
            chars = []
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
    result = Counter(words)
    return list(result.keys()), list(result.values())


def showBars(freq: list[int]) -> None:
    """Display pvals hist"""
    x_axis = np.linspace(0, len(freq) - 1, num=len(freq))
    plt.hist(freq, bins=len(freq) // 2, weights=np.zeros_like(freq) + 1. / len(freq))
    plt.title("Empiryczny rozkład wartości p")
    plt.xlabel("Wartość")
    plt.ylabel("Częstotliwość występowania")
    plt.show()


def showHistogram(data, title: str, word_length: int) -> None:
    total = sum(data)
    x_axis = np.linspace(0, len(data) - 1, num=len(data))
    y_axis = [data[i] / total for i in range(len(data))]
    plt.plot(x_axis, y_axis)
    plt.title(title)
    plt.xlabel("Wartość")
    plt.ylabel("Częstotliwość występowania")
    plt.show()
