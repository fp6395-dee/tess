import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QComboBox
from PyQt6.QtCore import Qt
from modules.database import get_connection

class TodoModule(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout(self)
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit(placeholderText="Введите бытовую задачу...")
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["🔥 Срочно", "⚡ Важно", "💤 Рутина"])
        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.add_task)
        input_layout.addWidget(self.task_input, stretch=3)
        input_layout.addWidget(self.priority_combo, stretch=1)
        input_layout.addWidget(add_btn, stretch=1)
        layout.addLayout(input_layout)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        done_btn = QPushButton("Выполнено / Снять отметку")
        done_btn.clicked.connect(self.toggle_task)
        del_btn = QPushButton("🗑 Удалить задачу")
        del_btn.clicked.connect(self.delete_task)
        btn_layout.addWidget(done_btn)
        btn_layout.addWidget(del_btn)
        layout.addLayout(btn_layout)

    def add_task(self):
        task = self.task_input.text()
        priority = self.priority_combo.currentText()
        if task:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO todo (task, priority, status) VALUES (?, ?, 0)", (task, priority))
            conn.commit()
            conn.close()
            self.task_input.clear()
            self.load_data()

    def toggle_task(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            task_id = current_item.data(Qt.ItemDataRole.UserRole)
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT status FROM todo WHERE id = ?", (task_id,))
            res = cursor.fetchone()
            if res is not None:
                new_status = 1 if res[0] == 0 else 0
                cursor.execute("UPDATE todo SET status = ? WHERE id = ?", (new_status, task_id))
                conn.commit()
            conn.close()
            self.load_data()

    def delete_task(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            task_id = current_item.data(Qt.ItemDataRole.UserRole)
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM todo WHERE id = ?", (task_id,))
            conn.commit()
            conn.close()
            self.load_data()

    def load_data(self):
        self.list_widget.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, task, priority, status FROM todo ORDER BY status ASC, id DESC")
        rows = cursor.fetchall()
        for row in rows:
            task_id, task, priority, status = row
            display_text = f"[{priority}] {task}"
            if status == 1:
                display_text += "  ✓ (Выполнено)"
            item = QListWidgetItem(display_text)
            item.setData(Qt.ItemDataRole.UserRole, task_id)
            if status == 1:
                item.setForeground(Qt.GlobalColor.gray)
            self.list_widget.addItem(item)
        conn.close()
