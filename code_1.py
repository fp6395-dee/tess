import os

# Структура создаваемого проекта
PROJECT_NAME = "HomeHub"
FILES = {
    # Главный файл запуска
    "main.py": """import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from modules.expenses import ExpenseModule
from modules.todo import TodoModule
from modules.calories import CalorieModule

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Бытовой Органайзер (HomeHub)")
        self.resize(800, 600)

        # Главный виджет и табы
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Подключение модулей
        self.tab_widget.addTab(ExpenseModule(), "💰 Учет расходов")
        self.tab_widget.addTab(TodoModule(), "📝 Список дел")
        self.tab_widget.addTab(CalorieModule(), "🍏 Калории и рецепты")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
""",

    # Модуль расходов
    "modules/expenses.py": """import json
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
""",

    # Модуль списка дел
    "modules/todo.py": """import json
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem

class TodoModule(QWidget):
    def __init__(self):
        super().__init__()
        self.db_file = "todo.json"
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)

        input_layout = QHBoxLayout()
        self.task_input = QLineEdit(placeholderText="Новая задача...")
        add_btn = QPushButton("Добавить задачу")
        add_btn.clicked.connect(self.add_task)
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(add_btn)
        layout.addLayout(input_layout)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        del_btn = QPushButton("Удалить выделенные")
        del_btn.clicked.connect(self.delete_task)
        layout.addWidget(del_btn)

    def add_task(self):
        task = self.task_input.text()
        if task:
            self.list_widget.addItem(task)
            self.task_input.clear()
            self.save_data()

    def delete_task(self):
        for item in self.list_widget.selectedItems():
            self.list_widget.takeItem(self.list_widget.row(item))
        self.save_data()

    def save_data(self):
        tasks = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r", encoding="utf-8") as f:
                    tasks = json.load(f)
                    self.list_widget.addItems(tasks)
            except Exception:
                pass
""",

    # Модуль калорий
    "modules/calories.py": """import json
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
        lines = self.log_area.toPlainText().split('\\n')
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
""",
    # Инициализация пакета
    "modules/__init__.py": ""
}

def generate_project():
    print(f"[*] Начало генерации проекта '{PROJECT_NAME}'...")
    
    # Создаем корневую директорию
    os.makedirs(PROJECT_NAME, exist_ok=True)
    
    for relative_path, content in FILES.items():
        # Полный путь к файлу
        full_path = os.path.join(PROJECT_NAME, relative_path)
        
        # Создаем поддиректории, если они нужны
        dir_name = os.path.dirname(full_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
            
        # Записываем контент файла
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
            
        print(f"[+] Создан файл: {full_path}")
        
    print(f"\\n[!] Проект успешно создан! Перейдите в папку '{PROJECT_NAME}' и запустите 'main.py'.")

if __name__ == "__main__":
    generate_project()
