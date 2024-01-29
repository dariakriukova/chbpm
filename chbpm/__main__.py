import sys
import chbpm.bpm as bpm
import argparse


def main():
    parser = argparse.ArgumentParser(description="Process audio files to adjust BPM.")
    
    parser.add_argument('input_path', help="Path to the input music folder")
    parser.add_argument('-o', '--output_path', default=None, help="Path to the output folder")
    
    args = parser.parse_args()
    
    if args.output_path is None:
        args.output_path = args.input_path + "_adjusted"
    
    bpm.main(args.input_path, args.output_path)

if __name__ == "__main__":
    main()