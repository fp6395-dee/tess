import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QProgressBar, QListWidget
from modules.database import get_connection
import datetime

class CalorieModule(QWidget):
    def __init__(self):
        super().__init__()
        self.daily_norm = 2000
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)
        input_layout = QHBoxLayout()
        self.type_selector = QLineEdit(placeholderText="Что сделали? (Например: Завтрак / Бег)")
        self.val_input = QLineEdit(placeholderText="Калории (ккал)")
        add_food_btn = QPushButton("+ Съел")
        add_food_btn.clicked.connect(lambda: self.add_entry("food"))
        add_sport_btn = QPushButton("- Сжег (Спорт)")
        add_sport_btn.clicked.connect(lambda: self.add_entry("sport"))

        input_layout.addWidget(self.type_selector, stretch=2)
        input_layout.addWidget(self.val_input, stretch=1)
        input_layout.addWidget(add_food_btn)
        input_layout.addWidget(add_sport_btn)
        layout.addLayout(input_layout)

        layout.addWidget(QLabel("Журнал активности за сегодня:"))
        self.log_list = QListWidget()
        layout.addWidget(self.log_list)

        layout.addWidget(QLabel("Прогресс выполнения нормы дня (2000 ккал):"))
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(self.daily_norm)
        layout.addWidget(self.progress_bar)

        self.balance_label = QLabel("Текущий баланс: 0 ккал")
        layout.addWidget(self.balance_label)

    def add_entry(self, entry_type):
        name = self.type_selector.text()
        val = self.val_input.text()
        date_str = datetime.date.today().strftime("%Y-%m-%d")
        if name and val.isdigit():
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO health (type, name, value, date) VALUES (?, ?, ?, ?)", (entry_type, name, int(val), date_str))
            conn.commit()
            conn.close()
            self.type_selector.clear()
            self.val_input.clear()
            self.load_data()

    def load_data(self):
        self.log_list.clear()
        date_str = datetime.date.today().strftime("%Y-%m-%d")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT type, name, value FROM health WHERE date = ?", (date_str,))
        rows = cursor.fetchall()
        total_in = 0
        total_out = 0
        for row in rows:
            etype, name, val = row
            if etype == "food":
                total_in += val
                self.log_list.addItem(f"🍏 Еда: {name} (+{val} ккал)")
            else:
                total_out += val
                self.log_list.addItem(f"🏃 Спорт: {name} (-{val} ккал)")
        conn.close()
        net_balance = total_in - total_out
        self.balance_label.setText(f"Получено: {total_in} | Сожжено: {total_out} | Чистый баланс: {net_balance} ккал")
        self.progress_bar.setValue(max(0, min(net_balance, self.daily_norm)))
