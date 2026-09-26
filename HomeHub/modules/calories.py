import json
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel

class CalorieModule(QWidget):
    def __init__(self):
        super().__init__()
        self.db_file = "calories.json"
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)

        input_layout = QHBoxLayout()
        self.food_input = QLineEdit(placeholderText="Блюдо/Продукт")
        self.cal_input = QLineEdit(placeholderText="Калории")
        add_btn = QPushButton("Записать")
        add_btn.clicked.connect(self.add_entry)
        
        input_layout.addWidget(self.food_input)
        input_layout.addWidget(self.cal_input)
        input_layout.addWidget(add_btn)
        layout.addLayout(input_layout)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        self.summary_label = QLabel("Всего калорий за день: 0 ккал")
        layout.addWidget(self.summary_label)

    def add_entry(self):
        food = self.food_input.text()
        cal = self.cal_input.text()
        if food and cal.isdigit():
            self.log_area.append(f"{food} — {cal} ккал")
            self.food_input.clear()
            self.cal_input.clear()
            self.save_data()
            self.update_summary()

    def update_summary(self):
        lines = self.log_area.toPlainText().split('\n')
        total = 0
        for line in lines:
            if "—" in line and "ккал" in line:
                try:
                    parts = line.split("—")
                    cal_part = parts[1].replace("ккал", "").strip()
                    total += int(cal_part)
                except Exception:
                    pass
        self.summary_label.setText(f"Всего калорий за день: {total} ккал")

    def save_data(self):
        text = self.log_area.toPlainText()
        with open(self.db_file, "w", encoding="utf-8") as f:
            f.write(text)

    def load_data(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r", encoding="utf-8") as f:
                    text = f.read()
                    self.log_area.setText(text)
                self.update_summary()
            except Exception:
                pass
