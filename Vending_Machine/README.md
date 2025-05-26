# 🥤 Vending Machine Simulator (CLI)

> “Why buy chips from a real vending machine when you can simulate existential hunger in your terminal?”


A modular, object-oriented Vending Machine Simulator implemented as a command-line interface (CLI) application in Python. The simulator provides an interactive experience, 
handling product selection, inventory management, and payment processing, mimicking the behavior of a real-world vending machine.

---

## 🚀 Features

- **Interactive CLI Interface:** User-friendly prompts and messages guide the user through product selection and purchasing.
- **Product Inventory Management:** Dynamic management of products including categories, availability checks, and stock updates.
- **Modular Payment System:** Handles payment methods, calculates totals, verifies payments, and manages change.
- **Persistent Data Handling:** Uses structured storage mechanisms to maintain consistent product and pricing data.

---

## ⚙️ Technologies Used

- Python 3.10+
- Object-Oriented Programming (OOP) principles

---

## 📦 Dependencies

- This project uses only Python's standard library. No external packages are required.

---

## 📁 Project Structure

```
Vending_Machine/
├── data/                         # Core data for items, stock, and pricing
│   ├── vm_data_item_list.json
│   ├── vm_data_item_price_list.json
│   ├── vm_stock_in_machine_list.json
│   └── vm_backup_stock.json
│
├── data_bank/                   # Bank file and transaction logs
│   ├── bank_file.json
│   └── transaction_log.txt
│
├── payment_handler/             # All payment-related logic
│   ├── core/
│   │   ├── payment_manager.py
│   │   ├── payment_method.py
│   │   ├── payment_process.py
│   │   └── payment_session.py
│   │
│   ├── helpers/
│   │   ├── denominations.py
│   │   ├── pricing.py
│   │   └── refund.py
│   │
│   └── persistence/
│       ├── update_bank_file.py
│       └── update_transaction_log.py
│
├── storage/
│   └── vending_machine_storage.py
│
├── ui/
│   └── vending_text_manager.py
│
├── main.py                      # Entry point
├── vending_machine.py          # Main application class
└── .gitignore
```
---

# Example Photos:

![image](https://github.com/user-attachments/assets/d89d3468-6f6a-4cf9-b25f-81b709a12f41)

![image](https://github.com/user-attachments/assets/1ce51bb9-956c-480f-a982-e8c1d8351c98)



