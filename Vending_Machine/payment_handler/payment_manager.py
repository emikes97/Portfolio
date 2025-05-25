import os, json
import sys
from pricing import ProductPrice as Price
from refund import RefundCustomer as Refund
from payment_session import PaymentSession
from payment_process import PaymentProcess
from payment_method import PaymentMethod

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_BANK_FILE = os.path.join(BASE_DIR, "data_bank", "bank_file.json")
JSON_PURCHASE_LOG_FILE = os.path.join(BASE_DIR, "data_bank", "purchase_log_file.json")

class VMPaymentProcess:

    def __init__(self, vmtext):
        # Helpers
        self.price = Price()
        self.vmtext = vmtext
        self.payment_method = PaymentMethod(vmtext)

        # Data sets
        self.data_bank = {}
        self.price_list = {}

        # Data lists
        self.purchase_log = []

        # Constructor
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
            with open(JSON_PURCHASE_LOG_FILE, "r") as file:
                self.purchase_log = json.load(file)
        except FileNotFoundError:
            # send an alert, stop the machine from working.
            self.purchase_log = []
            with open(JSON_PURCHASE_LOG_FILE, "w") as file:
                json.dump(self.purchase_log, file, indent=4)
            print("⚠️ Purchase log was missing. A new one has been created.")

    def payment(self, product_price):
        payment_method = self.payment_method.choose_how_to_pay()
        session = PaymentSession(product_price=product_price, payment_method=payment_method)
        total, payed = session.collect_payment()
        used_amount, total_given, bank_cash = PaymentProcess(total, payed, product_price).process_payment()

    def return_cost(self, category, item):
        """Checks and returns the price of the chosen product"""

        return self.price.return_price(category, item)

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


