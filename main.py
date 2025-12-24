import sys
import os

# Thêm đường dẫn gốc để Python tìm thấy module 'src'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.ui.styles import get_main_style

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Áp dụng style và font từ file styles.py
    app.setStyleSheet(get_main_style())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())