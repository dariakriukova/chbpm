import librosa
import audioread
import os
import shutil
import subprocess
import traceback
import numpy as np
import warnings
import logging

warnings.filterwarnings('ignore', category=FutureWarning, module='librosa.core.audio')
warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def analyze_bpm(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None, mono=True)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        logging.info(f"Analyzed BPM for '{file_path}' - BPM: {tempo}")
        return tempo
    except audioread.NoBackendError:
        logging.warning(f"No backend available for file: {file_path}")
        return None


def adjust_tempo_ffmpeg(input_file, output_file, original_bpm, target_bpm):
    tempo_factor = target_bpm / original_bpm
    command = [
    'ffmpeg', '-i', input_file, 
    '-filter:a', f'atempo={tempo_factor}', 
    '-c:a', 'libfdk_aac', '-vbr', '4', 
    '-c:v', 'copy', '-map', '0', 
    output_file
    ]
    
    logging.info('Executing command: ' + ' '.join(command))
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def process_audio_files(input_folder_path, output_folder_path, target_bpm=None, range_percentage=15):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    
    for root, dirs, files in os.walk(input_folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            try:
                logging.info(f"Analyzing '{file_name}'")
                bpm = analyze_bpm(file_path)
                if bpm is None:
                    logging.warning(f"Failed to analyze BPM for '{file_name}'")
                    continue
                logging.info(f"File: {file_name} - BPM: {bpm}")

                bpm_to_use = None
                if target_bpm:
                    lower_bound = target_bpm * (1 - range_percentage / 100)
                    upper_bound = target_bpm * (1 + range_percentage / 100)
                    if lower_bound <= bpm <= upper_bound:
                        bpm_to_use = target_bpm
                else:
                    if 80 <= bpm < 100:
                        bpm_to_use = 90
                    elif 147 <= bpm <= 210:
                        bpm_to_use = 180
                
                if bpm_to_use:
                    base_name, _ = os.path.splitext(file_name)
                    relative_path = os.path.relpath(root, input_folder_path)
                    new_dir = os.path.join(output_folder_path, relative_path)
                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir)

                    output_path = os.path.join(new_dir, base_name + '.m4a')
                    
                    logging.info(f"Adjusting '{file_name}' from BPM: {bpm} to {bpm_to_use}")
                    adjust_tempo_ffmpeg(file_path, output_path, bpm, bpm_to_use)
                else:
                    logging.info(f"'{file_name}' remains unchanged - BPM: {bpm}")

            except Exception as e:
                logging.error(f"Error processing {file_name}: {e}")
                traceback.print_exc()


def main(input_path=None, output_path=None, target_bpm=None, range_percentage=15):
    if input_path is None:
        input_folder_path = input("Please enter the path of your music folder: ")
    else:
        input_folder_path = input_path
    
    if output_path is None:
        output_folder_path = os.path.join(os.path.dirname(input_folder_path), "adjusted")
    else:
        output_folder_path = output_path

    process_audio_files(input_folder_path, output_folder_path, target_bpm, range_percentage)

    logging.info("Processing completed.")

