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


def genNumbers(count: int, bits: int, normalized: bool = False) -> list[int]:
    print(f"Loading data.. ", end="")
    numbers = [random.randrange((2 ** bits) - 1) for _ in range(count)]
    if normalized: numbers = [numbers[j] / 2 ** bits for j in range(len(numbers))]
    print(f"Done.")
    return numbers

def Phi(z):
    tmp = z / math.sqrt(2.)
    tmp = 1 + math.erf(tmp)
    return tmp / 2

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

def entropy(labels, base=None):
    value, counts = np.unique(labels, return_counts=True)
    norm_counts = counts / counts.sum()
    base = 0 if base is None else base
    return -(norm_counts * np.log(norm_counts) / np.log(base)).sum()