from Vending_Machine.storage.vending_machine_storage import VendingMachineStorage
from Vending_Machine.ui.vending_text_manager import VendingTextManager
from Vending_Machine.payment_handler.core.payment_manager import VMPaymentManager
from Vending_Machine.payment_handler.persistence.update_bank_file import BankUpdate

class VendingMachine:

    def __init__(self):
        print("Vending Machine Initializes")
        self.vmstorage = VendingMachineStorage()
        self.vmtext = VendingTextManager(vmstorage=self.vmstorage)
        self.vending_machine_on = None
        self.vmpayment = VMPaymentManager(self.vmtext)
        self.vending_machine_choices = []

    def run(self):
        self.vmtext.print_message("starting_message")
        self.vending_machine_on = True
        self.vending_machine()

    def vending_machine(self):
        while self.vending_machine_on:
            category, product = self.customer_choice_picker()
            is_available = self.vmstorage.is_available(category, product)
            if is_available:
                product_price = self.vmpayment.return_cost(category,product)
                self.vmtext.print_message("payment2", price=product_price)
                success = self.vmpayment.payment(product_price, product)
                if success:
                    self.vmstorage.decrease_stock(category, product)
                    print(f"Take your {product} from the Vending Machine")
                else:
                    print("Transaction Failed")
            else:
                self.vmtext.print_message("alert_2", item=product)

    def customer_choice_picker(self):
        """A helper function to run at vending_machine to validate and take the input from the user"""
        while True:
            self.vmtext.print_message("menu")
            choice_cat = input("Choose: ").strip().lower()
            if choice_cat in self.vmstorage.return_available_categories():
                self.vmtext.print_message(choice_cat)
                choice_item = input("Choose: ").strip().lower()
                if choice_item in self.vmstorage.return_available_items(choice_cat):
                    return choice_cat, choice_item
                else:
                    self.vmtext.print_message("alert_3", item=choice_item)
            else:
                self.vmtext.print_message("alert_4", category=choice_cat)




