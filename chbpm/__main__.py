import chbpm.bpm as bpm
import argparse


def main():
    parser = argparse.ArgumentParser(description="Process audio files to adjust BPM.")

    parser.add_argument("input_path", help="Path to the input music folder")
    parser.add_argument(
        "-o", "--output_path", default="adjusted", help="Path to the output folder"
    )
    parser.add_argument(
        "-t",
        "--target_bpm",
        type=int,
        default=180,
        help="Optional target BPM for tempo adjustment",
    )
    parser.add_argument(
        "-r",
        "--range_percentage",
        type=float,
        default=15,
        help="Percentage for BPM range adjustment (default: 15)",
    )
    parser.add_argument(
        "--ffmpeg_options", help="Additional FFmpeg command line options"
    )

    args = parser.parse_args()

    bpm.main(
        args.input_path,
        args.output_path,
        args.target_bpm,
        args.range_percentage,
        args.ffmpeg_options,
    )


if __name__ == "__main__":
    main()
