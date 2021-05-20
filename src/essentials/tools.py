import random
import os
import sys
import time
import cv2  # pip install opencv-python
import random
import math
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from scipy import stats as sc
import sympy as sp
import gc
import struct
from itertools import compress

# ----------------------------------------------- CONSTANTS -------------------------------------------------#
RESULT_OUTPUT = "binaryout.bin"
VIDEO_PATH = "resources/seed.mp4"
GOLDEN_RATIO = 1.61803398875
PI = 3.14159265359
M = 257


# ----------------------------------------------- FILE HANDLING -------------------------------------------------#
def saveToBinary(buffer, file):
    """Saving number to binary file"""
    file.write(struct.pack('B', buffer))


def binaryToArray(path, flag32bit: bool = False):
    """Loading binary file to array"""
    vals = []
    print(f"Started loading file.. ")
    mode = 'I' if flag32bit else 'B'
    div = 4 if flag32bit else 1
    bytes = 4 if flag32bit else 1
    with open(path, 'rb') as f:
        file_size = os.path.getsize(path)
        for i in range(file_size // div):
            vals.append(int(str(struct.unpack(mode, f.read(bytes))).strip('(,)')))  # same format as above
    print(f"Done.")
    return vals


def int32_to_int8(n) -> list[int]:
    mask = (1 << 8) - 1
    return [(n >> k) & mask for k in range(0, 32, 8)]


# ----------------------------------------------- MATH -------------------------------------------------#
def prime_dict():
    arr = primes(264)
    prime_dict = {}
    for value in range(3, 259):
        for i in range(len(arr)):
            if arr[i] == value:
                prime_dict[value] = [arr[i - 1], arr[i + 1]]
                break
            elif arr[i] > value:
                prime_dict[value] = [arr[i - 1], arr[i]]
                break
    return prime_dict


def Phi(z):
    tmp = z / math.sqrt(2.)
    tmp = 1 + math.erf(tmp)
    return tmp / 2


def chiCalc(data, count, probs) -> int:
    chi = 0
    for k, v in zip(data, count):
        print(v,"->",probs[k])
        chi += ((v - probs[k]) ** 2) / probs[k]
    return chi


def entropy(labels, base=None):
    value, counts = np.unique(labels, return_counts=True)
    norm_counts = counts / counts.sum()
    base = 0 if base is None else base
    return -(norm_counts * np.log(norm_counts) / np.log(base)).sum()


def primes(n):
    """ Input n>=6, Returns a list of primes, 2 <= p < n """
    n, correction = n - n % 6 + 6, 2 - (n % 6 > 1)
    sieve = [True] * (n // 3)
    for i in range(1, int(n ** 0.5) // 3 + 1):
        if sieve[i]:
            k = 3 * i + 1 | 1
            sieve[k * k // 3::2 * k] = [False] * ((n // 6 - k * k // 6 - 1) // k + 1)
            sieve[k * (k - 2 * (i & 1) + 4) // 3::2 * k] = [False] * (
                        (n // 6 - k * (k - 2 * (i & 1) + 4) // 6 - 1) // k + 1)
    return [2, 3] + [3 * i + 1 | 1 for i in range(1, n // 3 - correction) if sieve[i]]


# ----------------------------------------- GENERATOR FROM RANDOM LIB -------------------------------------------------#
def genNumbers(count: int, bits: int, normalized: bool = False) -> list[int]:
    print(f"Loading data.. ", end="")
    numbers = [random.randrange((2 ** bits) - 1) for _ in range(count)]
    if normalized: numbers = [numbers[j] / 2 ** bits for j in range(len(numbers))]
    print(f"Done.")
    return numbers


def genFakeNumbers(count: int, bits: int, normalized: bool = False) -> list[int]:
    print(f"Loading data.. ", end="")
    numbers = [i % 10000 for i in range(count)]
    if normalized: numbers = [numbers[j] / 2 ** bits for j in range(len(numbers))]
    print(f"Done.")
    return numbers


# ----------------------------------------------- FORMAT & DISPLAY -------------------------------------------------#
# function to convert to subscript
# from https://www.geeksforgeeks.org/how-to-print-superscript-and-subscript-in-python/
def get_sub(x):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    sub_s = "ₐ₈CDₑբGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥwₓᵧZₐ♭꜀ᑯₑբ₉ₕᵢⱼₖₗₘₙₒₚ૧ᵣₛₜᵤᵥwₓᵧ₂₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"
    res = x.maketrans(''.join(normal), ''.join(sub_s))
    return x.translate(res)


def xstr(s):  # 'None' as string
    if s is None:
        return ''
    return str(s)


def showHistogramFromGenerator(data):
    print(f"Started generating histogram.. ", end="")
    fig, ax = plt.subplots()
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.7)
    histogram = ax.hist(data, histtype='bar', density=True, stacked=True, bins=M - 1, range=[0, M - 1])
    ent = entropy(data, base=2)
    ax.set_ylim([0, max(histogram[0])])
    ax.set_xlabel("Wartość (x{})".format(get_sub('i')))
    ax.set_ylabel("Częstotliwość występowania (p{})".format(get_sub('i')))
    ax.set_title("Empiryczny rozkład zmiennych losowych {}\n".format('po post-processingu'))
    ax.text(0.12, 0.08, "H(X)={0}\nM={1}".format(round(ent, 5), M), transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', bbox=props)
    ax.ticklabel_format(useOffset=False, style='sci')
    plt.gca().set_ylim(0, histogram[0].max() * 1.05)
    plt.gca().set_xlim(0, (M - 1) - 1)
    plt.show()
    print(f"Done.")
