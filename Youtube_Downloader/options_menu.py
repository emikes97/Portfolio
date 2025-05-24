import json
from pathlib import Path

CONFIG_PATH_AUDIO = Path(__file__).parent / "Active_Configurations" / "audio_only_download.json"
CONFIG_PATH_VIDEO = Path(__file__).parent / "Active_Configurations" / "video_download_mp4.json"
CONFIG_PATH_LOAD_AUDIO = Path(__file__).parent / "Prefab_Json_Configurations" / "audio_only_download.json"
CONFIG_PATH_LOAD_VIDEO = Path(__file__).parent / "Prefab_Json_Configurations" / "video_download_mp4.json"
SAVE_PATH_CONFIG_AUDIO = Path(__file__).parent / "Prefab_Json_Configurations"
SAVE_PATH_CONFIG_VIDEO = Path(__file__).parent / "Prefab_Json_Configurations"

class Options:

    def __init__(self, helper, display_options, request_input, reason_to_pass):
        # Configs
        self.audio_config = None
        self.video_config = None

        # Controllers
        self.runner = True
        self.help = helper

        # Lists
        self.display_options = display_options  # ["DISPLAY_OPT", "DISPLAY_MED"]
        self.request_input = request_input  # ["STRING", "INT"]
        self.reason_to_pass = reason_to_pass  # ["APP_FUNC", "URL", "AUDIO_FORMAT", "INTEGER"]

        # Dictionaries
        self.options_list = {}
        self.show_configs = {}
        self.change_audio = {}
        self.change_video = {}
        self.load_configurations = {}
        self.save_configurations = {}

        # Settings

        # Audio
        self.media_formats = ["MP3", "WAV", "FLAC", "AAC", "OGG"]  # Media Format Options
        self.bit_rate = ["128", "192", "256", "320"] # Quality / Can be used for Video too

        # Video
        self.output_formats = ["mp4", "mkv", "webm"]
        self.audio_codecs = ["aac", "mp3", "opus", "copy"]
        self.video_codecs = ["copy", "libx264", "libx265"]

        # Constructors
        self._dict_constructor()

    def run_options_menu(self):

        while self.runner:

            label = self._get_label(self.options_list, self.options_list)

            match label:

                case "Show Active Configuration (Audio | Video)":
                    self._show_active_config()

                case "Change Audio Configuration":
                    self._change_audio_config()

                case "Change Video Configuration":
                    self._change_video_config()

                case "Load Saved Configuration":
                    self._load_saved_configuration()

                case "Save Active Configuration":
                    self._save_config()

                case "Exit Options":
                    self._exit_options()

    def _show_active_config(self):
        label = self._get_label(self.show_configs, self.show_configs)

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
        changes_happened = False

        while True:

            label = self._get_label(self.change_audio, self.change_audio)

            match label:

                case "Audio Format":
                    self.help.display_to_screen(self.display_options[1], self.media_formats)
                    audio_format = self.media_formats[self.help.retrieve_input(self.request_input[1], self.reason_to_pass[2], self.media_formats)]
                    for processor in self.audio_config.get("postprocessors", []):
                        if processor.get("key") == "FFmpegExtractAudio":
                            processor["preferredcodec"] = audio_format
                    print("Audio Format has been successfully changed")
                    changes_happened = True

                case "Bit Rate":
                    self.help.display_to_screen(self.display_options[1], self.bit_rate)
                    bit_rate_change = self.bit_rate[self.help.retrieve_input(self.request_input[1], self.reason_to_pass[2], self.bit_rate)]
                    for processor in self.audio_config.get("postprocessors", []):
                        if processor.get("key") == "FFmpegExtractAudio":
                            processor["preferredquality"] = bit_rate_change
                    print("Bit Rate has been successfully changed")
                    changes_happened = True

                case "Back":
                    self._changes_happened(changes_happened)
                    return

    def _change_video_config(self):
        changes_happened = False

        while True:

            label = self._get_label(self.change_video, self.change_video)

            match label:

                case "Audio Bit Rate":
                    self.help.display_to_screen(self.display_options[1], self.bit_rate)
                    audio_format = self.bit_rate[self.help.retrieve_input(self.request_input[1], self.reason_to_pass[2], self.bit_rate)]
                    for arg in self.video_config.get("postprocessor_args", {}).get("ffmpeg", []):
                        if "-b:a" in arg:
                            index = self.video_config["postprocessor_args"]["ffmpeg"].index("-c:a")
                            self.video_config["postprocessor_args"]["ffmpeg"][index+1] = audio_format
                    print("Audio Format has been successfully changed")
                    changes_happened = True

                case "Merge Format":
                    self.help.display_to_screen(self.display_options[1], self.output_formats)
                    merge_format = self.output_formats[self.help.retrieve_input(self.request_input[1], self.reason_to_pass[2], self.media_formats)]
                    self.video_config["merge_output_format"] = merge_format
                    print("Merge Format has been successfully changed")
                    changes_happened = True

                case "Audio Codec":
                    self.help.display_to_screen(self.display_options[1], self.audio_codecs)
                    aud_codex = self.output_formats[self.help.retrieve_input(self.request_input[1], self.reason_to_pass[2], self.audio_codecs)]
                    for arg in self.video_config.get("postprocessor_args", {}).get("ffmpeg", []):
                        if "-c:a" in arg:
                            index = self.video_config["postprocessor_args"]["ffmpeg"].index("-c:a")
                            self.video_config["postprocessor_args"]["ffmpeg"][index+1] = aud_codex
                    print("Audio Codec has been successfully changed")
                    changes_happened = True

                case "Video Codec":
                    self.help.display_to_screen(self.display_options[1], self.video_codecs)
                    vid_codex = self.output_formats[self.help.retrieve_input(self.request_input[1], self.reason_to_pass[2], self.video_codecs)]
                    for arg in self.video_config.get("postprocessor_args", {}).get("ffmpeg", []):
                        if "-c:v" in arg:
                            index = self.video_config["postprocessor_args"]["ffmpeg"].index("-c:v")
                            self.video_config["postprocessor_args"]["ffmpeg"][index+1] = vid_codex
                    print("Video Codec has been successfully changed")
                    changes_happened = True

                case "Back":
                    self._changes_happened(changes_happened)
                    return


    def _load_saved_configuration(self):

        while True:

            label = self._get_label(self.load_configurations, self.load_configurations)

            match label:

                case "Load Audio":

                    with open(CONFIG_PATH_LOAD_AUDIO, "r") as file:
                        self.audio_config = json.load(file)

                case "Load Video":

                    with open(CONFIG_PATH_LOAD_VIDEO, "r") as file:
                        self.video_config = json.load(file)

                case "Back":
                    return

            self._changes_happened(True)
            return

    def _save_config(self):
        try:

            with open(CONFIG_PATH_AUDIO, "w", encoding="utf-8") as file:
                json.dump(self.audio_config, file, indent=4)

            with open(CONFIG_PATH_VIDEO, "w", encoding="utf-8") as file:
                json.dump(self.video_config, file, indent=4)

            print("[INFO] Active Configurations have been saved successfully.")

        except Exception as e:
            print(f"[ERROR]: Failed to save configurations: {e}")

    def _exit_options(self):
        self.runner = False
        return

    def _changes_happened(self, changes):
        print("Do you wish to save? Unsaved changes won't carry over to the active options")
        if changes:
            label = self._get_label(self.save_configurations, self.save_configurations)

            match label:

                case "Yes":
                    self._save_config()
                    changes_happened = False
                    return

                case "No":
                    print("[INFO] Unsaved changed remain, if you don't save your changes won't carry over.")
                    return
        else:
            return

    def _get_label(self, list_to_pass, helper):
        self.help.display_to_screen(self.display_options[0], list_to_pass)  # Display the Options of the APP
        choice = self.help.retrieve_input(self.request_input[0], self.reason_to_pass[0],list_to_pass)  # Retrieve the Option
        label = self.help.user_choices(choice, helper)  # Retrieve the label for the function
        return label

    def _dict_constructor(self):
        """"""

        self.options_list = {
            "1": {"label": "Show Active Configuration (Audio | Video)",
                  "action": self._show_active_config},
            "2": {"label": "Change Audio Configuration",
                  "action": self._change_audio_config},
            "3": {"label": "Change Video Configuration",
                  "action": self._change_video_config},
            "4": {"label": "Load Saved Configuration",
                  "action": self._load_saved_configuration},
            "5": {"label": "Save Active Configuration",
                  "action": self._save_config},
            "6": {"label": "Exit Options",
                  "action": self._exit_options}
        }

        self.show_configs = {
            "1": {"label": "Show Audio Config",
                  "action": None},
            "2": {"label": "Show Video Config",
                  "action": None},
            "3": {"label": "Show Both Config",
                  "action": None},
            "4": {"label": "Back",
                  "action": None}
        }

        self.change_audio = {
            "1": {"label": "Audio Format",
                  "action": None},
            "2": {"label": "Bit Rate",
                  "action": None},
            "3": {"label": "Back",
                  "action": None}
        }

        self.change_video = {
            "1": {"label": "Audio Bit Rate",
                  "action": None},
            "2": {"label": "Merge Format",
                  "action": None},
            "3": {"label": "Audio Codec",
                  "action": None},
            "4": {"label": "Video Codec",
                  "action": None},
            "5": {"label": "Back",
                  "action": None}
        }

        self.load_configurations = {
            "1": {"label": "Load Audio",
                  "action": None},
            "2": {"label": "Load Video",
                  "action": None},
            "3": {"label": "Back",
                  "action": None}
        }

        self.save_configurations = {
            "1": {"label": "Yes",
                  "action": None},
            "2": {"label": "No",
                  "action": None}
        }

        with open(CONFIG_PATH_VIDEO, "r") as file:
            self.video_config = json.load(file)

        with open(CONFIG_PATH_AUDIO, "r") as file:
            self.audio_config = json.load(file)


