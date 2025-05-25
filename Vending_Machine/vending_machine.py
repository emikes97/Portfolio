from vending_machine_storage import VendingMachineStorage
from vending_text_manager import VendingTextManager
from vending_machine_payment_process import VMPaymentProcess

class VendingMachine:

    def __init__(self):
        self.vmstorage = VendingMachineStorage()
        self.vmtext = VendingTextManager(vmstorage=self.vmstorage)
        self.vmpayment = VMPaymentProcess()
        self.vending_machine_on = None
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
                product_price = self.vmpayment.check_price(category,product)
                self.vmtext.print_message("payment2", price=product_price)
                method_of_payment = self.choose_how_to_pay()
                payed, total = self.vmpayment.payment(method_of_payment)
                successful = self.vmpayment.check_customer_payment(total=total, payment=payed, price_check=product_price)
                if successful:
                    print(f"Kindly take your {product}")
                else:
                    print(f"Payment Failed")
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

    def choose_how_to_pay(self):
        """A helper function to choose the payment method for the user."""

        payment_method = {
            "1": "coins",
            "2": "bills",
        }

        self.vmtext.print_message("payment")
        while True:
            choice = input("Choose: ")
            if choice in payment_method:
                return payment_method[choice]
            else:
                self.vmtext.print_message("alert5")




