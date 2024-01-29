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

def process_audio_files(source_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            try:
                logging.info(f"Analyzing '{file_name}'")
                bpm = analyze_bpm(file_path)
                if bpm is None:
                    logging.warning(f"Failed to analyze BPM for '{file_name}'")
                    continue
                logging.info(f"File: {file_name} - BPM: {bpm}")
                
                if 80 <= bpm < 100 or 147 <= bpm <= 210:
                    target_bpm = 90 if bpm < 100 else 180
                    
                    base_name, _ = os.path.splitext(file_name)
                    relative_path = os.path.relpath(root, source_folder)
                    new_dir = os.path.join(output_folder, relative_path)
                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir)

                    output_path = os.path.join(new_dir, base_name + '.m4a')
                    
                    logging.info(f"Adjusting '{file_name}' from BPM: {bpm} to {target_bpm}")
                    adjust_tempo_ffmpeg(file_path, output_path, bpm, target_bpm)

                else:
                    logging.info(f"'{file_name}' remains unchanged - BPM: {bpm}")

            except Exception as e:
                logging.error(f"Error processing {file_name}: {e}")
                traceback.print_exc()

def main(path):
    if path is None:
        input_folder_path = input("Please enter the path of your music folder: ")
    else:
        input_folder_path = path
    output_folder_path = os.path.join(os.path.dirname(input_folder_path), "adjusted")

    process_audio_files(input_folder_path, output_folder_path)

    logging.info("Processing completed.")

