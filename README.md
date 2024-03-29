# Chbpm: BPM Adjustment Tool

     ██████╗██╗  ██╗██████╗ ██████╗ ███╗   ███╗    
    ██╔════╝██║  ██║██╔══██╗██╔══██╗████╗ ████║    
    ██║     ███████║██████╔╝██████╔╝██╔████╔██║    
    ██║     ██╔══██║██╔══██╗██╔═══╝ ██║╚██╔╝██║    
    ╚██████╗██║  ██║██████╔╝██║     ██║ ╚═╝ ██║    
     ╚═════╝╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝     ╚═╝    


## Overview
Chbpm is a Python-based tool designed for analyzing and adjusting the tempo of music tracks. This tool is ideal for fitness enthusiasts, dancers, and anyone who needs music to maintain a consistent BPM for their activities. The primary goal is to adjust the BPM of songs to fit within a target BPM range, facilitating a consistent pace during workouts or dance routines.

## Features
- **BPM Analysis**: Automatically analyzes the BPM of music files.
- **BPM Adjustment**: Adjusts the tempo of music tracks to a target BPM suitable for exercise or dance routines.
- **Dual BPM Handling**: For songs within a specified range, it uses the target BPM directly. For songs where double the BPM falls within the range, it adjusts to half the target BPM.
- **File Format Support**: Compatible with various audio file formats (e.g., MP3, M4A).
- **Error Logging**: Detailed logging for troubleshooting, including optional suppression of verbose `ffmpeg` metadata output.

## Installation
Ensure `ffmpeg` is installed on your system. [Installation inctructions.](https://ffmpeg.org/download.html)
### For Users
```bash
pip install chbpm
```

### For Developers
1. Install Pipenv:
```bash
pip install pipenv
```
2. Clone this repository.
```bash
git clone https://github.com/dariakriukova/rhythm-is-a-runner.git
```
3. Navigate to the Project Directory
4. Install Dependencies:
```bash
pipenv install
```
5. Activate the Virtual Environment:
```bash
pipenv shell
```

## Usage
Run the tool from the command line, specifying the input folder and other optional parameters:

```bash
python -m chbpm path_to_music_folder
```

### Command-Line Options
- `input_path`: Path to the input music folder. 

- `-o`, `--output_path`: Path to the output folder where adjusted music files will be saved. Defaults to `adjusted`.  

- `-t`, `--target_bpm`: Optional target BPM for tempo adjustment. Defaults to `180`.  

- `-r`, `--range_percentage`: Percentage for BPM range adjustment. Defaults to `15%`. This setting determines the 
flexibility in BPM adjustment.  

- `--log`: Set log level. INFO by default.

- `--format`: Convert output audio files to given format. By default keeps the original format.

`--ffmpeg_options`: Control over the audio processing, enabling adjustments to codec, bitrate, and more.

### Important Note
The arguments passed through `--ffmpeg_options` are directly supplied to FFmpeg, so it's essential to ensure they are valid and compatible with the input and output file formats being used. Refer to the [FFmpeg documentation](https://ffmpeg.org/ffmpeg.html) for a comprehensive list of available options.