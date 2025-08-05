# YouTube to MP3 Automation

A Python script that automatically downloads YouTube videos and converts them to MP3 audio files using `yt-dlp`.

## Features

-   Download multiple YouTube videos at once (batch download)
-   Paste multiple YouTube links in a single input (even without spaces)
-   Automatic conversion of videos to high-quality MP3 audio
-   Input validation for YouTube links and download paths
-   Error handling for invalid or unavailable videos

## Requirements

-   Python 3.11 or higher
-   FFmpeg (required for audio conversion)
-   Internet connection

## Installation

### 1. Clone or Download the Project

Download the project files to your computer or clone the repository.

### 2. Install Python Dependencies

Navigate to the project directory and install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg

FFmpeg is required for audio conversion. Follow the instructions for your operating system:

#### Windows

**Option 1: Using Chocolatey (Recommended)**

1. Install Chocolatey if you haven't: https://chocolatey.org/install
2. Run Command Prompt as Administrator
3. Install FFmpeg:
    ```bash
    choco install ffmpeg
    ```

**Option 2: Manual Installation**

1. Download FFmpeg from: https://ffmpeg.org/download.html#build-windows
2. Extract the downloaded zip file to a folder (e.g., `C:\ffmpeg`)
3. Add FFmpeg to your system PATH:
    - Press `Win + R`, type `sysdm.cpl`, press Enter
    - Click "Environment Variables"
    - Under "System Variables", find and select "Path", click "Edit"
    - Click "New" and add the path to FFmpeg's bin folder (e.g., `C:\ffmpeg\bin`)
    - Click "OK" to save changes
    - Restart your command prompt

#### macOS

**Using Homebrew:**

```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install ffmpeg
```

### 4. Verify FFmpeg Installation

Open a new command prompt/terminal and run:

```bash
ffmpeg -version
```

If FFmpeg is properly installed, you'll see version information.

## Usage

### 1. Run the Script

```bash
python main.py
```

### 2. Enter Download Path

When prompted, enter the folder path where you want to save the MP3 files:

```
Enter the download path (or type 'exit' to finish): C:\Users\YourName\Music
```

### 3. Add YouTube Links

Enter YouTube video URLs one by one. The script accepts links in this format:

```
Enter a YouTube link (or type 'exit' to finish): https://www.youtube.com/watch?v=VIDEO_ID
```

Continue adding links, or type `exit` when you're done adding URLs.

### 4. Download and Convert

The script will automatically:

-   Validate all YouTube links
-   Download the best available audio quality
-   Convert to MP3 format (192 kbps)
-   Save files to your specified download folder

## Example Usage

```
Enter the download path (or type 'exit' to finish): C:\Users\John\Downloads
Enter a YouTube link (or type 'exit' to finish): https://www.youtube.com/watch?v=dQw4w9WgXcQ
Enter a YouTube link (or type 'exit' to finish): https://www.youtube.com/watch?v=oHg5SJYRHA0
Enter a YouTube link (or type 'exit' to finish): exit
✅ Youtube Link Listed: https://www.youtube.com/watch?v=dQw4w9WgXcQ
✅ Youtube Link Listed: https://www.youtube.com/watch?v=oHg5SJYRHA0
Downloaded and converted: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Downloaded and converted: https://www.youtube.com/watch?v=oHg5SJYRHA0
Download completed successfully.
```

## Troubleshooting

### Common Issues

**"FFmpeg not found" error:**

-   Make sure FFmpeg is installed and added to your system PATH
-   Restart your command prompt after installation
-   Verify installation with `ffmpeg -version`

**"Invalid YouTube link" error:**

-   Ensure the link starts with `https://www.youtube.com/watch?v=`
-   Check that the video exists and is publicly accessible

**"Invalid download path" error:**

-   Make sure the folder path exists
-   Use absolute paths (full path from drive root)
-   Ensure you have write permissions to the folder

**"Video unavailable" error:**

-   The video might be private, deleted, or region-restricted
-   Try a different video URL

### Python Version Issues

If you encounter issues with missing modules (like `audioop`), make sure you're using Python 3.11 or higher but not Python 3.12+ if using other audio libraries.

## File Structure

```
YTMP3 Automation/
├── main.py           # Main script file
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

## Dependencies

-   `yt-dlp`: Modern YouTube downloader and video processor
-   `os`: Built-in Python module for file system operations

## License

This script is for educational and personal use only. Please respect YouTube's Terms of Service and copyright laws when downloading content.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Changelog

### Version 1.0

-   Initial release
-   Basic YouTube to MP3 conversion
-   Multiple link support
-   Error handling and validation
