import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QComboBox, QHeaderView
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from modules.database import get_connection
import datetime

class ExpenseModule(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        input_layout = QHBoxLayout()
        self.cat_combo = QComboBox()
        self.cat_combo.addItems(["Продукты", "ЖКХ / Аренда", "Транспорт", "Развлечения", "Здоровье", "Другое"])
        self.amount_input = QLineEdit(placeholderText="Сумма (руб.)")
        add_btn = QPushButton("Добавить расход")
        add_btn.clicked.connect(self.add_expense)
        
        input_layout.addWidget(self.cat_combo)
        input_layout.addWidget(self.amount_input)
        input_layout.addWidget(add_btn)
        left_layout.addLayout(input_layout)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Дата", "Категория", "Сумма (руб.)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        left_layout.addWidget(self.table)

        self.total_label = QLabel("Итого расходов: 0 руб.")
        left_layout.addWidget(self.total_label)
        
        clear_btn = QPushButton("Очистить историю")
        clear_btn.clicked.connect(self.clear_history)
        left_layout.addWidget(clear_btn)
        
        main_layout.addWidget(left_panel, stretch=2)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        main_layout.addWidget(self.canvas, stretch=2)

    def add_expense(self):
        category = self.cat_combo.currentText()
        amount = self.amount_input.text()
        date_str = datetime.date.today().strftime("%Y-%m-%d")
        if amount.replace('.', '', 1).isdigit():
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)", (category, float(amount), date_str))
            conn.commit()
            conn.close()
            self.amount_input.clear()
            self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT date, category, amount FROM expenses ORDER BY id DESC")
        rows = cursor.fetchall()
        total = 0
        categories_data = {}
        for row_idx, row in enumerate(rows):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(row[1])))
            self.table.setItem(row_idx, 2, QTableWidgetItem(f"{row[2]:.2f}"))
            total += row[2]
            categories_data[row[1]] = categories_data.get(row[1], 0) + row[2]
        conn.close()
        self.total_label.setText(f"Итого расходов: {total:.2f} руб.")
        self.update_chart(categories_data)

    def update_chart(self, data):
        self.fig.clear()
        if not data:
            self.canvas.draw()
            return
        ax = self.fig.add_subplot(111)
        self.fig.patch.set_facecolor('#2b2b2b')
        ax.set_facecolor('#2b2b2b')
        labels = list(data.keys())
        sizes = list(data.values())
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'color': 'white'})
        ax.axis('equal')
        self.canvas.draw()

    def clear_history(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses")
        conn.commit()
        conn.close()
        self.load_data()
