import librosa
import audioread
import os
import subprocess
import traceback
import warnings
import logging

warnings.filterwarnings("ignore", category=FutureWarning, module="librosa.core.audio")
warnings.filterwarnings("ignore")


def analyze_bpm(file_path, target_bpm):
    try:
        y, sr = librosa.load(file_path, sr=None, mono=True)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr, start_bpm=target_bpm)
        logging.info(f"Analyzed BPM for '{file_path}' - BPM: {tempo}")
        return tempo
    except audioread.NoBackendError:
        logging.warning(f"Failed to analyze BPM for '{file_path}'")
        return None


def adjust_tempo_ffmpeg(input_file, output_file, format, tempo_factor, ffmpeg_options):
    command = [
        "ffmpeg",
        "-loglevel",
        "error",
        "-i",
        input_file,
        "-filter:a",
        f"atempo={tempo_factor}",
        "-map_metadata",
        "0",
        "-y",
    ]

    if format.lower() in {"mp3", "mp4", "m4a", "aac", "flac", "mkv"}:
        command.extend(["-map", "0", '-c:v', 'copy'])
    else:
        command.extend(["-map", "0:a"])  #  keep only audio (drop images)

    if ffmpeg_options:
        command.extend(ffmpeg_options.split(" "))

    command.append(output_file)

    logging.debug("Executing command: %s", " ".join(command))
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout:
        logging.debug("FFmpeg Output: %s", result.stdout.decode("utf-8"))
    if result.stderr:
        logging.error("FFmpeg Error: %s", result.stderr.decode("utf-8"))


def process_audio_files(
    input_dir, output_dir, target_bpm, range_percentage, ffmpeg_options, format
):
    lower_bound = target_bpm * (1 - range_percentage / 100)
    upper_bound = target_bpm * (1 + range_percentage / 100)

    def process_file(file_path, root, is_single_file=False):
        try:
            file_name = os.path.basename(file_path)
            bpm = analyze_bpm(file_path, target_bpm)
            if bpm is None:
                logging.warning(f"Failed to analyze BPM for '{file_name}'")
                return
            logging.info(f"File: {file_name} - BPM: {bpm}")

            bpm_to_use = None
            if lower_bound <= bpm <= upper_bound:
                bpm_to_use = target_bpm
            elif lower_bound <= bpm * 2 <= upper_bound:
                bpm_to_use = target_bpm / 2
            else:
                logging.info(f"'{file_name}' remains unchanged - BPM: {bpm}")
                return

            if is_single_file:
                new_dir = output_dir
            else:
                relative_path = os.path.relpath(root, input_dir)
                new_dir = os.path.join(output_dir, relative_path)

            if not os.path.exists(new_dir):
                os.makedirs(new_dir)

            base_name, original_ext = os.path.splitext(file_name)
            file_ext = format if format is not None else original_ext[1:]
            output_path = os.path.join(new_dir, f"{base_name}.{file_ext}")

            logging.info(f"Adjusting '{file_name}' from BPM: {bpm} to {bpm_to_use}")

            tempo_factor = bpm_to_use / bpm
            adjust_tempo_ffmpeg(
                file_path, output_path, file_ext, tempo_factor, ffmpeg_options
            )

        except Exception as e:
            logging.error(f"Error processing {file_name}: {e}")
            traceback.print_exc()

    if os.path.isfile(input_dir):
        process_file(input_dir, os.path.dirname(input_dir), is_single_file=True)
    elif os.path.isdir(input_dir):
        for root, dirs, files in os.walk(input_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                process_file(file_path, root)
    else:
        logging.error(f"The input path '{input_dir}' is not a valid file or directory.")


def main(
    input_path, output_path, target_bpm, range_percentage, ffmpeg_options, to_m4a=False
):
    process_audio_files(
        input_path, output_path, target_bpm, range_percentage, ffmpeg_options, to_m4a
    )

    logging.info("Processing completed.")
