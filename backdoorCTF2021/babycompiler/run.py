from sample import *
import sys

def main():
    a = Sample.from_file(sys.argv[1])

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main()

