import os

import yt_dlp

class YTDLPWrapper:

    def __init__(self, output_path="downloads", audio_only=True, audio_format="mp3"):
        self.output_path = output_path
        self.audio_only = audio_only
        self.audio_format = audio_format
        os.makedirs(self.output_path, exist_ok=True)

    def _build_options(self):
        opts = {
            "outtmpl": os.path.join(self.output_path, "%(title)s.%(ext)s"),
            "quiet": False,
            "noplaylist": True,
            "progress_hooks": [self._progress_hook]
        }

        if self.audio_only:
            opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": self.audio_format,  # Correct: pass the actual format (e.g., 'mp3', 'wav')
                    "preferredquality": "192"
                }]
            })
        else:
            opts.update({
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
                "postprocessor_args": {
                    "ffmpeg": ["-c:v", "copy", "-c:a", "aac", "-b:a", "192k"]
                }
            })

        return opts


    def _progress_hook(self, d):
        if d["status"] == "downloading":
            print(f"Downloading: {d['_percent_str']} at {d.get('_speed_str', 'N/A')}")
        elif d["status"] == "finished":
            print("✅ Download complete.")

    def download(self, url):
        options = self._build_options()

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            print(f"[YTDLPWrapper ERROR]: {e}")
            return False