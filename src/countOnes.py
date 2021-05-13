import math
import random
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sc

BINARY_OUTPUT = "random.bin"
LETTERS_PROBE = [37 / 256, 56 / 256, 70 / 256, 56 / 256, 37 / 256]
LETTERS = ['A','B', 'C', 'D', 'E']


def countOnes() -> None:
    with open(BINARY_OUTPUT, 'rb') as f:
        file_array = []
        [file_array.append(int(i.strip())) for i in f.readlines()]
    numbers = []

    for item in file_array:
        for i in int32_to_int8(item)[::-1]:
            numbers.append(i)
    '''numbers = genNumbers(9600000)'''  # <- generate with random lib

    bins = []
    letters = []
    for item in numbers:
        for bit in np.binary_repr(item, 8):
            bins.append(bit)

    # print(f'bitów: {len(bins)}')
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
    print(f"Q5={round(chi5, 2)}, Q4={round(chi4, 2)}\n"
          f"Q5-Q4={round(chi5 - chi4, 2)}")

    showHistogram(counts4, "\n\nRozkład częstotliwości wystąpień wyrazów 4-literowych", 4)
    showHistogram(counts5, "Rozkład częstotliwości wystąpień wyrazów 5-literowych", 5)


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


def genNumbers(count) -> list[int]:
    return [random.randrange(255) for _ in range(count)]


def chiCalc(data, count, probs) -> int:
    chi = 0
    for k, v in zip(data, count):
        chi += ((v - probs[k]) ** 2) / probs[k]
        # print(f"{k}->({v}-{probs[k]})^2/{probs[k]}=={((v - probs[k]) ** 2) / probs[k]}")
    return chi


def showHistogram(data, title: str, word_length: int) -> None:
    density = sc.gaussian_kde(data)
    div = 15 if word_length == 5 else 17
    n, x, _ = plt.hist(data, bins=len(data)//div,
                       histtype='bar', density=True)
    plt.plot(x, density(x))
    plt.title(title)
    plt.show()


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


if __name__ == "__main__":
    countOnes()
