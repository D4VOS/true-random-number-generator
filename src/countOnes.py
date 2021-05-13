import numpy as np
from collections import Counter
import scipy.stats as sc
import matplotlib.pyplot as plt
import seaborn as sb

BINARY_OUTPUT = "random.bin"
LETTERS_PROBE = {'A': 37, 'B': 56, 'C': 70, 'D': 56, 'E': 37}

def countOnes():
    with open(BINARY_OUTPUT, 'rb') as f:
        file_array = []
        [file_array.append(int(i.strip())) for i in f.readlines()]
    numbers = []

    for item in file_array:
        for i in int32_to_int8(item)[::-1]:
            numbers.append(i)
    print(len(numbers))  # -> 1 024 000 liczb 8-bitowych

    bins = []
    letters = []
    counter = 0
    for item in numbers:
        for bit in np.binary_repr(item, 8):
            bins.append(bit)

    print(len(bins))
    for i in range(0, 1024000):
        counter = 0
        for bit in bins[i*8:i*8+8]:
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

    print(len(letters))

    words4, counts4 = connectLetters(letters, word_length=4)
    words5, counts5 = connectLetters(letters, word_length=5)
    print(len(words4), len(words4))
    print(len(words5), len(words5))
    stat4, chi4 = sc.chisquare(counts4)
    stat5, chi5 = sc.chisquare(counts5)

    y_axis = lambda x: np.ones_like(x) / len(x)
    showHistogram(counts4, "Rozkład wystąpień wyrazów 4-literowych")
    showHistogram(counts5, "Rozkład wystąpień wyrazów 5-literowych")
    print(chi4, chi5)
    print(f"Oryg. ChiSquare result= {stat5 - stat4}, Q5= {stat5}, Q4= {stat4}")


def int32_to_int8(n):
    mask = (1 << 8) - 1
    return [(n >> k) & mask for k in range(0, 32, 8)]


def connectLetters(list_of_letters: list, word_length: int):
    words = list()
    for letter in range(0, int(1024000/word_length)):
        word = "".join(list_of_letters[letter:letter + word_length])
        words.append(word)
    print(len(words))
    result = Counter(words)
    return list(result.keys()), list(result.values())

def showHistogram(data, title: str):
    sb.set_style("whitegrid")  # Setting style(Optional)
    plt.figure(figsize=(10, 5))  # Specify the size of figure we want(Optional)
    sb.distplot(x=data, bins=20, kde=True, color='teal',
                kde_kws=dict(linewidth=2, color='black'))
    plt.title(title)
    plt.xlim()
    #plt.bar(range(len(data)), data)
    plt.show()
    y_axis = lambda x: np.ones_like(x) / len(x)

if __name__ == "__main__":
    countOnes()
