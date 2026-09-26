import json
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
