import sys
import chbpm.bpm as bpm
import argparse


def main():
    parser = argparse.ArgumentParser(description="Process audio files to adjust BPM.")
    
    parser.add_argument('input_path', help="Path to the input music folder")
    parser.add_argument('-o', '--output_path', default=None, help="Path to the output folder")
    parser.add_argument('-t', '--target_bpm', type=int, default=None, help="Optional target BPM for tempo adjustment")
    parser.add_argument('-r', '--range_percentage', type=float, default=15, help="Percentage for BPM range adjustment (default: 15)")


    
    args = parser.parse_args()
    
    if args.output_path is None:
        args.output_path = args.input_path + "_adjusted"
    
    bpm.main(args.input_path, args.output_path, args.target_bpm, args.range_percentage)

if __name__ == "__main__":
    main()