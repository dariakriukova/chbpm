# Import necessary libraries
import librosa
import os
import shutil


def analyze_bpm(file_path):
    y, sr = librosa.load(file_path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return tempo


def process_songs(folder_path, destination_folder):
    for file_name in os.listdir(folder_path):
        if file_name.startswith('.') or not file_name.lower().endswith(('.mp3', '.wav', '.m4a')):
            continue

        file_path = os.path.join(folder_path, file_name)

        try:
            bpm = analyze_bpm(file_path)
            print(f"The BPM of '{file_name}' is: {bpm}")

            if is_fast_bpm(bpm):
                move_to_fast_bpm_folder(file_path, destination_folder)

        except Exception as e:
            print(f"Error processing {file_name}: {e}")

def is_fast_bpm(bpm):
    return 80 <= bpm <= 100 or 160 <= bpm <= 200

def move_to_fast_bpm_folder(file_path, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    shutil.move(file_path, os.path.join(destination_folder, os.path.basename(file_path)))


music_folder_path = 'music'
fast_bpm_folder_path = 'fast-bpm'

process_songs(music_folder_path, fast_bpm_folder_path)