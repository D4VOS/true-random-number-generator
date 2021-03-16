import time
import sys
import math
from PIL import Image as img
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# =============================================================================
# Constants
# =============================================================================


image_path = "./lena.png"
output_path = "./output.txt"
m = 197
random_numbers_amount = 10000


# =============================================================================
# Random number generate methods
# =============================================================================


def getRandomPixelValue(image_path):
    lena_image = img.open(image_path)       # load image
    width, height = lena_image.size         # get width and height
    pixs_val = np.array(lena_image)         # cast image to array
    current_width, current_height = int(
        time.time() * 1000 % width), int(time.time() * 1000 % height)
    return pixs_val[current_width, current_height][0]


def getSeed(path):
    value = getRandomPixelValue(path)
    if(value <= 2):                         # p1
        prev_prime = value                  #
    else:                                   #
        prev_prime = sp.prevprime(value)
    next_prime = sp.nextprime(value)        # p2

    return [((prev_prime*next_prime) % m), prev_prime, next_prime]


def getRandomNumber(prev_x, prev_p1, prev_p2):
    f = getRandomPixelValue(image_path)
    if(f <= 2):
        current_p1 = f
    else:
        current_p1 = sp.prevprime(f)
    current_p2 = sp.nextprime(f)
    a = current_p1*current_p2             # incr
    b = (f * prev_p1 * prev_p2) % m       # multi
    x = ((prev_x*b+a) % m)                # next
    return [x, current_p1, current_p2]

# =============================================================================
# Display methods
# =============================================================================


def showHistogram():
    file = open(output_path, "r")
    data = np.loadtxt(file)
    histogram = plt.hist(data, histtype='bar', bins=m, range=[0, m])
    ent = 0
    for i in histogram[0]:
        if(i != 0):
            ent += (-(i/random_numbers_amount) *
                    math.log2(i/random_numbers_amount))
    print("Entropia:", round(ent, 4))
    plt.xlabel('Generated number')
    plt.ylabel('Number of occurrences')
    plt.title('Distribution of generated numbers')
    plt.show()
    file.close()

# =============================================================================
# Worker method
# =============================================================================


def worker():
    seed = getSeed(image_path)
    random_number = getRandomNumber(seed[0], seed[1], seed[2])
    print("Worker has been launched..")
    iterIndex = 0
    with open(output_path, "a") as text_file:
        while iterIndex <= random_numbers_amount:
            temp = getRandomNumber(
                random_number[0], random_number[1], random_number[2])
            if(temp[0] == random_number[0]):
                continue
            else:
                random_number = temp
                print("{}".format(random_number[0]), file=text_file)
                if(((iterIndex % 1000) == 0) and (iterIndex != 0)):
                    print(iterIndex, "numbers has been generated.")
                iterIndex += 1
    text_file.close()
    showHistogram()

# =============================================================================
# Main --new - reset current output.txt file, --hist - only generate histogram
# =============================================================================


def main():
    if(len(sys.argv) > 1):
        if(sys.argv[1] == "--new"):
            try:
                os.remove('output.txt')
                print('Output file has been removed!')
            except Exception as e:
                print(f'File does not exist, creating new one..')
            finally:
                file = open("output.txt", "w")
        if(sys.argv[1] == "--hist"):
            showHistogram()
            return
    worker()


if __name__ == "__main__":
    main()
