from src import *


def main():
    option = sys.argv[1] if len(sys.argv) > 1 else None
    while True:
        if option in ["--new", "--hist", "--test", "--append"]:
            break
        os.system('cls')
        option = input("Missing or invalid parameter. Choose the task:\n"
                       "\t--new <count> to run generator\n"
                       "\t--append to append new n 8-bit numbers to binary file\n"
                       "\t--hist to display histogram from binary file\n"
                       "\t--test to run diehard tests:\n")
    os.system('cls')
    # ---------------------------------------- RUN TASK -------------------------------------------------#
    if option in ["--append", "--new"]:
        try:
            if option == "--new":
                os.remove(RESULT_OUTPUT)
                print("Output file have been removed!")
        except FileNotFoundError:
            print("File doesn't exist! A new one will be created.")
        finally:
            with open(RESULT_OUTPUT, 'ab'):
                pass
        if len(sys.argv) > 2:
            count = sys.argv[2]
        else:
            count = input("How many 8-bit numbers? ")
        append = True if option == "--append" else False
        generateNumbers(count, append)
    elif option == "--hist":
        try:
            data = binaryToArray(RESULT_OUTPUT)
            showHistogramFromGenerator(data)
        except FileNotFoundError:
            print("Any file provided! Generate new one using --new")
    elif option == "--test":
        try:
            runTests()
        except FileNotFoundError:
            print("Any file provided! Generate new one using --new")


if __name__ == '__main__':
    main()
