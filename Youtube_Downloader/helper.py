from pathlib import Path
import sys

class Helper:

    @staticmethod
    def user_choices(user_input, dict_to_check):
        """Returns the label of the action we want to take, in case it doesn't exist it will return None
           If it's None, always verify how you have structured your dict keys, a check shouldn't be needed for this
           method."""
        return dict_to_check.get(user_input, {}).get("label", None)

    @staticmethod
    def display_to_screen(display_type, data_list):
        """
           A helper to display your different options
           1) DISPLAY_OPT
           2) DISPLAY_MED
        """
        options = ["DISPLAY_OPT", "DISPLAY_MED"]

        display = ""  # A variable to store anything we need to be shown to the user

        match display_type:

            case "DISPLAY_OPT":
                for key, value in data_list.items():
                    display += f"{key}) {value.get('label', '[WARN] Unknown Label')}\n"

            case "DISPLAY_MED":
                for i, media_format in enumerate(data_list):
                    display += f"{i + 1}) {media_format} \n"

            case _:
                raise ValueError("The Display Option you have provided isn't correct.")

        print(display)

    @staticmethod
    def get_resource_path(relative_path: str) -> Path:
        """Return absolute path to resource, whether running as script or bundled by PyInstaller."""
        if hasattr(sys, '_MEIPASS'):
            return Path(sys._MEIPASS) / relative_path
        return Path(__file__).parent / relative_path
