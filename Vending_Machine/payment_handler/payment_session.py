from denominations import Denominations

class PaymentSession:

    def __init__(self, product_price, payment_method):
        # Variables
        self.product_price = product_price
        self.payment_method = payment_method

        # Extract type of payment
        self.payment_type, self.payment_messages = Denominations.get_payment_method(payment_method)

        # Collect pay
        self.payed = {}

        # Controller
        self.runner = True

    def collect_payment(self):

        continue_choice = {
            "yes": True,
            "no": False
        }

        payed = {}

        while self.runner:

            pay = input(self.payment_messages["type"])
            if pay in self.payment_method:

                pay = self.payment_type[pay]

                try:
                    quantity = int(input(self.payment_messages["quantity"]))
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
                            denomination_value = Denominations.get_denomination_value(key)
                            total += denomination_value * payed[key]

                        return total, payed
                else:
                    print("⚠️ Invalid input. Please type 'yes' or 'no'.")
