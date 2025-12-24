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
        
        # Cấu hình nút
        self.btn_start = QPushButton("BẮT ĐẦU TƯ VẤN")
        self.btn_start.setFixedSize(230, 55)
        self.btn_start.setCursor(Qt.PointingHandCursor) # Hiệu ứng bàn tay khi rê chuột
        self.btn_start.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32; 
                color: white; 
                font-weight: bold; 
                font-size: 18px; 
                border-radius: 15px; 
                border: 2px solid white;
            }
            QPushButton:hover { 
                background-color: #1B5E20; 
                border: 2px solid #A5D6A7;
            }
        """)

        # --- ĐIỀU CHỈNH VỊ TRÍ TẠI ĐÂY ---
        # Thêm khoảng trống lớn phía trên (trọng số 10) để đẩy nút xuống
        lay.addStretch(200) 
        
        # Thêm nút vào giữa theo chiều ngang
        lay.addWidget(self.btn_start, alignment=Qt.AlignCenter)
        
        # Thêm một khoảng trống nhỏ phía dưới (trọng số 1) để nút không sát mép dưới quá
        lay.addStretch(1)

        # Load ảnh nền trang chủ 
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        img_path = os.path.join(base, "assets", "images", "Trang chủ.png")
        self.bg_pixmap = QPixmap(img_path)

    def _paint_home_background(self, event):
        if not self.bg_pixmap.isNull():
            painter = QPainter(self.home)
            # Vẽ hình nền phủ kín widget
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
            found_dishes = []
            
            # 1. Xác định loại món từ checkbox/radio (Nước hoặc Khô)
            target_loai = "Nước" if criteria.get("nuoc") else "Khô"

            for mon in DATA_MON_AN:
                # --- KIỂM TRA CÁC ĐIỀU KIỆN ---
                
                # Kiểm tra Loại (Nước/Khô)
                if mon.get("loai") != target_loai:
                    continue
                
                # Kiểm tra Tỉnh (Nếu người dùng có chọn tỉnh cụ thể)
                # Giả sử criteria["tinh"] là "Tất cả" hoặc tên tỉnh cụ thể
                if criteria.get("tinh") and criteria["tinh"] != "Tất cả":
                    if mon.get("tinh") != criteria["tinh"]:
                        continue

                # Kiểm tra Mùa
                if criteria.get("mua") and criteria["mua"] != "Tất cả":
                    if mon.get("mua") != criteria["mua"]:
                        continue

                # Kiểm tra Vị (Cay, Chua, Ngọt,...)
                # Giả sử criteria["vi"] là một chuỗi hoặc danh sách các vị người dùng muốn
                if criteria.get("vi") and criteria["vi"] != "Tất cả":
                    if criteria["vi"] not in mon.get("vi", []):
                        continue
                
                # Nếu vượt qua tất cả các bộ lọc trên, thêm vào danh sách kết quả
                found_dishes.append(mon)
            
            if not found_dishes:
                no_res = QLabel("Không tìm thấy món ăn nào phù hợp với khẩu vị của bạn.")
                no_res.setStyleSheet("font-size: 16px; color: red;")
                no_res.setAlignment(Qt.AlignCenter)
                self.result_p.res_layout.insertWidget(0, no_res)
            else:
                self.result_p.show_dishes(found_dishes)
            
            self.stack.setCurrentIndex(2) 
        except Exception as e:
            print(f"Lỗi xử lý logic: {e}")