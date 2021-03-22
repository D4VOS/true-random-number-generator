import time
import sys
import math
import cv2  # pip install opencv-python
from PIL import Image as img  # pip install Pillow
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.stats import entropy
from sympy.core.evalf import do_integral

# =============================================================================
# * Constants
# =============================================================================

image_path = "resources/lena.png"
output_path = "output.txt"
video_path = "resources/test.mp4"
m = 251
random_numbers_amount = 1000000

# =============================================================================
# * Random number generate methods
# =============================================================================


def getSeed(source, framesCount, frameWidth, frameHeight):
    value = getRandomPixelValue(source, framesCount, frameWidth, frameHeight) + 3  # get random pixel's value

    prev_prime = sp.prevprime(value)  # p1
    next_prime = sp.nextprime(value)  # p2

    return ((prev_prime * next_prime) % m), prev_prime, next_prime


def getRandomPixelValue(source, framesCount, frameWidth, frameHeight):
    current_time = time.time() * 1000  # get system_clock
    current_width = int(current_time % frameWidth)
    current_height = int(current_time % frameHeight)

    return source[((current_width * current_height) % framesCount), current_height, current_width, ((current_width * current_height) % 3)]
    # [frame_no, height, width, [R,G,B]]


def getRandomNumber(prev_x, prev_p1, prev_p2, source, framesCount, frameWidth, frameHeight):
    f = getRandomPixelValue(source, framesCount, frameWidth, frameHeight) + 3  # get random pixel's value
    current_p1 = sp.prevprime(f)  # previous prime number
    current_p2 = sp.nextprime(f)  # next prime number
    a = (current_p1 * current_p2)  # incr
    b = ((f * prev_p1 * prev_p2) % m)  # ! multi ? % m
    x = (prev_x * b + a) % m  # next
    return x, current_p1, current_p2


# =============================================================================
# * Display methods
# =============================================================================


def showHistogram():
    file = open(output_path, "r")
    data = np.loadtxt(file)
    histogram = plt.hist(data, histtype="bar", bins=m, range=[0, m])
    ent = entropy(histogram[0], base=2)

    print("Entropia:", round(ent, 5))
    plt.xlabel("Generated number")
    plt.ylabel("Number of occurrences")
    plt.title("Distribution of generated numbers")
    plt.show()
    file.close()


# =============================================================================
# * Video handling method
# =============================================================================


def loadVideo(path):
    cap = cv2.VideoCapture(path)
    framesCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    captured_frames = np.empty((framesCount, frameHeight, frameWidth, 3), np.dtype("uint8"))
    fc = 0
    ret = True
    while fc < framesCount and ret:
        ret, captured_frames[fc] = cap.read()
        fc += 1
    cap.release()

    return captured_frames, framesCount, frameWidth, frameHeight


def worker():
    start = time.time()  # start time measure

    frames, framesCount, frameWidth, frameHeight = loadVideo(video_path)
    seed, current_p1, current_p2 = getSeed(frames, framesCount, frameWidth, frameHeight)
    random_number, current_p1, current_p2 = getRandomNumber(seed, current_p1, current_p2, frames, framesCount, frameWidth, frameHeight)

    print("Worker has been launched..")

    iterIndex = 0
    with open(output_path, "a") as text_file:
        while iterIndex <= random_numbers_amount:
            temp_number, temp_p1, temp_p2 = getRandomNumber(random_number, current_p1, current_p2, frames, framesCount, frameWidth, frameHeight)
            if temp_number == random_number:
                continue
            else:
                random_number, current_p1, current_p2 = temp_number, temp_p1, temp_p2
                print("{}".format(random_number), file=text_file)
                if ((iterIndex % int(random_numbers_amount / 10)) == 0) and (iterIndex != 0):
                    print(iterIndex, "numbers has been generated..")
                iterIndex += 1

    text_file.close()

    print("Done.", random_numbers_amount, "numbers have been generated in", round((time.time() - start), 2), "seconds.")  # finish time measure
    showHistogram()


# =============================================================================
# * Main --new - reset current output.txt file, --hist - only generate histogram
# =============================================================================

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--new":
            try:
                os.remove("output.txt")
                print("Output file has been removed!")
            except Exception as e:
                print(f"Creating new one..")
            finally:
                file = open("output.txt", "w")
        if sys.argv[1] == "--hist":
            showHistogram()
            return
    worker()


if __name__ == "__main__":
    main()
