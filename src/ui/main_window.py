import os
import json
from PySide6.QtWidgets import (
    QMainWindow, QStackedWidget, QWidget, 
    QVBoxLayout, QPushButton, QLabel 
)
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt

from src.ui.input_panel import InputPanel
from src.ui.result_panel import ResultPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HỆ CHUYÊN GIA TƯ VẤN MÓN ĂN")
        self.resize(1000, 700)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Khởi tạo các trang
        self.home = QWidget()
        self.input_p = InputPanel()
        self.result_p = ResultPanel()

        self.stack.addWidget(self.home)
        self.stack.addWidget(self.input_p)
        self.stack.addWidget(self.result_p)

        self._init_home()
        self._setup_connections()

    def _init_home(self):
        lay = QVBoxLayout(self.home)
        self.btn_start = QPushButton("BẮT ĐẦU TƯ VẤN")
        self.btn_start.setFixedSize(250, 60)
        self.btn_start.setStyleSheet("background: white; font-weight: bold; border-radius: 10px;")
        lay.addWidget(self.btn_start, alignment=Qt.AlignCenter)

        # Đường dẫn ảnh nền
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.bg = QPixmap(os.path.join(base, "assets", "images", "Trang chủ.png"))

    def _setup_connections(self):
        self.btn_start.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.input_p.btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.result_p.btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.input_p.submitted.connect(self.process_logic)

    def process_logic(self, criteria):
        """Hàm suy diễn chính"""
        self.result_p.clear_results()
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        json_path = os.path.join(base, "assets", "data", "knowledge_base.json")

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            found = False
            for mon in data:
                # Logic lọc: Khớp loại và Vị
                if mon["loai"] == criteria["loai"]:
                    # Nếu chọn Cay thì món phải có Cay trong list 'vi'
                    if not criteria["cay"] or "Cay" in mon["vi"]:
                        self.result_p.add_dish_card(mon)
                        found = True
            
            if not found:
                self.result_p.res_layout.insertWidget(0, QLabel("Không có món nào phù hợp."))
            
            self.stack.setIndex(2) # Chuyển sang trang kết quả
        except Exception as e:
            print(f"Lỗi: {e}")

    def paintEvent(self, event):
        """Vẽ ảnh nền trang chủ"""
        if self.stack.currentIndex() == 0 and not self.bg.isNull():
            p = QPainter(self)
            p.drawPixmap(self.rect(), self.bg.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))