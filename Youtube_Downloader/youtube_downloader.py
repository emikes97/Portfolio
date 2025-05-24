from helper import Helper
from downloader import Downloader
from pathlib import Path

class YtbDownloader:

    def __init__(self):
        """Iniatializing everything that is needed for the program to function. Should be kept simple"""
        self.program_choices = {}  # It will store all the menu options in here

        # Lists
        self.media_formats = ["MP3", "WAV", "FLAC", "AAC", "OGG"] # Media Format Options
        self.display_options = ["DISPLAY_OPT", "DISPLAY_MED"] # Display Options
        self.request_input = ["STRING", "INT"]
        self.reason_to_pass = ["APP_FUNC", "URL", "AUDIO_FORMAT", "INTEGER"]

        # Controllers / Helpers
        self.help = Helper()
        self.download = Downloader()
        self.app_is_on = True

        # APP Variables
        self.path = Path.home() / "Downloads"

        # Constructors:
        self.dict_constructor() # Constructs all dictionaries with the data they need, to less clatter init.

    def run(self):
        """Runs the program until user quits himself"""
        while self.app_is_on:
            label = self._get_label()

            if not label:
                print("[WARN]: An action hasn't been chosen")
                continue
            elif label not in [entry["label"] for entry in self.program_choices.values()]:
                print(f"[ERROR]: The label {label} isn't mapped to a function")
                continue

            match label:

                case "Download Audio":
                    self._download_audio(label)

                case "Download Video":
                    self._download_video(label)

                case ("Multiple Downloads (Audio)" | "Multiple Downloads (Videos)"):
                    self._queued_download(label)

                case "Exit":
                    self._terminate_app()

    def _download_audio(self, label):
        self.help.display_to_screen(self.display_options[1], self.media_formats)  # Display the Options of the APP
        audio_format = self._pick_audio_format()
        function_to_run, url = self._get_func_to_call_and_url(label)
        function_to_run.download_audio(url, audio_format, self.path)

    def _download_video(self, label):
        function_to_run, url = self._get_func_to_call_and_url(label)
        function_to_run.download_video(url, self.path)

    def _queued_download(self, label):
        queue = []
        videos_to_download = self.help.retrieve_input(self.request_input[1], self.reason_to_pass[3])

        if label == "Multiple Downloads (Audio)":
            audio_format = self._pick_audio_format()

        for i in range(videos_to_download):
            url = self.help.retrieve_input(self.request_input[0], self.reason_to_pass[1])  # Request the URL if function is for download
            queue.append(url)

        match label:

            case "Multiple Downloads (Audio)":
                self.download.multiple_downloads(queue, self.path, audio_format=audio_format,  audio_only=True)

            case "Multiple Downloads (Videos)":
                self.download.multiple_downloads(queue, self.path, audio_only=False)

    def _terminate_app(self):
        self.app_is_on = False
        print("APP was terminated gracefully")

    def _pick_audio_format(self):
        audio_format_index = self.help.retrieve_input(self.request_input[1], self.reason_to_pass[2], self.media_formats)
        audio_format = self.media_formats[audio_format_index].lower()
        return audio_format

    def _get_func_to_call_and_url(self, label):
        function_to_run = None
        for entry in self.program_choices.values():
            if entry.get('label') == label:
                function_to_run = entry.get('action')
                break
        url = self.help.retrieve_input(self.request_input[0],self.reason_to_pass[1])  # Request the URL if function is for download
        return function_to_run, url

    def _get_label(self):
        self.help.display_to_screen(self.display_options[0], self.program_choices)  # Display the Options of the APP
        choice = self.help.retrieve_input(self.request_input[0], self.reason_to_pass[0],self.program_choices)  # Retrieve the Option
        label = self.help.user_choices(choice, self.program_choices)  # Retrieve the label for the function

        return label

    def dict_constructor(self):

        self.program_choices = {
            "1": {"label": "Download Audio",
                  "action": self.download},
            "2": {"label": "Download Video",
                  "action": self.download},
            "3": {"label": "Multiple Downloads (Audio)",
                  "action": self.download},
            "4": {"label": "Multiple Downloads (Videos)",
                  "action": self.download},
            "5": {"label": "Options",
                  "action": None},
            "6": {"label": "Exit",
                  "action": self._terminate_app}
        }
