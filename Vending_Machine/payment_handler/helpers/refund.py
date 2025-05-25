class RefundCustomer:

    @staticmethod
    def process(total, product_price, failed=False):
        """Method should be called to refund the customer for excessive cash input or for a failed purchase in case the
        provided cash is less than the required amount"""

        if failed:
            print(f"⚠️ Transaction failed. Please take back your €{total}.")
            return
        else:
            money_to_refund = round(total - product_price, 2)

            if money_to_refund > 0:
                print(f"💶 Change returned: €{money_to_refund}")
                return
            else:
                return
