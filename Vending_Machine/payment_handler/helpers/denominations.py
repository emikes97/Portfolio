class Denominations:

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

        match method_of_payment:

            case "coins":
                return coins_payment, coins_messages

            case "bills":
                return bills_payment, bills_messages

            case _:
                raise ValueError(f"Unsupported payment method: {method_of_payment}")

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