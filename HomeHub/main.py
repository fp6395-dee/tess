import sys
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
