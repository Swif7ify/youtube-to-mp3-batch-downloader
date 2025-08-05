
import os 
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
import yt_dlp

class YoutubeAutomation:
    def __init__(self):
        self.yLink = list()
        self.downloadPath = None

    def get_youtube_link(self, input_prompt):
        if input_prompt == "exit":
            for link in self.yLink:
                print(f"✅ Youtube Link Listed: {link}")
            return False
        
        if input_prompt is not None and not input_prompt.startswith("https://www.youtube.com/watch?v="):
            print("❌ Invalid YouTube link. Please try again.")
            return True
        
        if input_prompt is not None and input_prompt.startswith("https://www.youtube.com/watch?v="):
            if input_prompt in self.yLink:
                print("❌ This link has already been added.")
                return True
            self.yLink.append(input_prompt)
            return True
    
    def get_download_path(self, input_prompt):
        if input_prompt == "exit":
            return False

        if input_prompt is not None and not os.path.isdir(input_prompt):
            print("❌ Invalid download path. Please try again.")
            return None
        self.downloadPath = input_prompt
        return self.downloadPath
    
    def check_youtube_link_if_valid(self):
        temp = []
        for link in self.yLink:
            try:
                yt = YouTube(link)
                temp.append(yt)
            except VideoUnavailable:
                print(f"❌ Video unavailable: {link}")
                return False
            except Exception:
                print(f"❌ Error processing link: {link}")
                return False
        self.yLink = temp
        return True
    
    def download_videos(self):
        if not self.yLink:
            print("No valid YouTube links to download.")
            return False

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.downloadPath, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': False,
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for link in self.yLink:
                try:
                    ydl.download([link])
                    print(f"Downloaded and converted: {link}")
                except Exception as e:
                    print(f"Error downloading {link}: {e}")
        return True

if __name__ == "__main__":
    yt_automation = YoutubeAutomation()
        
    while True:
        download_path = input(str("Enter the download path (or type 'exit' to finish): "))
        process = yt_automation.get_download_path(download_path)
        if process is not None:
            break
        
    while True:
        link = input(str("Enter a YouTube link (or type 'exit' to finish): "))
        process = yt_automation.get_youtube_link(link)
        if not process:
            break
        
    process = yt_automation.download_videos()
    if process:
        print("Download completed successfully.")
    else:
        print("Download failed.")
