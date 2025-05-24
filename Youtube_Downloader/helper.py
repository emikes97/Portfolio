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

    @staticmethod
    def retrieve_input(request_input, reason, data_list=None):
        """
        Request what input the user should add and provide the correct Data list.

        The function is strict with Validations, be careful with your choices as it will raise errors otherwise.

        Ensure the correct variables are in order of whatever action you need so there is a correct handling of data

        Variable 1:
        1) STRING,
        2) INT,

        Variable 2:
        1) APP_FUNC,
        2) URL,
        3) AUDIO_FORMAT
        4) INTEGER

        Variable 3:
        The data list we want to choose from, it's used to validate our inputs as in some cases we want to remove writing,
        and pressing only 1, 2, 3, 4 from the user as string to streamline choosing and have less writing for the CLI version.
        """

        threshold = 5 # Change the threshold if you want more retries before aborting the process.
        counter = 0 # A counter to abort the choosing if exceeds the threshold of failed attempts from the user
        data_list_choices = [] # An empty list to be provided with the intended range of choices

        if data_list is None and reason not in ["URL", "AUDIO_FORMAT", "INTEGER"]:
            raise ValueError("The data set you provided is empty or non-existent")
        else:
            if data_list is None:
                pass
            else:
                for i, _ in enumerate(data_list):
                    data_list_choices.append(str(i + 1))

        while counter < threshold:

            match (request_input, reason):

                case ("STRING", "APP_FUNC"):
                    choice = input("Input: ")
                    if choice in data_list_choices:
                        return choice
                    counter += 1

                case ("STRING", "URL"):
                    return input("Provide the URL: ")

                case ("INT", "AUDIO_FORMAT"):
                    try:
                        choice = int(input("Input: "))
                        if str(choice) in data_list_choices:
                            return choice - 1
                        else:
                            print("[WARN] Invalid selection. Choose a valid number from the list")
                            counter += 1
                    except ValueError:
                        print("[WARN] provide only a valid number. Input was not recognized.")
                        counter += 1

                case ("INT", "INTEGER"):
                    try:
                        return int(input("Input: "))
                    except ValueError:
                        print("[WARN] Invalid Input, kindly provide an Integer as requested")
                        counter += 1

                case _:
                    print("[ERROR] Unmatched reason / Input combo")
                    return None  #Unmatched reason/input combo.