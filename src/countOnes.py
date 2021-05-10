import numpy as np
import scipy.stats as sc
import matplotlib.pyplot as plt

BINARY_OUTPUT = "random.bin"


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

    Q4, counts4 = chiCalc(4, letters)
    Q5, counts5 = chiCalc(5, letters)
    stat4, chi4 = sc.chisquare(counts4)
    stat5, chi5 = sc.chisquare(counts5)
    print(stat4, chi4, stat5, chi5)
    print(f"ChiSquare result= {Q5 - Q4}, Q5= {Q5}, Q4= {Q4}")
    print(f"Oryg. ChiSquare result= {stat5 - stat4}, Q5= {stat5}, Q4= {stat4}")


def joinToWord(letters: list, word_length: int):
    words = list()
    for letter in range(0, 256000):
        words.append("".join(letters[letter * word_length:letter * word_length + word_length]))
    return np.unique(words, return_counts=True)


def chiCalc(word_length: int, letters: list):
    _, counts = joinToWord(letters, word_length)
    expected = 256000 / word_length ** 5
    result = 0
    for val in counts:
        result += ((val - expected) ** 2) / expected
    return result, counts


if __name__ == "__main__":
    countOnes()
