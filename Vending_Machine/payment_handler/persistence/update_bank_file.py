import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JSON_BANK_FILE = os.path.join(BASE_DIR, "data_bank", "bank_file.json")

class BankUpdate:

    def __init__(self):
        print("🏁 BankUpdate initialized.")
        self.data_bank = {}

        self.load_data_bank()


    def update_data_bank(self, bank_data):
        for key in ["coins", "bills"]:
            for denomination, amount in self.data_bank[key].items():
                bank_data[key][denomination] += amount

        bank_data["total-money"] += self.data_bank["total-money"]

        with open(JSON_BANK_FILE, "w") as file:
            json.dump(bank_data, file, indent=2)

    def load_data_bank(self):
        """A method to load the required files for the VM to be able to process and log the payments"""
        try:
            print("📂 Attempting to open bank_file.json at:", JSON_BANK_FILE)
            with open(JSON_BANK_FILE, "r") as file:
                print("📂 Attempting to open bank_file.json at:", JSON_BANK_FILE)
                self.data_bank = json.load(file)
        except FileNotFoundError:
            # send an alert, stop the machine from working.
            print("❌ Terminating the VM. Critical error: bank file missing.")
            sys.exit()
