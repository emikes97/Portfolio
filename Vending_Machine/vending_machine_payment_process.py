import os, json
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_BANK_FILE = os.path.join(BASE_DIR, "data_bank", "bank_file.json")
JSON_PURCHASE_LOG_FILE = os.path.join(BASE_DIR, "data_bank", "purchase_log_file.json")
JSON_ITEM_PRICE = os.path.join(BASE_DIR, "data", "vm_data_item_price_list.json")


class VMPaymentProcess:

    def __init__(self):
        self.data_bank = {}
        self.price_list = {}
        self.purchase_log = []
        self.load_data()

    def load_data(self):
        """A method to load the required files for the VM to be able to process and log the payments"""

        try:
            with open(JSON_BANK_FILE, "r") as file:
                self.data_bank = json.load(file)
        except FileNotFoundError:
            # send an alert, stop the machine from working.
            print("❌ Terminating the VM. Critical error: bank file missing.")
            sys.exit()

        try:
            with open(JSON_ITEM_PRICE, "r") as file:
                self.price_list = json.load(file)
        except FileNotFoundError:
            # send an alert, stop the machine from working.
            print("❌ Terminating the VM. Critical error: bank file missing.")
            sys.exit()

        try:
            with open(JSON_PURCHASE_LOG_FILE, "r") as file:
                self.purchase_log = json.load(file)
        except FileNotFoundError:
            # send an alert, stop the machine from working.
            self.purchase_log = []
            with open(JSON_PURCHASE_LOG_FILE, "w") as file:
                json.dump(self.purchase_log, file, indent=4)
            print("⚠️ Purchase log was missing. A new one has been created.")

    def check_price(self, category, item):
        """Checks and returns the price of the chosen product"""

        return self.price_list[category][item]

    def payment(self, method_of_payment):
        continue_choice = {
            "yes": True,
            "no": False
        }

        payment_method, payment_messages = type(self).get_payment_method(method_of_payment)
        paying = True
        payed = {}

        while paying:
            pay = input(payment_messages["type"])
            if pay in payment_method:

                pay = payment_method[pay]

                try:
                    quantity = int(input(payment_messages["quantity"]))
                except ValueError:
                    return payed, 0

                if pay not in payed:
                    payed[pay] = quantity
                else:
                    payed[pay] += quantity

            while True:
                to_continue = input("Do you wish to continue? Type: 'yes' or 'no'").lower().strip()
                if to_continue in ["yes", "no"]:
                    if continue_choice[to_continue]:
                        break
                    else:
                        total = 0
                        
                        for key in payed:
                            denomination_value = type(self).get_denomination_value(key)
                            total += denomination_value * payed[key]

                        return payed, total
                else:
                    print("⚠️ Invalid input. Please type 'yes' or 'no'.")

    def check_customer_payment(self, total, payment, price_check):
        """Checks the payment of the customer as a dictionary format, if it fails refund all the money, if it doesn't
        check how much
        should be refunded and process the payment.
        1) total = max amount paid
        2) payment = a dict of all coins/bills used.
        3) price_check = the price of the item or items"""

        if total > price_check:
            payment_completed = self.payment_process(total, payment, price_check)
            return payment_completed
        else:
            self.refund_customer(total, refund=True)

    def payment_process(self, total, payment, price_check):
        """Processes the successful payment, then call refund_customer if needed for the extra cash.
        Also calls update_bank_file, log_purchase and notify_purchase for a successful payment."""
        amount_used = 0
        total_given = 0

        for key, count in payment.items():
            key_value = type(self).get_denomination_value(key)

            for _ in range(count):

                total_given += key_value

                if amount_used >= price_check:
                    continue  # Accept money but don't process it (it will be refunded)

                if key in self.data_bank["coins"]:
                    self.data_bank["coins"][key] += 1
                else:
                    self.data_bank["bills"][key] += 1

                amount_used += key_value

        if amount_used >= price_check:
            money_to_refund = round(total_given - price_check, 2)
            if money_to_refund > 0:
                type(self).refund_customer(money_to_refund)

            self.update_bank_file()
            self.update_log_purchase()
            self.notify_purchase()
            return True
        else:
            type(self).refund_customer(total_given, refund=True)
            return False

    def update_bank_file(self):
        """Updates the json file that keeps track of how much money is inside the  machine"""
        pass

    def update_log_purchase(self):
        """Updates the json file of when the purchase happened, and what item was brought for second verification for
        the purchase / cash at hand at the machine"""
        pass

    def notify_purchase(self):
        """Notifies the owner of the purchase made"""
        pass

    @staticmethod
    def get_denomination_value(key):
        """A helper function for payment process"""
        values = {
            "half-euro": 0.5,
            "euro": 1.0,
            "two-euro": 2.0,
            "five-euro-bill": 5.0,
            "ten-euro-bill": 10.0,
        }

        return values.get(key,0)

    @staticmethod
    def refund_customer(money_to_refund, refund=False):
        """Method should be called to refund the customer for excessive cash input or for a failed purchase in case the
        provided cash is less than the required amount"""
        if not refund:
            print(f"Kindly take your {money_to_refund} back from the machine.")
        else:
            print(f"Kindly take your {money_to_refund} back from the machine."
                  f"The payment failed due to the money provided being less than the required amount.")
            # Ejects the money back to the customer if a real VM was used.

    @staticmethod
    def get_payment_method(method_of_payment):
        """A helper function to retrieve the payment method and text"""
        coins_payment = {
            "1": "half-euro",
            "2": "euro",
            "3": "two-euro"
        }
        coins_messages = {
            "type": "Type: '1': Half-Euro, '2' Euro, '3' Two-Euro\n",
            "quantity": "Provide the quantity: "
        }

        bills_payment = {
            "1": "five-euro-bill",
            "2": "ten-euro-bill"
        }

        bills_messages = {
            "type": "Type: '1': Five-euro-bill, '2': Ten-euro-bill\n",
            "quantity": "Provide the quantity: "
        }

        if method_of_payment == "coins":
            return coins_payment, coins_messages
        else:
            return bills_payment, bills_messages
