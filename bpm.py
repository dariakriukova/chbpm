# Import necessary libraries
import librosa
import os


def analyze_bpm(file_path):
    y, sr = librosa.load(file_path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return tempo


def process_songs(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.startswith('.') or not file_name.lower().endswith(('.mp3', '.wav')):
            continue

        file_path = os.path.join(folder_path, file_name)

        try:
            bpm = analyze_bpm(file_path)
            print(f"The BPM of '{file_name}' is: {bpm}")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")


music_folder_path = 'music'

process_songs(music_folder_path)
