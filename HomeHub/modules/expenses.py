import json
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel

class ExpenseModule(QWidget):
    def __init__(self):
        super().__init__()
        self.db_file = "expenses.json"
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Форма ввода
        input_layout = QHBoxLayout()
        self.item_input = QLineEdit(placeholderText="На что потрачено?")
        self.amount_input = QLineEdit(placeholderText="Сумма (руб.)")
        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.add_expense)
        
        input_layout.addWidget(self.item_input)
        input_layout.addWidget(self.amount_input)
        input_layout.addWidget(add_btn)
        layout.addLayout(input_layout)

        # Таблица
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Предмет/Услуга", "Сумма"])
        layout.addWidget(self.table)

        # Итого
        self.total_label = QLabel("Всего потрачено: 0 руб.")
        layout.addWidget(self.total_label)

    def add_expense(self):
        item = self.item_input.text()
        amount = self.amount_input.text()
        if item and amount.isdigit():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(item))
            self.table.setItem(row, 1, QTableWidgetItem(amount))
            self.item_input.clear()
            self.amount_input.clear()
            self.save_data()
            self.update_total()

    def update_total(self):
        total = 0
        for row in range(self.table.rowCount()):
            total += int(self.table.item(row, 1).text())
        self.total_label.setText(f"Всего потрачено: {total} руб.")

    def save_data(self):
        data = []
        for row in range(self.table.rowCount()):
            data.append({
                "item": self.table.item(row, 0).text(),
                "amount": self.table.item(row, 1).text()
            })
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for entry in data:
                        row = self.table.rowCount()
                        self.table.insertRow(row)
                        self.table.setItem(row, 0, QTableWidgetItem(entry["item"]))
                        self.table.setItem(row, 1, QTableWidgetItem(entry["amount"]))
                self.update_total()
            except Exception:
                pass
