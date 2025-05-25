import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TXT_TRANSACTION_LOG_FILE = os.path.join(BASE_DIR, "data_bank", "transaction_log.txt")
class TransactionLog:

    def __init__(self):
        self.purchase_log = TXT_TRANSACTION_LOG_FILE

    def log_transaction(self, product, price):
        timestamp = str(datetime.now().timestamp())
        log_entry = f"{timestamp} | {product} | €{price:.2f}\n"

        with open(self.purchase_log, "a") as file:
            file.write(log_entry)

    def read_log(self):
        try:
            with open(self.file_path, "r") as file:
                return file.readlines()
        except FileNotFoundError:
            print("⚠️ Log file not found. Creating one...")
            with open(self.file_path, "w") as file:
                pass
            return []
