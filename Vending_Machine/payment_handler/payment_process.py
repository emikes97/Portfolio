from denominations import Denominations

class PaymentProcess:

    def __init__(self, total_amount, payed_dict, product_price):

        self.total_amount = total_amount
        self.payed_dict = payed_dict
        self.product_price = product_price


    def process_payment(self):

        bank_cash_saved = {
                              "coins": {
                                "half-euro": 0,
                                "euro": 0,
                                "two-euro": 0
                              },
                              "bills": {
                                "five-euro-bill": 0,
                                "ten-euro-bill": 0
                              } }

        amount_used = 0
        total_given = 0

        for key, count in self.payed_dict.items():
            key_value = Denominations.get_denomination_value(key)

            for _ in range(count):

                total_given += key_value

                if amount_used >= self.product_price:
                    continue  # Accept money but don't process it (it will be refunded)

                if key in bank_cash_saved["coins"]:
                    bank_cash_saved["coins"][key] += 1
                else:
                    bank_cash_saved["bills"][key] += 1

                amount_used += key_value

        return amount_used, total_given, bank_cash_saved