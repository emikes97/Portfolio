import os, json, yt_dlp
from helper import Helper

CONFIG_PATH_AUDIO = Helper.get_resource_path("Active_Configurations/audio_only_download.json")
CONFIG_PATH_VIDEO = Helper.get_resource_path("Active_Configurations/video_download_mp4.json")

class YTDLPWrapper:

    def __init__(self, output_path="downloads", audio_only=True):
        self.output_path = output_path
        self.audio_only = audio_only
        #os.makedirs(self.output_path, exist_ok=True)

    def _build_options(self):

        match self.audio_only:

            case True:
                with CONFIG_PATH_AUDIO.open("r", encoding="utf-8") as file:
                    config = json.load(file)
                    config["progress_hooks"] = [self._progress_hook]
                    config["outtmpl"] = os.path.join(self.output_path, "%(title)s.%(ext)s")

                return config

            case False:
                with CONFIG_PATH_VIDEO.open("r", encoding="utf-8") as file:
                    config = json.load(file)
                    config["progress_hooks"] = [self._progress_hook]
                    config["outtmpl"] = os.path.join(self.output_path, "%(title)s.%(ext)s")

                return config

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