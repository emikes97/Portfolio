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

        reasons = ["APP_FUNC", "URL", "AUDIO_FORMAT", "INTEGER"] # If you want to add more reasons, add them here and also in main script
        request_inputs = ["STRING", "INT"] # If you want more inputs add them here and also in main script for easier use.

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

        if reason in reasons and request_input in request_inputs:
            while counter <= threshold:
                if request_input == request_inputs[0] and reason == reasons[0]:  # String Input # Strict # Return index for function
                    choice = input("Input: ")
                    if choice in data_list_choices:
                        return choice
                    counter += 1
                elif request_input == request_inputs[0] and reason == reasons[1]:  # Return the URL
                    choice = input("Provide the URL: ")
                    return choice
                elif request_input == request_inputs[1] and reason == reasons[2]:  # Return audio format index
                    try:
                        choice = int(input("Provide the audio format: "))
                        if str(choice) in data_list_choices:
                            return choice - 1
                        else:
                            print("[WARN] Invalid selection. Choose a valid number from the list.")
                            counter += 1
                    except ValueError:
                        print("[WARN] Provide only a valid number. Input was not recognized.")
                        counter += 1
                elif request_input == request_inputs[1] and reason == "INTEGER":  # INT Input # Strict
                    try:
                        choice = int(input("Input: "))
                        if isinstance(choice, int):
                            return choice
                    except ValueError:
                        print("Invalid Input, kindly provide an Integer as requested")
                        counter += 1
                else:
                    return None  # Abort download  // Unexpected error // Should fail silently and retry
            print("Maximum retries reached, download will be aborted")
            return None  # Abort download // Threshold reached // fail silently
        else:
            raise ValueError(f"{reason} may not be included in {reasons} or {request_input} may not be included in {request_inputs}")
