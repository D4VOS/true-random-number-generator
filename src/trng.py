from essentials import *

# =============================================================================
# * Constants
# =============================================================================
SEED_OUTPUT = "seed_output.txt"
RESULT_OUTPUT = "binaryout.bin"
VIDEO_PATH = "resources/test2.mp4"
NUMBERS_COUNT = 9600000
m = 257  # 8 bits


# =============================================================================
# * Random number generate methods
# =============================================================================
def getSeed(video):
    """Returns seed for generator"""
    value = getRandomPixelValue(video) + 3  # get random pixel's value
    result = {
        "previous_prime": sp.prevprime(value),  # p1
        "next_prime": sp.nextprime(value)  # p2
    }
    result["random_number"] = ((result["previous_prime"] * result["next_prime"]) % m)
    return result


def getRandomPixelValue(video):
    """Returns pixel value based on system clock value"""
    current_time = time.time() * 1000  # get system_clock

    posX = int(current_time % video["width"])
    posY = int(current_time % video["height"])

    no_frame = (posX * posY) % video["count"]

    return video["frames"][no_frame, posY, posX, ((posX * posY) % 3)]  # [frame_no, height, width, [R,G,B]]


def getRandomNumber(generated_number, video):
    """Generate random number using vision source and specific expressions"""
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
def showHistogram(txt_path):
    file = open(txt_path, "r")
    data = np.loadtxt(file)
    fig, ax = plt.subplots()
    if txt_path == SEED_OUTPUT:
        top = 255
        text = "generowanych przez plik wideo"
        bins = 255
    else:
        top = m - 1
        text = "po post-processingu"
        if m > 257:
            bins = m // 100
        else:
            bins = m - 1
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.7)
    histogram = ax.hist(data, histtype='bar', density=True, stacked=True, bins=bins, range=[0, top])
    ent = entropy(data, base=2)
    ax.set_ylim([0, max(histogram[0])])
    ax.set_xlabel("Wartość (x{})".format(get_sub('i')))
    ax.set_ylabel("Częstotliwość występowania (p{})".format(get_sub('i')))
    ax.set_title("Empiryczny rozkład zmiennych losowych {}\n".format(text))
    ax.text(0.12, 0.08, "H(X)={0}\nm={1}".format(round(ent, 5), m), transform=ax.transAxes, fontsize=10, verticalalignment='bottom', bbox=props)
    ax.ticklabel_format(useOffset=False, style='sci')
    plt.gca().set_ylim(0, histogram[0].max() * 1.05)
    plt.gca().set_xlim(0, top - 1)
    plt.show()
    base = os.path.splitext(os.path.basename(txt_path))
    fig.savefig('charts/{0}_m_{1}.png'.format(base[0], m), dpi=fig.dpi)
    file.close()


def save_result(buffer, files):  # todo rework
    """Saving number to binary file"""
    files["binary"].write(str(buffer) + "\n")


# =============================================================================
# * Video handling method
# =============================================================================
def loadVideo(path):
    """Capture vision source to array"""
    captured_video = cv2.VideoCapture(path)  # load video file
    video = {
        "count": int(captured_video.get(cv2.CAP_PROP_FRAME_COUNT)),  # frames count
        "height": int(captured_video.get(cv2.CAP_PROP_FRAME_HEIGHT)),  # frame height
        "width": int(captured_video.get(cv2.CAP_PROP_FRAME_WIDTH))  # frame width
    }
    captured_frames = np.empty((video["count"], video["height"], video["width"], 3), np.dtype("uint8"))

    frameIndex = 0
    flag = True
    while (frameIndex < video["count"]) and flag:
        ret, captured_frames[frameIndex] = captured_video.read()
        frameIndex += 1

    captured_video.release()
    video["frames"] = captured_frames

    return video


def worker():
    """Main worker"""
    start = time.time()  # start time measure

    video = loadVideo(VIDEO_PATH)  # get video params
    generated_number = getSeed(video)  # get first frame as seed

    print("Worker has been launched..")
    generated_number = getRandomNumber(generated_number, video)  # get first random value

    files = {
        "source": open(SEED_OUTPUT, "a"),
        "binary": open(RESULT_OUTPUT, "a")
    }
    index = 0
    buffer = 0x0
    while index < NUMBERS_COUNT:
        temp_generated_number = getRandomNumber(generated_number, video)
        if temp_generated_number["random_number"] == generated_number["random_number"] or temp_generated_number["random_number"] == -1:
            continue
        else:
            generated_number = temp_generated_number
            if index % 4 == 0 and index != 0:  # collect 4 bytes and save as 32-bit value
                buffer = buffer << 8  #
                buffer = buffer ^ generated_number["random_number"]  #
                save_result(0xFFFFFFFF & buffer, files)  #
                buffer = 0x0  #
            else:  #
                buffer = buffer << 8  #
                buffer = buffer ^ generated_number["random_number"]  #

            if ((index % int(NUMBERS_COUNT / 10)) == 0) and (index != 0):
                print(index, "numbers has been generated..")
            index += 1

    for file in files.values():
        file.close()

    end = round((time.time() - start), 2)
    print("Done.", NUMBERS_COUNT, "numbers have been generated in", end, "seconds.")  # finish time measure


# =======================================================================
# * Main --new - clear output files, --hist - only generate histogram
# =======================================================================
def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--new":
            try:
                os.remove(SEED_OUTPUT)
                os.remove(RESULT_OUTPUT)
                print("Outputs files have been removed!")
            except Exception as e:
                print(f"Creating new ones..")
        if sys.argv[1] == "--hist":
            showHistogram(RESULT_OUTPUT)
            showHistogram(SEED_OUTPUT)
            return
    worker()


if __name__ == "__main__":
    main()
