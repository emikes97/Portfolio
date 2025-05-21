import json
from pathlib import Path

CONFIG_PATH_AUDIO = Path(__file__).parent / "Active_Configurations" / "audio_only_download.json"
CONFIG_PATH_VIDEO = Path(__file__).parent / "Active_Configurations" / "video_download_mp4.json"
SAVE_PATH_CONFIG_AUDIO = Path(__file__).parent / "Prefab_Json_Configurations"
SAVE_PATH_CONFIG_VIDEO = Path(__file__).parent / "Prefab_Json_Configurations"

class Options:

    def __init__(self, helper):
        # Controllers
        self.runner = True
        self.help = helper

        # Dictionaries
        self.options_list = {}
        self.options_list_helper = {}

        #constructors
        self._dict_constructor()

    def run_options_menu(self):

        while self.runner:

            label = self._get_label()

            match label:

                case "Show Active Configuration (Audio | Video)":
                    pass

                case "Change Audio Configuration":
                    pass

                case "Change Video Configuration":
                    pass

                case "Load Saved Configuration":
                    pass

                case "Save Active Configuration":
                    pass

                case "Exit Options":
                    pass
    def _show_active_config(self):
        pass

    def _change_audio_config(self):
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

    def _get_label(self):
        self.help.display_to_screen(self.display_options[0], self.options_list)  # Display the Options of the APP
        choice = self.help.retrieve_input(self.request_input[0], self.reason_to_pass[0],self.options_list)  # Retrieve the Option
        label = self.help.user_choices(choice, self.program_choices_helper)  # Retrieve the label for the function
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

