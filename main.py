# main.py
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from src.ui.main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont("assets\\fonts\\Nunito-ExtraBold.ttf")
    app.setStyleSheet("""
        * {
            font-family: "Nunito";
        }
    """)

    # Khởi chạy cửa sổ chính
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())