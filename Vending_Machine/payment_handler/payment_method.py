class PaymentMethod:

    def __init__(self, vmtext):
        self.vmtext = vmtext

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