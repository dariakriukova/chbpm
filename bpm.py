import librosa
import os
import shutil
import subprocess
import traceback
import zipfile

def analyze_bpm(file_path):
    y, sr = librosa.load(file_path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return tempo

def adjust_tempo_ffmpeg(input_file, output_file, original_bpm, target_bpm):
    tempo_factor = target_bpm / original_bpm
    command = ['ffmpeg', '-i', input_file, '-filter:a', f'atempo={tempo_factor}', output_file]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def process_audio_files(source_folder, output_folder, target_bpm=90):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            if file_name.startswith('.') or not file_name.lower().endswith(('.mp3', '.wav', '.m4a')):
                continue

            file_path = os.path.join(root, file_name)
            output_path = os.path.join(output_folder, file_name)

            try:
                bpm = analyze_bpm(file_path)
                print(f"Analyzing '{file_name}' - BPM: {bpm}")

                if 160 <= bpm <= 200 or 80 <= bpm < 100:
                    print(f"Processing '{file_name}' - BPM: {bpm}")
                    if 80 <= bpm < 100:
                        adjust_tempo_ffmpeg(file_path, output_path, bpm, target_bpm)
                    else:
                        shutil.copy(file_path, output_path)

            except Exception as e:
                print(f"Error processing {file_name}: {e}")
                traceback.print_exc()


def unzip_folder(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                zip_ref.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(folder_path, '..')))

def main():
    input_zip_path = input("Please enter the path of your zipped music folder: ")
    output_zip_path = os.path.join(os.path.dirname(input_zip_path), "adjusted.zip")

    input_folder = 'temp_input'
    output_folder = 'temp_output'


    print(f"Unzipping {input_zip_path} to {input_folder}...")
    unzip_folder(input_zip_path, input_folder)

    print(f"Files in {input_folder} after unzipping:")
    if os.listdir(input_folder):
        for file in os.listdir(input_folder):
            print(file)
    else:
        print("No files found in the input folder.")
        return


    print("Processing audio files...")
    process_audio_files(input_folder, output_folder)

    print(f"Files in {output_folder} before zipping:")
    if os.listdir(output_folder):
        for file in os.listdir(output_folder):
            print(file)
    else:
        print("No files processed. Skipping zip creation.")
        return

    print(f"Creating zip file {output_zip_path}...")
    zip_folder(output_folder, output_zip_path)


    shutil.rmtree(input_folder)
    shutil.rmtree(output_folder)

    if os.path.exists('temp_output'):
        shutil.rmtree('temp_output')


    print("Processing completed.")

if __name__ == "__main__":
    main()