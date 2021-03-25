import time
import sys
from types import ClassMethodDescriptorType
import cv2  # pip install opencv-python
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.stats import entropy

# =============================================================================
# * Constants
# =============================================================================

SEED_OUTPUT = "seed_output.txt"
RESULT_OUTPUT = "output.txt"
VIDEO_PATH = "resources/test2.mp4"
NUMBERS_COUNT = 1000000

m = 257         # 8 bits
# m = 4294967295  # 32 bits :Sadge:
m = 65535       # 16 bits

# =============================================================================
# * Random number generate methods
# =============================================================================


def getSeed(video):
    value = getRandomPixelValue(video) + 3          # get random pixel's value
    result = {
        "previous_prime": sp.prevprime(value),      # p1
        "next_prime": sp.nextprime(value)           # p2
    }
    result["random_number"] = ((result["previous_prime"] * result["next_prime"]) % m)
    return result


def getRandomPixelValue(video):
    current_time = time.time() * 1000  # get system_clock

    rand_x = int(current_time % video["width"])
    rand_y = int(current_time % video["height"])

    return video["frames"][((rand_x * rand_y) % video["count"]), rand_y, rand_x, ((rand_x * rand_y) % 3)]  # [frame_no, height, width, [R,G,B]]


def getRandomNumber(generated_number, video):
    f = getRandomPixelValue(video) + 3  # get random pixel's value

    result = {
        "previous_prime": sp.prevprime(f),   # previous prime number
        "next_prime": sp.nextprime(f),       # next prime number
        "seed_value": f
    }

    a = (result["previous_prime"] * result["next_prime"])               # incr
    b = ((f * generated_number["previous_prime"] * generated_number["next_prime"]) % m)     # multi
    x = (generated_number["random_number"] * b + a) % m                                     # next

    result["random_number"] = (x-1)

    return result


# =============================================================================
# * Display methods
# =============================================================================


def showHistogram(txt_path):
    file = open(txt_path, "r")
    data = np.loadtxt(file)
    fig, ax = plt.subplots()
    if(txt_path == SEED_OUTPUT):
        top = 255
    else:
        top = m
    if(m < 1000):
        ymax = 4500
    else:
        ymax = 65
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.7)
    histogram = ax.hist(data, histtype='bar', bins=top, range=[0, top])
    ent = entropy(histogram[0], base=2)
    #ax.set_ylim(0, auto=True)
    #ax.set_ylim(0, y.max()*1.1)
    ax.set_xlabel("Generated number")
    ax.set_ylabel("Number of occurrences")
    ax.set_title("Distribution of {:,} generated numbers".format(NUMBERS_COUNT))
    ax.text(0.12, 0.08, "H(X)={0}\nm={1}".format(round(ent, 5), m), transform=ax.transAxes, fontsize=10, verticalalignment='bottom', bbox=props)

    plt.autoscale(enable=True, axis='y')
    plt.show()
    if(txt_path == SEED_OUTPUT):
        fig.savefig('charts/src_m_{}.png'.format(m), dpi=fig.dpi)
    else:
        fig.savefig('charts/m_{}.png'.format(m), dpi=fig.dpi)
    file.close()


def save_result(number, files):
    print(number["random_number"], file=files["result"])
    print(number["seed_value"], file=files["source"])

# =============================================================================
# * Video handling method
# =============================================================================


def loadVideo(path):

    captured_video = cv2.VideoCapture(path)    # load video file
    video = {
        "count": int(captured_video.get(cv2.CAP_PROP_FRAME_COUNT)),        # frames count
        "height": int(captured_video.get(cv2.CAP_PROP_FRAME_HEIGHT)),      # frame height
        "width": int(captured_video.get(cv2.CAP_PROP_FRAME_WIDTH))         # frame width
    }
    captured_frames = np.empty((video["count"], video["height"], video["width"], 3), np.dtype("uint8"))

    frameIndex = 0
    flag = True
    while ((frameIndex < video["count"]) and flag):
        ret, captured_frames[frameIndex] = captured_video.read()
        frameIndex += 1

    captured_video.release()
    video["frames"] = captured_frames

    return video


def worker():
    start = time.time()     # start time measure

    video = loadVideo(VIDEO_PATH)           # get video params
    generated_number = getSeed(video)       # get first frame as seed

    print("Worker has been launched..")
    generated_number = getRandomNumber(generated_number, video)     # get first random value

    index = 0

    files = {
        "result": open(RESULT_OUTPUT, "a"),
        "source": open(SEED_OUTPUT, "a")
    }

    while (index <= NUMBERS_COUNT):
        temp_generated_number = getRandomNumber(generated_number, video)
        if (temp_generated_number["random_number"] == generated_number["random_number"] or temp_generated_number["random_number"] == -1):
            continue
        else:
            generated_number = temp_generated_number
            save_result(generated_number, files)
            if ((index % int(NUMBERS_COUNT / 10)) == 0) and (index != 0):
                print(index, "numbers has been generated..")
            index += 1

    for file in files.values():
        file.close()

    end = round((time.time() - start), 2)
    print("Done.", NUMBERS_COUNT, "numbers have been generated in", end, "seconds.")  # finish time measure

    showHistogram(RESULT_OUTPUT)
    showHistogram(SEED_OUTPUT)


# =============================================================================
# * Main --new - reset current output.txt file, --hist - only generate histogram
# =============================================================================

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--new":
            try:
                os.remove(SEED_OUTPUT)
                os.remove(RESULT_OUTPUT)
                print("Outputs files have been removed!")
            except Exception as e:
                print(f"Creating new ones..")
            finally:
                file = open(RESULT_OUTPUT, "w")
                file = open(SEED_OUTPUT, "w")
        if sys.argv[1] == "--hist":
            showHistogram(RESULT_OUTPUT)
            showHistogram(SEED_OUTPUT)
            return
    worker()


if __name__ == "__main__":
    main()
