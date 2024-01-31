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


def adjust_tempo_ffmpeg(
    input_file, output_file, original_bpm, target_bpm, ffmpeg_options
):
    tempo_factor = target_bpm / original_bpm
    command = [
        "ffmpeg",
        "-loglevel",
        "error",
        "-i",
        input_file,
        "-filter:a",
        f"atempo={tempo_factor}",
        "-c:v",
        "copy",
        "-map",
        "0",
        "-y",
        output_file,
    ]

    if ffmpeg_options:
        command.extend(ffmpeg_options.split(" "))

    logging.debug("Executing command: " + " ".join(command))
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout:
        logging.debug("FFmpeg Output: " + result.stdout.decode('utf-8'))
    if result.stderr:
        logging.error("FFmpeg Error: " + result.stderr.decode('utf-8'))


def process_audio_files(
    input_dir, output_dir, target_bpm, range_percentage, ffmpeg_options, format
):
    lower_bound = target_bpm * (1 - range_percentage / 100)
    upper_bound = target_bpm * (1 + range_percentage / 100)

    

    for root, dirs, files in os.walk(input_dir):
        
        for file_name in files:
            file_path = os.path.join(root, file_name)

            try:
                bpm = analyze_bpm(file_path, target_bpm)
                if bpm is None:
                    continue
                logging.info(f"File: {file_name} - BPM: {bpm}")

                bpm_to_use = None
                if lower_bound <= bpm <= upper_bound:
                    bpm_to_use = target_bpm
                elif lower_bound <= bpm * 2 <= upper_bound:
                    bpm_to_use = target_bpm / 2
                else:
                    logging.info(f"'{file_name}' remains unchanged - BPM: {bpm}")
                    continue

                relative_path = os.path.relpath(root, input_dir)
                new_dir = os.path.join(output_dir, relative_path)
                if not os.path.exists(new_dir):
                    os.makedirs(new_dir)

                base_name, original_ext = os.path.splitext(file_name)
                new_ext = f'.{format}' if format is not None else original_ext
                output_path = os.path.join(new_dir, f"{base_name}{new_ext}")

                logging.info(f"Adjusting '{file_name}' from BPM: {bpm} to {bpm_to_use}")
                adjust_tempo_ffmpeg(
                    file_path, output_path, bpm, bpm_to_use, ffmpeg_options
                )

            except Exception as e:
                logging.error(f"Error processing {file_name}: {e}")
                traceback.print_exc()


def main(input_path, output_path, target_bpm, range_percentage, ffmpeg_options, to_m4a=False):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    process_audio_files(
        input_path, output_path, target_bpm, range_percentage, ffmpeg_options, to_m4a
    )

    logging.info("Processing completed.")
