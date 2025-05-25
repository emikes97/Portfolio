from Vending_Machine.payment_handler.helpers.pricing import ProductPrice as Price
from Vending_Machine.payment_handler.helpers.refund import RefundCustomer as Refund
from Vending_Machine.payment_handler.core.payment_session import PaymentSession
from Vending_Machine.payment_handler.core.payment_process import PaymentProcess
from Vending_Machine.payment_handler.core.payment_method import PaymentMethod
from Vending_Machine.payment_handler.persistence.update_bank_file import BankUpdate
from Vending_Machine.payment_handler.persistence.update_transaction_log import TransactionLog

class VMPaymentManager:
    def __init__(self, vmtext):
        # Helpers
        self.price = Price()
        self.vmtext = vmtext
        self.payment_method = PaymentMethod(vmtext)
        self.bank = BankUpdate()
        self.log = TransactionLog()

    def payment(self, product_price, product):
        payment_method = self.payment_method.choose_how_to_pay()
        session = PaymentSession(product_price=product_price, payment_method=payment_method)
        total, payed = session.collect_payment()
        success, used_amount, total_given, bank_cash = PaymentProcess(total, payed, product_price).process_payment()
        if success:
            Refund.process(total_given, product_price)
            self.bank.update_data_bank(bank_cash)
            self.log.log_transaction(product, product_price)
            # Notify Purchase On or Off settings.
            return success
        else:
            Refund.process(total_given, product_price, failed=True)
            print("Payment failed, aborting the process.")
            return success

    def return_cost(self, category, item):
        """Checks and returns the price of the chosen product"""

        return self.price.return_price(category, item)




