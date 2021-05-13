import numpy as np
from collections import Counter
import scipy.stats as sc
import matplotlib.pyplot as plt

BINARY_OUTPUT = "random.bin"


def countOnes():
    with open(BINARY_OUTPUT, 'rb') as f:
        file_array = []
        [file_array.append(int(i.strip())) for i in f.readlines()]
    numbers = []
    print("Loaded")
    for item in file_array:
        for i in int32_to_int8(item)[::-1]:
            numbers.append(i)
        # print(f"{item}->{numbers[-4:]}")

    bins = []
    letters = []
    counter = 0
    for item in numbers:
        value = np.binary_repr(item)
        for bit in value:
            bins.append(bit)
    for i in range(0, 4800000):
        counter = 0
        value = bins[i:i + 8]
        for bit in value:
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
    words4, counts4 = connectLetters(letters, word_length=4)
    words5, counts5 = connectLetters(letters, word_length=5)
    stat4, chi4 = sc.chisquare(counts4)
    stat5, chi5 = sc.chisquare(counts5)

    '''for c4, w4 in zip(counts4, words4):
        print(f"{w4}: {c4}")'''
    print(counts4,"\n", words4)
    print("\n\n")
    print(counts5,"\n", words5)
    '''for c5, w5 in zip(counts5, words5):
        print(f"{w5}: {c5}")'''

    y_axis = lambda x: np.ones_like(x) / len(x)
    plt.bar(range(len(counts4)) , counts4)
    plt.show()
    plt.clf()
    plt.bar(range(len(counts5)) , counts5)
    plt.show()

    print(f"Oryg. ChiSquare result= {stat5 - stat4}, Q5= {stat5}, Q4= {stat4}")


def int32_to_int8(n):
    mask = (1 << 8) - 1
    return [(n >> k) & mask for k in range(0, 32, 8)]


def connectLetters(list_of_letters: list, word_length: int):
    words = list()
    print(list_of_letters[0:30])
    for letter in range(0, 1200000):
        word = "".join(list_of_letters[letter * word_length:letter * word_length + word_length])
        words.append(word)
    result = Counter(words)
    return list(result.keys()), list(result.values())


if __name__ == "__main__":
    countOnes()
