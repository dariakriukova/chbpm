import librosa
import os
import shutil
import subprocess
import traceback

# Analyze BPM function
def analyze_bpm(file_path):
    y, sr = librosa.load(file_path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return tempo

# Load audio file function
def load_audio_file(file_path):
    file_format = file_path.split('.')[-1]
    if file_format == 'mp3':
        return AudioSegment.from_mp3(file_path)
    elif file_format == 'm4a':
        return AudioSegment.from_file(file_path, format='m4a')
    else:
        return AudioSegment.from_file(file_path)

# FFmpeg-based function to adjust tempo
def adjust_tempo_ffmpeg(input_file, output_file, original_bpm, target_bpm):
    tempo_factor = target_bpm / original_bpm
    command = ['ffmpeg', '-i', input_file, '-filter:a', f'atempo={tempo_factor}', output_file]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Process audio files function
def process_audio_files(source_folder, output_folder, target_bpm=90):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(source_folder):
        if file_name.startswith('.') or not file_name.lower().endswith(('.mp3', '.wav', '.m4a')):
            continue

        file_path = os.path.join(source_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        try:
            bpm = analyze_bpm(file_path)
            print(f"Analyzing '{file_name}' - BPM: {bpm}")

            if 160 <= bpm <= 200 or 80 <= bpm < 100:
                print(f"Processing '{file_name}' - BPM: {bpm}")

                if 80 <= bpm < 100:
                    # Adjust tempo using FFmpeg
                    adjust_tempo_ffmpeg(file_path, output_path, bpm, target_bpm)
                else:
                    # Copy the file as is
                    shutil.copy(file_path, output_path)

        except Exception as e:
            print(f"Error processing {file_name}: {e}")
            traceback.print_exc()

# Paths to input and output folders
input_folder_path = 'music'
output_folder_path = 'adjusted'

# Call the process_audio_files function
process_audio_files(input_folder_path, output_folder_path)
