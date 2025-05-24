from ytb_dlp import YTDLPWrapper

class Downloader:
    def __init__(self, output_path="downloads", audio_only=False):
        self.wrapper = YTDLPWrapper(output_path, audio_only)

    def download_audio(self, url, path):
        self.wrapper.output_path = path
        self.wrapper.audio_only = True
        return self.wrapper.download(url)

    def download_video(self, url, path):
        self.wrapper.output_path = path
        self.wrapper.audio_only = False
        return self.wrapper.download(url)

    def multiple_downloads(self, queue, path, audio_only=False):
        self.wrapper.output_path = path
        self.wrapper.audio_only = audio_only

        for video in queue:
            self.wrapper.download(video)

        return True