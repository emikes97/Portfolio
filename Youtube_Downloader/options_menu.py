import json
from pathlib import Path

CONFIG_PATH_AUDIO = Path(__file__).parent / "Active_Configurations" / "audio_only_download.json"
CONFIG_PATH_VIDEO = Path(__file__).parent / "Active_Configurations" / "video_download_mp4.json"
SAVE_PATH_CONFIG_AUDIO = Path(__file__).parent / "Prefab_Json_Configurations"
SAVE_PATH_CONFIG_VIDEO = Path(__file__).parent / "Prefab_Json_Configurations"

class Options:

    def __init__(self, helper):
        # Configs
        self.audio_config = None
        self.video_config = None

        # Controllers
        self.runner = True
        self.help = helper

        # Dictionaries
        self.options_list = {}
        self.options_list_helper = {}
        self.show_configs = {}
        self.show_configs_helper = {}
        self.change_audio = {}
        self.change_audio_helper = {}
        self.change_video = {}
        self.change_video_helper = {}

        # Constructors
        self._dict_constructor()

    def run_options_menu(self):

        while self.runner:

            label = self._get_label(self.options_list, self.options_list_helper)

            match label:

                case "Show Active Configuration (Audio | Video)":
                    self._show_active_config()

                case "Change Audio Configuration":
                    self._change_audio_config()

                case "Change Video Configuration":
                    self._change_audio_config()

                case "Load Saved Configuration":
                    self._load_saved_configuration()

                case "Save Active Configuration":
                    self._save_config()

                case "Exit Options":
                    self._exit_options()

    def _show_active_config(self):
        label = self._get_label(self.show_configs, self.show_configs_helper)

        match label:

            case "Show Audio Config":
                print("🎧 Current Audio Config:\n")
                print(json.dumps(self.audio_config, indent=4))

                return

            case "Show Video Config":
                print("🎥 Current Video Config:\n")
                print(json.dumps(self.video_config, indent=4))

                return

            case "Show Both Config":
                print("🎧 Current Audio Config:\n")
                print(json.dumps(self.audio_config, indent=4))
                print("\n" + "="*40 + "\n")
                print("🎥 Current Video Config:\n")
                print(json.dumps(self.video_config, indent=4))

                return

            case "Back":
                return

    def _change_audio_config(self):
        media_formats = ["MP3", "WAV", "FLAC", "AAC", "OGG"]  # Media Format Options
        bit_rate = ["128", "192", "256", "320"] # Quality
        changes_happened = False

        while True:

            label = self._get_label(self.change_audio, self.change_audio_helper)

            match label:

                case "Audio Format":
                    pass

                case "Bit Rate":
                    pass

    def _change_video_config(self):
        pass

    def _load_saved_configuration(self):
        pass

    def _save_config(self):
        pass

    def _exit_options(self):
        self.runner = False
        return

    def _get_label(self, list_to_pass, helper):
        self.help.display_to_screen(self.display_options[0], list_to_pass)  # Display the Options of the APP
        choice = self.help.retrieve_input(self.request_input[0], self.reason_to_pass[0],list_to_pass)  # Retrieve the Option
        label = self.help.user_choices(choice, helper)  # Retrieve the label for the function
        return label

    def _dict_constructor(self):
        """"""

        self.options_list = {
            "Show Active Configuration (Audio | Video)": self._show_active_config,
            "Change Audio Configuration": self._change_audio_config,
            "Change Video Configuration": self._change_video_config,
            "Load Saved Configuration": self._load_saved_configuration,
            "Save Active Configuration": self._save_config,
            "Exit Options": self._exit_options,
        }

        self.options_list_helper = {
            "1": "Show Active Configuration (Audio | Video)",
            "2": "Change Audio Configuration",
            "3": "Change Video Configuration",
            "4": "Load Saved Configuration",
            "5": "Save Active Configuration",
            "6": "Exit Options"
        }

        self.show_configs = {
            "Show Audio Config": None,
            "Show Video Config": None,
            "Show Both Config": None,
            "Back": None
        }

        self.show_configs_helper = {
            "1": "Show Audio Config",
            "2": "Show Video Config",
            "3": "Show Both Config",
            "4": "Back"
        }

        self.change_audio = {
            "Audio Format": None,
            "Bit Rate": None
        }

        self.change_audio_helper = {
            "1": "Audio Format",
            "2": "Bit Rate"
        }

        with open(CONFIG_PATH_VIDEO, "r") as file:
            self.video_config = json.load(file)

        with open(CONFIG_PATH_AUDIO, "r") as file:
            self.audio_config = json.load(file)


