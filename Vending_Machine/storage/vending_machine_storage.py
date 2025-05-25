import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_STOCK = os.path.join(BASE_DIR, "data", "vm_stock_in_machine_list.json")
JSON_DATA_ITEM_LIST = os.path.join(BASE_DIR, "data", "vm_data_item_list.json")
JSON_BACKUP_STOCK = os.path.join(BASE_DIR, "data", "vm_backup_stock.json")

class VendingMachineStorage:

    def __init__(self):
        self.categories = []
        self.item_list = {}
        self.stock_available = {}
        self.backup_stock = {}
        self.load_data()

        print(self.backup_stock)
        print(self.stock_available)
        print(self.item_list)
        print(self.categories)

    def load_data(self):

        try:
            with open(JSON_DATA_ITEM_LIST, "r") as file:
                self.item_list = json.load(file)
                self.categories = list(self.item_list.keys())
        except FileNotFoundError:
            # send an alert via api to inform about this.
            print("Sorry there has been an issue with the Vending Machine, the maintenance team has been notified.")

        try:
            with open(JSON_STOCK, "r") as file:
                self.stock_available = json.load(file)
        except FileNotFoundError:
            # send an alert via api to inform about this
            print("Sorry there has been an issue with the Vending Machine, the maintenance team has been notified.")

        try:
            with open(JSON_BACKUP_STOCK, "r") as file:
                self.backup_stock = json.load(file)
        except FileNotFoundError:
            # send an alert via api to inform about this
            self.backup_stock = {}  # Empty list, Machine can operate, but it will lead to problems if stock depletes.

    def is_available(self, category, choice):
        """Returns True if the choice of the customer is available to be taken or False if it's not.
           If the first check fails, automatic restock will be called before failing the order
        """
        if category == "coffee":
            required_ingredients = self.item_list.get("coffee", {}).get(choice,{})
            for ingredient, amount_required in required_ingredients.items():
                available_amount = self.stock_available["stock"].get(ingredient,0)
                if amount_required > available_amount:
                    self.restock_machine(ingredient=ingredient, required_amount=amount_required)
                    if amount_required > available_amount:
                        return False
            return True
        else:
            return self.stock_available["stock"].get(choice, 0) >= 1

    def update_storage(self):
        """If a successful order has been processed and payment confirm, then the deducted amount from local-memory,
           will be saved into the json file to ensure local memory and json are the same."""
        with open(JSON_STOCK, "w") as file:
            json.dump(self.stock_available, file, indent=4)
        print("The internal memory has been updated")

    def update_backup_storage(self):
        """After a successful refill from backup then we have to update the backup storage json file to ensure no data
           loss"""
        with open(JSON_BACKUP_STOCK, "w") as file:
            json.dump(self.backup_stock, file, indent=2)

    def restock_machine(self, ingredient, required_amount):
        """Attempts automatic restock if check_availability fails.
        If restock fails, sends an alert to the owner."""
        available_backup = self.backup_stock.get("stock", {}).get(ingredient, 0)
        missing_amount = required_amount - self.stock_available.get("stock",{}).get(ingredient, 0)
        amount_to_transfer = min(missing_amount, available_backup)

        if amount_to_transfer > 0:
            self.stock_available["stock"][ingredient] += amount_to_transfer
            self.backup_stock["stock"][ingredient] -= amount_to_transfer

            self.update_storage()
            self.update_backup_storage()
        else:
            # send an alert to inform that backup storage has dried out for the ingredient
            print("No available backup")

    def return_available_categories(self):
        """A Class method to return all the available choices aka
        1) coffee
        2) soda
        3) chips
        4) chocolate
        etc"""
        return self.categories

    def return_available_items(self, list_choice):
        """A static method to return all available items available in the respective choice
        coffee choices, brands of sodas or available chips etc"""
        return self.item_list[list_choice]
