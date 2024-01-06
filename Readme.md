# MMBs Video Concatenator

This Python script creates a simple UI for concatenating video files from a SD card to a single mp4 file ordered by date.
It also automatically creates a backup of it on an external drive and is able to delete all files from the SD card afterwards.
It is designed for inexperienced home video filmers who just want to merge and save their clips once a month.

## Requirements

- Python 3
- TKinter
- FFmpeg installed (download from [here](https://ffmpeg.org/download.html))

## Usage

1. Clone or download this repository.

2. Install Python, TKinter and FFmpeg if not already installed.

3. Set up the configuration file (`MVC.cfg`) with the desired backup path, for instance your external hard drive.

4. Run the script using the provided batch file (`MVC.bat`) on windows or use `python3 MVC.py` in the terminal.

## Configuration

- **MVC.cfg**: Edit this configuration file to set the backup path.
  Ideally this should be an external hard drive or a mounted cloud storage.
  Make sure that sufficient amount of storage space is available!

## Notes

- Ensure that Python is added to the system's PATH variable.

- Make sure to have the required permissions for file manipulation.



