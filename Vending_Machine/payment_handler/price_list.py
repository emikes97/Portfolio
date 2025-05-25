import os, json, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_ITEM_PRICE = os.path.join(BASE_DIR, "data", "vm_data_item_price_list.json")

class ProductPrice:

    def __init__(self):
        self.price_list = {}


    def load_data(self):
        """A method to load the required files for the VM to be able to process and log the payments"""

        try:
            with open(JSON_ITEM_PRICE, "r") as file:
                self.price_list = json.load(file)
        except FileNotFoundError:
            # send an alert, stop the machine from working.
            print("❌ Terminating the VM. Critical error: bank file missing.")
            sys.exit()

    def return_price(self, category, item):
        """Checks and returns the price of the chosen product"""

        return self.price_list[category][item]