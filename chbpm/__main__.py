import sys
import chbpm.bpm as bpm


def main():
    path = sys.argv[1]
    bpm.main(path)

if __name__ == "__main__":
    main()