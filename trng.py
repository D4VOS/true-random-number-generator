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
# Constants
# =============================================================================


image_path = "./lena.png"
output_path = "./output.txt"
video_path = "./test.mp4"
m = 197
random_numbers_amount = 1000000


# =============================================================================
# Random number generate methods
# =============================================================================

def getSeed(path):
    value = getRandomPixelValue() + 3       # get random pixel's value

    prev_prime = sp.prevprime(value)        # p1
    next_prime = sp.nextprime(value)        # p2

    return [((prev_prime*next_prime) % m), prev_prime, next_prime]


def getRandomPixelValue():
    current_time = time.time() * 1000               # get system_clock
    current_width = int(current_time % frameWidth)
    current_height = int(current_time % frameHeight)

    return frames[((current_width * current_height) % frameCount), current_height, current_width, ((current_width * current_height) % 3)]
    # [frame_no, height, width, [R,G,B]]


def getRandomNumber(prev_x, prev_p1, prev_p2):
    f = getRandomPixelValue() + 3           # get random pixel's value
    current_p1 = sp.prevprime(f)            # previous prime number
    current_p2 = sp.nextprime(f)            # next prime number
    a = current_p1 * current_p2             # incr
    b = ((f * prev_p1 * prev_p2) % m)       # multi
    x = ((prev_x*b+a) % m)                  # next
    return [x, current_p1, current_p2]

# =============================================================================
# Display methods
# =============================================================================


def showHistogram():
    file = open(output_path, "r")
    data = np.loadtxt(file)
    histogram = plt.hist(data, histtype='bar', bins=m, range=[0, m])
    ent = entropy(histogram[0], base=2)
    print("Entropia:", round(ent, 5))
    plt.xlabel('Generated number')
    plt.ylabel('Number of occurrences')
    plt.title('Distribution of generated numbers')
    plt.show()
    file.close()

# =============================================================================
# Worker method
# =============================================================================


def loadVideo(path):
    cap = cv2.VideoCapture(path)
    global frameCount, frameWidth, frameHeight
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    captured_frames = np.empty(
        (frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))
    fc = 0
    ret = True
    while (fc < frameCount and ret):
        ret, captured_frames[fc] = cap.read()
        fc += 1
    cap.release()

    return captured_frames


def worker():
    start = time.time()

    # lena_image = img.open(image_path)       #load image
    # global width, height
    # width, height = lena_image.size  # get width and height
    # global pixs_val
    # pixs_val = np.array(lena_image)         # cast image to array

    global iterIndex
    iterIndex = 0
    global frames
    frames = loadVideo(video_path)
    seed = getSeed(image_path)
    random_number = getRandomNumber(seed[0], seed[1], seed[2])
    print("Worker has been launched..")

    with open(output_path, "a") as text_file:
        while iterIndex <= random_numbers_amount:
            temp = getRandomNumber(
                random_number[0], random_number[1], random_number[2])
            if(temp[0] == random_number[0]):
                continue
            else:
                random_number = temp
                print("{}".format(random_number[0]), file=text_file)
                if(((iterIndex % int(random_numbers_amount/10)) == 0) and (iterIndex != 0)):
                    print(iterIndex, "numbers has been generated.")
                iterIndex += 1

    text_file.close()
    print(random_numbers_amount, "numbers in", round(
        (time.time() - start), 2), "seconds.")
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
                print(f'Creating new one..')
            finally:
                file = open("output.txt", "w")
        if(sys.argv[1] == "--hist"):
            showHistogram()
            return
    worker()


if __name__ == "__main__":
    main()
