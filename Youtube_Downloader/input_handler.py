class InputHandler:

    def __init__(self):
        self.count = 0  # Counter for wrong Inputs
        self.threshold = 10  # Threshold for wrong inputs before aborting.

    def retrieve_string(self, data_list=None):

        if data_list is not None:
            data_list_choices = self._produce_choice_list(data_list)

        while True:

            if self.count >= self.threshold:
                self.count = 0
                return  # Abort

            choice = input("Input: ")

            if data_list is None:
                return choice

            if choice in data_list_choices:
                self.count = 0
                return choice
            else:
                print("[WARN] Invalid selection. Choose a valid number from the list")
                self.count += 1

    def retrieve_integer(self, data_list=None):

        if data_list is not None:
            data_list_choices = self._produce_choice_list(data_list)

        while True:

            try:

                if self.count >= self.threshold:
                    self.count = 0
                    return  # Abort

                choice = int(input("Input: "))

                if data_list is None:
                    return choice

                if str(choice) in data_list_choices:
                    return choice - 1
                else:
                    print("[WARN] Invalid selection. Choose a valid number from the list")
                    self.count += 1

            except ValueError:
                print("[WARN] provide only a valid number. Input was not recognized.")
                self.count += 1

    def retrieve_url(self):

        return input("Provide the URL: ").strip()

    def _produce_choice_list(self, data_list):

        if data_list is None:
            raise ValueError("The data set you provided is empty or non-existent")

        return [str(i+1) for i in range(len(data_list))]

