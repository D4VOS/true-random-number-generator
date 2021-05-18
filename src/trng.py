from src.generator import *


def generateNumbers(count, append: bool = False):
    """Generating numbers"""
    print(f"Loading video file ({VIDEO_PATH}).. ")
    mode = "ab" if append else "wb"
    video = Video(VIDEO_PATH)
    print(f"Done.")
    start = time.time()  # start time measure
    trng = Generator(video, RESULT_OUTPUT)
    print(f"Started generating {count} numbers.. ")
    with open(RESULT_OUTPUT, mode) as file:
        for i in range(int(count)):
            saveToBinary(trng.next(), file)
            if (i % (int(count) / 20)) == 0 and i != 0:
                print(f"{i} numbers has been generated in {round((time.time() - start), 2)}s.")

    end = round((time.time() - start), 2)
    print(f"Done. {count} numbers have been generated in {end} seconds.")  # finish time measure
