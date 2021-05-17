from src.essentials import *

LETTERS_PROBE = [37 / 256, 56 / 256, 70 / 256, 56 / 256, 37 / 256]
LETTERS = ['A', 'B', 'C', 'D', 'E']
MEAN = 2500
STD = math.sqrt(5000)


def init(numbers: list[int], histogram: bool = False) -> float:
    p_vals = []
    print(f"Count-the-1's test: ", end="")
    for test in range(24):
        bins = []
        letters = []

        for item in numbers[test * 64000:test * 64000 + 64000]:
            for byte in int32_to_int8(item):
                for bit in np.binary_repr(byte, 8):
                    bins.append(bit)

        for i in range(0, 256000 + 5):
            counter = 0
            for bit in bins[i * 8:i * 8 + 8]:
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
        words4, counts4 = connectLetters(letters, word_length=4)
        words5, counts5 = connectLetters(letters, word_length=5)

        chi4 = chiCalc(words4, counts4, expected_freq)
        chi5 = chiCalc(words5, counts5, expected_freq)

        chsq = chi5 - chi4
        z = (chsq - MEAN) / STD
        p = 1 - Phi(z)
        # print(f"chisquare={round(chsq, 2)}\tz-score={round(z, 3)}\tp-value={round(p, 6)}")

        p_vals.append(p)
    _, p_value = sc.kstest(p_vals, 'uniform')
    print(f"p-value={round(p_value, 6)} ", end="")
    if 0.025 < p_value < 0.975:
        print("PASSED")
    else:
        print("FAILED")
    if histogram:
        showHistogram(counts4, "Empiryczny rozkład wystąpień wyrazów 4-literowych", 4)
        showHistogram(counts5, "Empiryczny rozkład wystąpień wyrazów 5-literowych", 5)
        showBars(p_vals)


def int32_to_int8(n) -> list[int]:
    mask = (1 << 8) - 1
    return [(n >> k) & mask for k in range(0, 32, 8)]


def connectLetters(list_of_letters: list, word_length: int) -> tuple[list[str], list[int]]:
    words = list()
    for letter in range(0, 256000):
        word = "".join(list_of_letters[letter:letter + word_length])
        words.append(word)
    # print(f'utworzone {word_length}-literowe słowa: {len(words)}')
    result = Counter(words)
    return list(result.keys()), list(result.values())


def showBars(freq: list[int]) -> None:
    x_axis = np.linspace(0, len(freq) - 1, num=len(freq))
    plt.hist(freq, weights=np.zeros_like(freq) + 1. / len(freq))
    plt.title("Empiryczny rozkład wartości p")
    plt.xlabel("Wartość")
    plt.ylabel("Częstotliwość występowania")
    plt.show()


def chiCalc(data, count, probs) -> int:
    chi = 0
    for k, v in zip(data, count):
        chi += ((v - probs[k]) ** 2) / probs[k]
    return chi


def showHistogram(data, title: str, word_length: int) -> None:
    density = sc.gaussian_kde(data)
    div = 15 if word_length == 5 else 17
    n, x, _ = plt.hist(data, bins=len(data) // div,
                       histtype='bar', density=True)
    plt.plot(x, density(x))
    plt.title(title)
    plt.xlabel("Wartość")
    plt.ylabel("Częstotliwość występowania")
    plt.show()


def updateTotalCounts(t4, c4, t5, c5):
    for i in range(len(c4)):
        t4[i] += c4[i]
    for i in range(len(c5)):
        t5[i] += c5[i]
    return t4, t5


def getExpectedProbs() -> dict[str, int]:
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
                # print(freq)
            expected_freq[''.join(chars)] = freq
    return expected_freq
