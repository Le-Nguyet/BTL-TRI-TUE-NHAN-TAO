import os
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QPushButton, QLabel, QApplication
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt

# Import Panels
from src.ui.input_panel import InputPanel
from src.ui.result_panel import ResultPanel

# --- THAY ĐỔI QUAN TRỌNG: Import dữ liệu từ file python ---
from src.logic.knowledge_base import DATA_MON_AN 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HỆ CHUYÊN GIA TƯ VẤN MÓN ĂN")
        self.resize(1000, 700)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Giao diện Trang chủ
        self.home = QWidget()
        self.home.paintEvent = self._paint_home_background 
        
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
        self.btn_start.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32; color: white; font-weight: bold; 
                font-size: 18px; border-radius: 15px; border: 2px solid white;
            }
            QPushButton:hover { background-color: #1B5E20; }
        """)
        lay.addStretch()
        lay.addWidget(self.btn_start, alignment=Qt.AlignCenter)
        lay.addStretch()

        # Load ảnh nền trang chủ 
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        img_path = os.path.join(base, "assets", "images", "Trang chủ.png")
        self.bg_pixmap = QPixmap(img_path)

    def _paint_home_background(self, event):
        if not self.bg_pixmap.isNull():
            painter = QPainter(self.home)
            painter.drawPixmap(self.home.rect(), self.bg_pixmap.scaled(
                self.home.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            ))

    def _setup_connections(self):
        self.btn_start.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.input_p.btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.result_p.btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.input_p.submitted.connect(self.process_logic)
        self.result_p.btn_exit.clicked.connect(QApplication.instance().quit)

    def process_logic(self, criteria):
        """Sử dụng trực tiếp DATA_MON_AN từ knowledge_base.py"""
        self.result_p.clear_results()

        try:
            # Logic lọc món ăn từ biến DATA_MON_AN
            found_dishes = []
            
            # Lưu ý: criteria['nuoc'] là True/False từ Checkbox 
            target_loai = "Nước" if criteria["nuoc"] else "Khô"

            for mon in DATA_MON_AN:
                # Kiểm tra loại món (Nước/Khô)
                if mon["loai"] == target_loai:
                    # Nếu chọn "Cay", món đó phải có "Cay" trong danh sách vị
                    if criteria["cay"]:
                        if "Cay" in mon["vi"]:
                            found_dishes.append(mon)
                    else:
                        found_dishes.append(mon)
            
            if not found_dishes:
                no_res = QLabel("Không tìm thấy món ăn nào phù hợp với khẩu vị của bạn.")
                no_res.setAlignment(Qt.AlignCenter)
                self.result_p.res_layout.insertWidget(0, no_res)
            else:
                self.result_p.show_dishes(found_dishes)
            
            self.stack.setCurrentIndex(2) 
        except Exception as e:
            print(f"Lỗi xử lý logic: {e}")