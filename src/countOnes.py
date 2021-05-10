import numpy as np
import scipy.stats as sc
import matplotlib.pyplot as plt

BINARY_OUTPUT = "binaryout.bin"


def countOnes():
    flile = open(BINARY_OUTPUT, 'r')
    file_array = np.fromfile(flile, dtype=np.uint32)
    bins = list()
    letters = list()
    for item in file_array:
        value = np.binary_repr(item)
        for bit in value:
            bins.append(bit)
    for i in range(0, 2048000):
        counter = 0
        value = bins[i:i+8]
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

    words4, counts4 = joinToWord(letters, 4)
    for word, count in zip(words4, counts4):
        print(f"{word}: {count}")


def joinToWord(letters: list, word_length: int):
    words = list()
    for letter in range(0, 256000):
        words.append("".join(letters[letter * word_length:letter * word_length + word_length]))
    return np.unique(words, return_counts=True)


countOnes()
