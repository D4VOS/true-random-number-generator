import random

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import *
import math

BINARY_OUTPUT = "random.bin"
NO_STATES = math.factorial(5)


def permTest():
    with open(BINARY_OUTPUT, 'rb') as file:
        numbers = [int(num) for num in file]

    states = []
    for i in range(200000):
        state = [num for num in numbers[i:i + 5]]
        states.append(state)

    unique = set(states)
    print(unique)


permTest()
