from collections import Counter
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sc
import random

BINARY_OUTPUT = "random.bin"
LETTERS_PROBE = [37 / 256, 56 / 256, 70 / 256, 56 / 256, 37 / 256]
LETTERS = ['A', 'B', 'C', 'D', 'E']


def countOnes():
    with open(BINARY_OUTPUT, 'rb') as f:
        file_array = []
        [file_array.append(int(i.strip())) for i in f.readlines()]
    numbers = []

    for item in file_array:
        for i in int32_to_int8(item)[::-1]:
            numbers.append(i)
    # print(f'8-bitowych liczb: {len(numbers)}')  # -> 1 024 000 liczb 8-bitowych
    '''numbers = genNumbers(9600000)'''

    bins = []
    letters = []
    counter = 0
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

    # print(f'liter: {len(letters)}')
    expProbs = getExpectedProbs()
    words4, words5 = dict(), dict()
    words4, counts4 = connectLetters(letters, word_length=4)
    words5, counts5 = connectLetters(letters, word_length=5)

    chi4 = chiCalc(words4, counts4, expProbs)
    chi5 = chiCalc(words5, counts5, expProbs)
    print(f"Q5={round(chi5, 2)}, Q4={round(chi4, 2)}\n"
          f"Q5-Q4={round(chi5 - chi4, 2)}")

    showHistogram(counts4, "\n\nRozkład częstotliwości wystąpień wyrazów 4-literowych")
    showHistogram(counts5, "Rozkład częstotliwości wystąpień wyrazów 5-literowych")


def int32_to_int8(n):
    mask = (1 << 8) - 1
    return [(n >> k) & mask for k in range(0, 32, 8)]


def connectLetters(list_of_letters: list, word_length: int):
    words = list()
    for letter in range(0, 256000):
        word = "".join(list_of_letters[letter:letter + word_length])
        words.append(word)
    # print(f'utworzone {word_length}-literowe słowa: {len(words)}')
    unique = Counter(words)
    return list(unique.keys()), list(unique.values())


def genNumbers(count):
    return [random.randrange(255) for _ in range(count)]


def chiCalc(data, count, probs):
    chi = 0
    for k, v in zip(data, count):
        chi += ((v - probs[k]) ** 2) / probs[k]
        # print(f"{k}->({v}-{probs[k]})^2/{probs[k]}=={((v - probs[k]) ** 2) / probs[k]}")
    return chi


def showHistogram(data, title: str):
    density = sc.gaussian_kde(data)
    n, x, _ = plt.hist(data, bins=20,
                       histtype='bar', density=True)
    plt.plot(x, density(x))
    plt.title(title)
    plt.show()


def getExpectedProbs():
    probs = {}
    for word_length in [4, 5]:
        for possible_word in range(5 ** word_length):
            exp_freq = 256000
            word = possible_word
            chars = []
            for _ in range(word_length):
                chars.append(LETTERS[word % 5])
                exp_freq *= LETTERS_PROBE[word % 5]
                word = math.floor(word / 5)
                # print(exp_freq)
            probs[''.join(chars)] = exp_freq
    return probs


if __name__ == "__main__":
    countOnes()
    # getExpectedProbs()
