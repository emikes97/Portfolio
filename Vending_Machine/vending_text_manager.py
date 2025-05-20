class VendingTextManager:

    def __init__(self, vmstorage):
        """Initializes the needed variables and instantiates the vending machine storage to get a hold of the menu"""
        self.vms = vmstorage
        self.text_bank = {}
        self.text_bank_creator()

    def text_bank_creator(self):
        """Creates the text_bank, so we can provide all messages without the need to write each one individually"""
        self.text_bank = {
            "starting_message": "☕🍫 Welcome! Initializing #VendingMachine...\n"
                                "Loading inventory, checking stocks, and preparing tasty treats.\n"
                                "Please wait...\n",
            "menu": f"Kindly choose one from:\n{', '.join(self.vms.return_available_categories())}\n",
            "coffee": f"Kindly choose of from:\n{', '.join(self.vms.return_available_items('coffee'))}\n",
            "soda": f"Kindly choose of from:\n{', '.join(self.vms.return_available_items('soda'))}\n",
            "chips": f"Kindly choose of from:\n{', '.join(self.vms.return_available_items('chips'))}\n",
            "chocolate": f"Kindly choose of from:\n{', '.join(self.vms.return_available_items('chocolate'))}\n",
            "price": "The cost of your {item} is {price}",
            "payment": "Choose, with what you will pay. Type 1 for 'Coins', 2 for 'Bills'",
            "payment2": "The price of the item you chose is {price}",
            "alert_1": "Sorry there has been an issue to the Vending Machine, the maintenance team has been notified.",
            "alert_2": "Sorry but the {item}, is not available currently.",
            "alert_3": "Sorry your input was wrong. The {item} doesn't exist.",
            "alert_4": "Sorry your input was wrong. The Category {category} doesn't exist.",
            "alert_5": "Sorry your input was wrong. Kindly choose 1 or 2."
        }

    def print_message(self, word, **kwargs):
        if word in self.text_bank.keys():
            print(self.text_bank[word].format(**kwargs))
        else:
            print(f"⚠️ Warning: Message key '{word}' not found.")
