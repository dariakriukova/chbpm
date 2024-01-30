# Rhythm Runner: BPM Adjustment Tool

## Overview
Rhythm Runner is a Python-based tool designed for analyzing and adjusting the tempo of music tracks. This tool is ideal for fitness enthusiasts, dancers, and anyone who needs music to maintain a consistent BPM for their activities. The primary goal is to adjust the BPM of songs to fit within a target BPM range, facilitating a consistent pace during workouts or dance routines.

## Features
- **BPM Analysis**: Automatically analyzes the BPM of music files.
- **BPM Adjustment**: Adjusts the tempo of music tracks to a target BPM suitable for exercise or dance routines.
- **Dual BPM Handling**: For songs within a specified range, it uses the target BPM directly. For songs where double the BPM falls within the range, it adjusts to half the target BPM.
- **File Format Support**: Compatible with various audio file formats (e.g., MP3, M4A).
- **Error Logging**: Detailed logging for troubleshooting, including optional suppression of verbose `ffmpeg` metadata output.

## Installation
Ensure Python and `ffmpeg` are installed on your system, then:

1. Clone or download this repository.
2. Install required Python packages:  

## Usage
Run the tool from the command line, specifying the input folder and other optional parameters:

```bash
python -m chbpm path_to_music_folder
```

### Command-Line Options
- `input_path`: Path to the input music folder. 
```bash
python -m chbpm <input_path>
```
- `-o`, `--output_path`: Path to the output folder where adjusted music files will be saved. Defaults to `adjusted`.  
```bash
python -m chbpm <input_path> -o <output_path>
```
- `-t`, `--target_bpm`: Optional target BPM for tempo adjustment. Defaults to `180`.  
```bash
python -m chbpm <input_path> -t <target_bpm>
```
- `-r`, `--range_percentage`: Percentage for BPM range adjustment. Defaults to `15%`. This setting determines the 
flexibility in BPM adjustment.  
```bash
python -m chbpm <input_path> -r <range_percentage>
```