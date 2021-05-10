import numpy as np

BINARY_OUTPUT = "binaryout.bin"


def countOnes():
    flile = open(BINARY_OUTPUT, 'r')
    file_array = np.fromfile(flile, dtype=np.uint8)
    bin_values = list()
    letters = list()
    for item in file_array:
        bin_values.append(np.binary_repr(item, 8))

    for i in range(0, 100000):
        counter = 0
        value = bin_values[i]
        for j in range(0, 8):
            if value[j] == '1':
                counter += 1
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


def joinToWord(letters: list, word_length: int):
    words = list()
    for letter in range(0, 20000):
        words.append("".join(letters[letter * word_length:letter * word_length + word_length]))
    return np.unique(words, return_counts=True)
