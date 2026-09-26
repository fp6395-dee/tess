import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QComboBox, QHBoxLayout, QLabel
from modules.database import init_db
from modules.expenses import ExpenseModule
from modules.todo import TodoModule
from modules.calories import CalorieModule

DARK_THEME = '''
    QMainWindow, QWidget { background-color: #2b2b2b; color: #ffffff; font-family: "Segoe UI", Arial; }
    QTabWidget::pane { border: 1px solid #444; }
    QTabBar::tab { background: #3c3f41; padding: 10px 20px; border: 1px solid #444; }
    QTabBar::tab:selected { background: #4b6eaf; color: white; }
    QLineEdit, QComboBox, QSpinBox { background-color: #3c3f41; border: 1px solid #555; padding: 5px; color: white; border-radius: 4px; }
    QPushButton { background-color: #4b6eaf; color: white; border: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; }
    QPushButton:hover { background-color: #5c85d6; }
    QTableWidget { background-color: #313335; gridline-color: #444; color: white; }
    QHeaderView::section { background-color: #3c3f41; color: white; border: 1px solid #444; }
    QListWidget { background-color: #313335; color: white; }
'''

LIGHT_THEME = '''
    QMainWindow, QWidget { background-color: #f5f5f5; color: #333333; font-family: "Segoe UI", Arial; }
    QTabWidget::pane { border: 1px solid #ccc; }
    QTabBar::tab { background: #e0e0e0; padding: 10px 20px; border: 1px solid #ccc; }
    QTabBar::tab:selected { background: #0078d4; color: white; }
    QLineEdit, QComboBox, QSpinBox { background-color: white; border: 1px solid #ccc; padding: 5px; color: #333; border-radius: 4px; }
    QPushButton { background-color: #0078d4; color: white; border: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; }
    QPushButton:hover { background-color: #106ebe; }
    QTableWidget { background-color: white; gridline-color: #ccc; color: #333; }
    QHeaderView::section { background-color: #e0e0e0; color: #333; border: 1px solid #ccc; }
    QListWidget { background-color: white; color: #333; }
'''

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Бытовой Системный Органайзер (HomeHub Pro)")
        self.resize(1000, 700)
        init_db()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(QLabel("🎨 Тема оформления:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Темная", "Светлая"])
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        top_layout.addWidget(self.theme_combo)
        main_layout.addLayout(top_layout)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        self.tab_widget.addTab(ExpenseModule(), "📊 Учет и Анализ Расходов")
        self.tab_widget.addTab(TodoModule(), "✅ Матрица Дел")
        self.tab_widget.addTab(CalorieModule(), "🍎 Дневник Здоровья")

        self.change_theme("Темная")

    def change_theme(self, theme_name):
        if theme_name == "Темная":
            self.setStyleSheet(DARK_THEME)
        else:
            self.setStyleSheet(LIGHT_THEME)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
