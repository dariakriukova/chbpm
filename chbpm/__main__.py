import chbpm.bpm as bpm
import argparse
import logging


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
    parser.add_argument(
        "--log", help="Set log level", default="INFO"
    )
    parser.add_argument(
        '--format',
        help='Convert output audio files to given format'
    )


    args = parser.parse_args()

    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log)
    logging.basicConfig(level=numeric_level,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


    bpm.main(
        args.input_path,
        args.output_path,
        args.target_bpm,
        args.range_percentage,
        args.ffmpeg_options,
        args.format
    )


if __name__ == "__main__":
    main()
