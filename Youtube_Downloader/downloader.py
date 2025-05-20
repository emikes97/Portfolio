from ytb_dlp import YTDLPWrapper

class Downloader:
    def __init__(self, output_path="downloads", audio_only=False):
        self.wrapper = YTDLPWrapper(output_path, audio_only)

    def download_audio(self, url, audio_format, path):
        self.wrapper.output_path = path
        self.wrapper.audio_format = audio_format
        self.wrapper.audio_only = True
        return self.wrapper.download(url)
