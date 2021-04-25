import struct
import binascii
from typing import Collection
from matplotlib.pyplot import hist
import numpy
import sys
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp

BINARY_OUTPUT = "binaryout.bin"


def parking_test():

    total_colsions = []
    total_no_colisions = []
    with open(BINARY_OUTPUT, 'rb') as f:
        for i in range(0, 100):
            parking = numpy.zeros((100, 100))
            numbers_count = 0
            colisions, no_colisions = 0, 0
            while True:
                x = f.read(4)
                if sys.getsizeof(x) < 37:
                    print(f"Iteracja {i}. Kolizje:{colisions}, BRak kolizji: {no_colisions}")
                    print(i, numbers_count)
                    total_no_colisions.append((no_colisions-3523)/(21.9))  # ((100−3523)/21.9)
                    total_colsions.append(colisions)
                    break

                y = f.read(4)
                if sys.getsizeof(y) < 37:
                    print(f"Iteracja {i}. Kolizje:{colisions}, BRak kolizji: {no_colisions}")
                    print(i, numbers_count)
                    total_no_colisions.append((no_colisions-3523)/(21.9))
                    total_colsions.append(colisions)
                    break
                # print(f"Liczba kolizji {colisions}", sys.getsizeof(x))
                if numbers_count == 12000:
                    print(f"Iteracja {i}. Kolizje:{colisions}, BRak kolizji: {no_colisions}")
                    total_no_colisions.append((no_colisions-3523)/(21.9))
                    total_colsions.append(colisions)
                    break
                (x,) = struct.unpack('I', x)
                numbers_count += 1
                x = int(x/42949672.95)

                (y,) = struct.unpack('I', y)
                numbers_count += 1
                y = int(y/42949672.95)
                if parking[x][y] != 1:
                    parking[x][y] = 1
                    no_colisions += 1
                else:
                    colisions += 1
        print(numpy.mean(total_no_colisions))
        plt.hist(total_no_colisions, histtype='bar', density=True, stacked=True, bins=10, range=[min(total_no_colisions), max(total_no_colisions)])
        plt.show()


def test2():
    parking = numpy.zeros((100, 100))
    numbers_count = 0
    colisions, no_colisions = 0, 0
    previous_number = None
    with open(BINARY_OUTPUT, 'rb') as f:
        while True:
            number = f.read(4)
            if sys.getsizeof(number) < 37:
                return print(f"Liczba kolizji {numbers_count/2}/{colisions}, ostatni rozmiar {sys.getsizeof(number)}, suma: {parking.sum()} brak kolizji: {no_colisions}")

            (number,) = struct.unpack('I', number)
            numbers_count += 1
            number = number % 100
            if previous_number is None:
                previous_number = number
                continue

            if parking[previous_number][number] != 1:
                parking[previous_number][number] = 1
                no_colisions += 1
            else:
                colisions += 1
            previous_number = number


def test3():
    parking = numpy.zeros(10000)
    numbers_count = 0
    colisions, no_colisions = 0, 0
    with open(BINARY_OUTPUT, 'rb') as f:
        while True:
            x = f.read(4)
            if sys.getsizeof(x) < 37:
                return print(f"Liczba kolizji {numbers_count/2}/{colisions}, ostatni rozmiar {sys.getsizeof(x)}, suma: {parking.sum()} brak kolizji: {no_colisions}")

            # print(f"Liczba kolizji {colisions}", sys.getsizeof(x))

            (x,) = struct.unpack('I', x)
            numbers_count += 1
            x = int(x/429496.7295)

            if parking[x] != 1:
                parking[x] = 1
                no_colisions += 1
            else:
                colisions += 1


parking_test()
