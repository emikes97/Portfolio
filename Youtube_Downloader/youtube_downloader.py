from helper import Helper
from downloader import Downloader
from pathlib import Path

class YtbDownloader:

    def __init__(self):
        """Iniatializing everything that is needed for the program to function. Should be kept simple"""
        self.program_choices = {}  # It will store all the menu options in here
        self.program_choices_helper = {}  # Maps the keys for "program_choices" to make it easier for the user to minimize input

        # Lists
        self.media_formats = ["MP3", "WAV", "FLAC", "AAC", "OGG"] # Media Format Options
        self.display_options = ["DISPLAY_OPT", "DISPLAY_MED"] # Display Options
        self.request_input = ["STRING", "INT"]
        self.reason_to_pass = ["APP_FUNC", "URL", "AUDIO_FORMAT"]

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
            self.help.display_to_screen(self.display_options[0], self.program_choices) # Display the Options of the APP
            choice = self.help.retrieve_input(self.request_input[0], self.reason_to_pass[0], self.program_choices) # Retrieve the Option
            label = self.help.user_choices(choice, self.program_choices_helper) # Retrieve the label for the function

            if not label:
                print("[WARN]: An action hasn't been chosen")
                continue
            elif label not in self.program_choices:
                print(f"[ERROR]: The label {label} isn't mapped to a function")
                continue

            match label:

                case "Download Audio":
                    self._download_audio(label)

                case "Exit":
                    self._terminate_app()

    def _download_audio(self, label):
        function_to_run = self.program_choices[label]  # Retrieve the function
        self.help.display_to_screen(self.display_options[1], self.media_formats)  # Display the Options of the APP
        audio_format_index = self.help.retrieve_input(self.request_input[1], self.reason_to_pass[2], self.media_formats)
        audio_format = self.media_formats[audio_format_index].lower()
        url = self.help.retrieve_input(self.request_input[0],self.reason_to_pass[1])  # Request the URL if function is for download
        function_to_run.download_audio(url, audio_format, self.path)

    def _terminate_app(self):
        self.app_is_on = False
        print("APP was terminated gracefully")

    def dict_constructor(self):
        self.program_choices = {
            "Download Audio": self.download,
            "Exit": self._terminate_app
        }  # It will store all the menu options in here
        self.program_choices_helper = {
            "1": "Download Audio",
            "2": "Exit"
        }  # Maps the keys for "program_choices" to make it easier for the user to minimize input