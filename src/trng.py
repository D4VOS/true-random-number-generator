import time
import sys
import os
from types import ClassMethodDescriptorType
import cv2  # pip install opencv-python
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import pickle

# =============================================================================
# * Constants
# =============================================================================

SEED_OUTPUT = "seed_output.txt"
RESULT_OUTPUT = "output.txt"
BINARY_OUTPUT = "binaryout.bin"
VIDEO_PATH = "resources/test2.mp4"
NUMBERS_COUNT = 9600000

m = 257  # 8 bits
# m = 4294967295  # 32 bits :Sadge:
# m = 65537       # 16 bits

# =============================================================================
# * Random number generate methods
# =============================================================================


def getSeed(video):
    value = getRandomPixelValue(video) + 3  # get random pixel's value
    result = {
        "previous_prime": sp.prevprime(value),  # p1
        "next_prime": sp.nextprime(value)  # p2
    }
    result["random_number"] = ((result["previous_prime"] * result["next_prime"]) % m)
    return result


def getRandomPixelValue(video):
    current_time = time.time() * 1000  # get system_clock

    rand_x = int(current_time % video["width"])
    rand_y = int(current_time % video["height"])

    # return video["frames"][((rand_x * rand_y) % video["count"]), rand_y, rand_x, ((rand_x * rand_y) % 3)]  # [frame_no, height, width, [R,G,B]]
    return video["frames"][((rand_x * rand_y) % video["count"]), rand_y, rand_x, ((rand_x * rand_y) % 3)]  # [frame_no, height, width, [R,G,B]]


def getRandomNumber(generated_number, video):
    f = getRandomPixelValue(video) + 3  # get random pixel's value

    result = {
        "previous_prime": sp.prevprime(f),  # previous prime number
        "next_prime": sp.nextprime(f),  # next prime number
        "seed_value": f
    }

    a = (result["previous_prime"] * result["next_prime"])  # incr
    b = ((f * generated_number["previous_prime"] * generated_number["next_prime"]) % m)  # multi
    x = (generated_number["random_number"] * b + a) % m  # next

    result["random_number"] = (x - 1)

    return result


# =============================================================================
# * Display methods
# =============================================================================

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


def showHistogram(txt_path):
    file = open(txt_path, "r")
    data = np.loadtxt(file)
    fig, ax = plt.subplots()
    if (txt_path == SEED_OUTPUT):
        top = 255
        tekst = "generowanych przez plik wideo"
        bins = 255
    else:
        top = m - 1
        tekst = "po post-processingu"
        if (m > 257):
            bins = m // 100
        else:
            bins = m - 1
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.7)
    histogram = ax.hist(data, histtype='bar', density=True, stacked=True, bins=bins, range=[0, top])
    ent = entropy(data, base=2)
    ax.set_ylim([0, max(histogram[0])])
    ax.set_xlabel("Wartość (x{})".format(get_sub('i')))
    ax.set_ylabel("Częstotliwość występowania (p{})".format(get_sub('i')))
    ax.set_title("Empiryczny rozkład zmiennych losowych {}\n".format(tekst))
    ax.text(0.12, 0.08, "H(X)={0}\nm={1}".format(round(ent, 5), m), transform=ax.transAxes, fontsize=10, verticalalignment='bottom', bbox=props)
    ax.ticklabel_format(useOffset=False, style='sci')
    plt.gca().set_ylim(0, histogram[0].max() * 1.05)
    plt.gca().set_xlim(0, top - 1)
    plt.show()
    base = os.path.splitext(os.path.basename(txt_path))
    fig.savefig('charts/{0}_m_{1}.png'.format(base[0], m), dpi=fig.dpi)
    file.close()


def save_result(number, files):
    print(number["random_number"], file=files["result"])
    print(number["seed_value"], file=files["source"])
    byte_arr = [number["random_number"]]
    binary_format = bytearray(byte_arr)
    files["binary"].write(binary_format)


# =============================================================================
# * Video handling method
# =============================================================================
def loadVideo(path):
    captured_video = cv2.VideoCapture(path)  # load video file
    video = {
        "count": int(captured_video.get(cv2.CAP_PROP_FRAME_COUNT)),  # frames count
        "height": int(captured_video.get(cv2.CAP_PROP_FRAME_HEIGHT)),  # frame height
        "width": int(captured_video.get(cv2.CAP_PROP_FRAME_WIDTH))  # frame width
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
    start = time.time()  # start time measure

    video = loadVideo(VIDEO_PATH)  # get video params
    generated_number = getSeed(video)  # get first frame as seed

    print("Worker has been launched..")
    generated_number = getRandomNumber(generated_number, video)  # get first random value

    index = 0

    files = {
        "result": open(RESULT_OUTPUT, "a"),
        "source": open(SEED_OUTPUT, "a"),
        "binary": open(BINARY_OUTPUT, "a+b")
    }

    while (index < NUMBERS_COUNT):
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
                os.remove(BINARY_OUTPUT)
                print("Outputs files have been removed!")
            except Exception as e:
                print(f"Creating new ones..")
            finally:
                file = open(RESULT_OUTPUT, "w")
                file = open(SEED_OUTPUT, "w")
                file = open(BINARY_OUTPUT, "a+b")
        if sys.argv[1] == "--hist":
            showHistogram(RESULT_OUTPUT)
            showHistogram(SEED_OUTPUT)
            return
    worker()


if __name__ == "__main__":
    main()
