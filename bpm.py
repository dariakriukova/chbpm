import librosa
import os
import shutil
import subprocess
import traceback
import numpy as np
import audioread

def analyze_bpm(file_path):
    with audioread.audio_open(file_path) as f:
        audio_data = []
        for buffer in f:
            audio_data.append(np.frombuffer(buffer, dtype=np.int16))

        y = np.concatenate(audio_data)
        if f.channels > 1:
            y = y.reshape(-1, f.channels)
            y = np.mean(y, axis=1)

    y = y.astype(np.float32) / np.iinfo(np.int16).max

    tempo, _ = librosa.beat.beat_track(y=y, sr=f.samplerate)
    return tempo


def adjust_tempo_ffmpeg(input_file, output_file, original_bpm, target_bpm):
    tempo_factor = target_bpm / original_bpm
    command = ['ffmpeg', '-i', input_file, '-filter:a', f'atempo={tempo_factor}', output_file]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def process_audio_files(source_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            if file_name.startswith('.') or not file_name.lower().endswith(('.mp3', '.wav', '.m4a')):
                continue

            file_path = os.path.join(root, file_name)

            try:
                bpm = analyze_bpm(file_path)
                print(f"Analyzing '{file_name}' - BPM: {bpm}")

                if 80 <= bpm < 100 or 150 <= bpm <= 210:
                    target_bpm = 90 if bpm < 100 else 180
                    output_path = os.path.join(output_folder, file_name)
                    print(f"Adjusting '{file_name}' from BPM: {bpm} to {target_bpm}")
                    adjust_tempo_ffmpeg(file_path, output_path, bpm, target_bpm)

                else:
                    print(f"'{file_name}' remains unchanged - BPM: {bpm}")

            except Exception as e:
                print(f"Error processing {file_name}: {e}")
                traceback.print_exc()

def main():
    input_folder_path = input("Please enter the path of your music folder: ")
    output_folder_path = os.path.join(os.path.dirname(input_folder_path), "adjusted")

    process_audio_files(input_folder_path, output_folder_path)

    print("Processing completed.")

if __name__ == "__main__":
    main()
