from ytb_dlp import YTDLPWrapper

class Downloader:
    def __init__(self, output_path="downloads", audio_only=False):
        self.wrapper = YTDLPWrapper(output_path, audio_only)

    def download_audio(self, url, audio_format, path):
        self.wrapper.output_path = path
        self.wrapper.audio_format = audio_format
        self.wrapper.audio_only = True
        return self.wrapper.download(url)

    def download_video(self, url, path):
        self.wrapper.output_path = path
        self.wrapper.audio_only = False
        return self.wrapper.download(url)

    def multiple_downloads(self, queue, path, audio_only=False, audio_format=None):
        self.wrapper.output_path = path
        self.wrapper.audio_only = audio_only

        if audio_format is not None:
            self.wrapper.audio_format = audio_format

        for video in queue:
            self.wrapper.download(video)

        return True
