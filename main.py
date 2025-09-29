import os 
import subprocess
import sys
import time
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
import yt_dlp
import re

class YoutubeAutomation:
    def __init__(self):
        self.yLink = list()
        self.downloadPath = None
        self.use_cookies = False
        self.browser_name = None
        self.cookie_method = None

    def get_youtube_link(self, input_prompt):
        if input_prompt == "exit":
            for link in self.yLink:
                print(f"✅ Youtube Link Listed: {link}")
            return False

        links = re.findall(
            r"https://www\.youtube\.com/(?:watch\?v=[\w\-]+|playlist\?list=[\w\-]+)",
            input_prompt
        )
        if not links:
            print("❌ No valid YouTube links found. Please try again.")
            return True

        added = 0
        for link in links:
            if link not in self.yLink:
                self.yLink.append(link)
                added += 1
            else:
                print(f"❌ This link has already been added: {link}")
        if added:
            print(f"✅ Added {added} new link(s).")
        return True
    
    def get_download_path(self, input_prompt):
        if input_prompt == "exit":
            return False

        if input_prompt is not None and not os.path.isdir(input_prompt):
            print("❌ Invalid download path. Please try again.")
            return None
        self.downloadPath = input_prompt
        return self.downloadPath
    
    def close_browser(self, browser_name):
        """Close the specified browser automatically"""
        browser_processes = {
            'chrome': ['chrome.exe', 'chromedriver.exe'],
            'firefox': ['firefox.exe'],
            'edge': ['msedge.exe'],
            'safari': ['safari.exe'],
            'opera': ['opera.exe']
        }
        
        if browser_name not in browser_processes:
            return False
            
        print(f"🔄 Automatically closing {browser_name.title()}...")
        
        try:
            for process_name in browser_processes[browser_name]:
                # Use taskkill to force close the browser
                result = subprocess.run(['taskkill', '/F', '/IM', process_name], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ Closed {process_name}")
                    
            # Wait a moment for processes to fully close
            time.sleep(3)
            print("✅ Browser closed successfully")
            return True
            
        except Exception as e:
            print(f"⚠️  Could not automatically close browser: {e}")
            print("Please close the browser manually and press Enter...")
            input()
            return True
    
    def setup_cookies(self):
        print("\n🍪 Cookie Authentication Setup")
        print("This will help download private videos you have access to.")
        use_cookies = input("Do you want to use browser cookies? (y/n): ").lower().strip()
        
        if use_cookies == 'y':
            print("\nCookie methods:")
            print("1. Extract from browser (auto-close browser)")
            print("2. Use manual cookie file (cookies.txt)")
            print("3. Skip cookies")
            
            method = input("Choose method (1-3): ").strip()
            
            if method == '1':
                print("\nAvailable browsers:")
                print("1. Chrome")
                print("2. Firefox (Recommended - better cookie support)")
                print("3. Edge")
                print("4. Safari")
                print("5. Opera")
                
                choice = input("Choose your browser (1-5): ").strip()
                browser_map = {
                    '1': 'chrome',
                    '2': 'firefox', 
                    '3': 'edge',
                    '4': 'safari',
                    '5': 'opera'
                }
                
                if choice in browser_map:
                    self.browser_name = browser_map[choice]
                    self.use_cookies = True
                    self.cookie_method = 'browser'
                    
                    # Special handling for Chrome DPAPI issues
                    if self.browser_name == 'chrome':
                        print("\n⚠️  Chrome may have encryption issues on some systems.")
                        print("If extraction fails, consider using:")
                        print("1. Firefox instead (better cookie support)")
                        print("2. Manual cookie file export")
                        proceed = input("Still want to try Chrome? (y/n): ").lower().strip()
                        if proceed != 'y':
                            print("📝 Please choose a different method or browser.")
                            return self.setup_cookies()
                    
                    # Automatically close the browser
                    print(f"\n⚠️  About to automatically close {self.browser_name.title()}")
                    confirm = input("Continue? (y/n): ").lower().strip()
                    
                    if confirm == 'y':
                        if self.close_browser(self.browser_name):
                            print(f"✅ Will extract cookies from {self.browser_name.title()}")
                        else:
                            print("❌ Failed to close browser, proceeding without cookies.")
                            self.use_cookies = False
                    else:
                        print("❌ Cancelled, proceeding without cookies.")
                        self.use_cookies = False
                else:
                    print("❌ Invalid choice, proceeding without cookies.")
                    
            elif method == '2':
                print("\n📝 Manual Cookie File Instructions:")
                print("1. Install browser extension 'Get cookies.txt LOCALLY'")
                print("2. Go to YouTube and make sure you're logged in")
                print("3. Click the extension and export cookies for youtube.com")
                print("4. Save the file as 'cookies.txt' in this folder")
                print()
                
                cookie_file = input("Enter path to cookies.txt file (or press Enter for 'cookies.txt'): ").strip()
                if not cookie_file:
                    cookie_file = 'cookies.txt'
                
                if os.path.exists(cookie_file):
                    self.cookie_method = 'file'
                    self.browser_name = cookie_file  # Store file path
                    self.use_cookies = True
                    print(f"✅ Will use cookie file: {cookie_file}")
                    print("📝 Make sure your cookies.txt file is in Netscape format!")
                else:
                    print(f"❌ Cookie file not found: {cookie_file}")
                    print("📝 Create the cookie file and try again")
                    retry = input("Want to try again? (y/n): ").lower().strip()
                    if retry == 'y':
                        return self.setup_cookies()
            else:
                print("📝 Proceeding without cookies")
        else:
            print("📝 Proceeding without cookies (may skip private videos)")
    
    def check_youtube_link_if_valid(self):
        # Skip pytube validation for playlists when using cookies
        if self.use_cookies:
            print("ℹ️  Skipping link validation (using cookie authentication)")
            return True
            
        for link in self.yLink:
            try:
                YouTube(link)  
            except VideoUnavailable:
                print(f"❌ Video unavailable: {link}")
                return False
            except Exception:
                print(f"❌ Error processing link: {link}")
                return False
        return True
    
    def update_ytdlp(self):
        """Update yt-dlp to the latest version"""
        try:
            print("🔄 Updating yt-dlp to latest version...")
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ yt-dlp updated successfully")
                return True
            else:
                print(f"⚠️  Update failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"⚠️  Could not update yt-dlp: {e}")
            return False
    
    def download_videos(self):
        self.check_youtube_link_if_valid()
        if not self.yLink:
            print("No valid YouTube links to download.")
            return False

        # Check if user wants to update yt-dlp first
        update_choice = input("Update yt-dlp to latest version? (recommended) (y/n): ").lower().strip()
        if update_choice == 'y':
            self.update_ytdlp()
            print()

        ydl_opts = {
            # More flexible format selection to avoid signature issues
            'format': '(bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio)/best',
            'outtmpl': os.path.join(self.downloadPath, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': False,
            'ignoreerrors': True,
            'no_warnings': False,
            'extract_flat': False,
            # Additional options to handle signature issues
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'player_skip': ['dash', 'hls'],
                }
            },
            # Retry options
            'retries': 3,
            'fragment_retries': 3,
            # Bypass age gate
            'age_limit': None,
        }
        
        # Add cookie support based on method
        if self.use_cookies and self.browser_name:
            if self.cookie_method == 'browser':
                ydl_opts['cookiesfrombrowser'] = (self.browser_name,)
                print(f"🍪 Extracting cookies from {self.browser_name.title()}")
            elif self.cookie_method == 'file':
                ydl_opts['cookiefile'] = self.browser_name  # browser_name contains file path
                print(f"🍪 Using cookie file: {self.browser_name}")

        success_count = 0
        error_count = 0
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for link in self.yLink:
                try:
                    print(f"🔄 Processing: {link}")
                    ydl.download([link])
                    print(f"✅ Successfully processed: {link}")
                    success_count += 1
                except Exception as e:
                    error_msg = str(e).lower()
                    print(f"❌ Error downloading {link}: {e}")
                    
                    # Specific handling for different types of errors
                    if 'signature extraction failed' in error_msg:
                        print("💡 Signature extraction issue - this is usually fixed by updating yt-dlp")
                    elif 'dpapi' in error_msg or 'decrypt' in error_msg:
                        print("💡 Cookie decryption failed. Try using:")
                        print("   1. Firefox instead of Chrome")
                        print("   2. Manual cookie file export")
                        print("   3. Running without cookies")
                    elif 'private video' in error_msg:
                        print("💡 Private video encountered - cookies may help")
                    elif '403 forbidden' in error_msg or 'fragment' in error_msg:
                        print("💡 Format access issue - trying alternative formats")
                    elif 'requested format is not available' in error_msg:
                        print("💡 Format unavailable - trying to extract audio anyway")
                    
                    print("⏭️  Continuing with next link...")
                    error_count += 1
        
        print(f"\n📊 Download Summary:")
        print(f"✅ Successful: {success_count}")
        print(f"❌ Failed: {error_count}")
        
        if error_count > 0:
            print("\n💡 If downloads are failing:")
            print("   • Update yt-dlp regularly (YouTube changes frequently)")
            print("   • Check if videos are region-blocked or private")
            print("   • Try using cookies for private/unlisted videos")
            print("   • Some formats may not be available due to YouTube restrictions")
        
        return success_count > 0

if __name__ == "__main__":
    yt_automation = YoutubeAutomation()
        
    while True:
        download_path = input(str("Enter the download path (or type 'exit' to finish): "))
        process = yt_automation.get_download_path(download_path)
        if process is not None:
            break
    
    # Setup cookie authentication
    yt_automation.setup_cookies()
        
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