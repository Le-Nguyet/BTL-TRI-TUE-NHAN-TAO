import os
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QPushButton, QLabel, QApplication
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt

# Import Panels
from src.ui.input_panel import InputPanel
from src.ui.result_panel import ResultPanel

# Import dữ liệu từ kiến thức chuyên gia
from src.logic.knowledge_base import DATA_MON_AN 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HỆ CHUYÊN GIA TƯ VẤN MÓN ĂN")
        
        # Thiết lập kích thước mặc định và cho phép co giãn
        self.resize(1100, 800)
        
        # Mở ứng dụng ở chế độ cửa sổ tối đa (Maximized) khi khởi chạy
        self.showMaximized() 

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
        
        # Cấu hình nút Bắt đầu
        self.btn_start = QPushButton("BẮT ĐẦU TƯ VẤN")
        self.btn_start.setFixedSize(250, 60)
        self.btn_start.setCursor(Qt.PointingHandCursor)
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

        # Đẩy nút xuống vị trí phù hợp trên ảnh nền
        lay.addStretch(200) 
        lay.addWidget(self.btn_start, alignment=Qt.AlignCenter)
        lay.addStretch(1)

        # Load ảnh nền
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        img_path = os.path.join(base, "assets", "images", "Trang chủ.png")
        self.bg_pixmap = QPixmap(img_path)

    def _paint_home_background(self, event):
        """Vẽ hình nền tự động co giãn theo kích thước cửa sổ"""
        if not self.bg_pixmap.isNull():
            painter = QPainter(self.home)
            painter.drawPixmap(self.home.rect(), self.bg_pixmap.scaled(
                self.home.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            ))

    def keyPressEvent(self, event):
        """Xử lý phím tắt cho chế độ màn hình"""
        # Nhấn F11 để bật/tắt toàn màn hình (FullScreen)
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showMaximized() # Hoặc showNormal()
            else:
                self.showFullScreen()
        
        # Nhấn Esc để thoát chế độ toàn màn hình
        elif event.key() == Qt.Key_Escape and self.isFullScreen():
            self.showMaximized()

    def _setup_connections(self):
        self.btn_start.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.input_p.btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.result_p.btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.input_p.submitted.connect(self.process_logic)
        self.result_p.btn_exit.clicked.connect(QApplication.instance().quit)

    def process_logic(self, criteria):
        """Logic lọc món ăn dựa trên dữ liệu chuyên gia"""
        self.result_p.clear_results()

        try:
            found_dishes = []
            target_loai = "Nước" if criteria.get("nuoc") else "Khô"

            for mon in DATA_MON_AN:
                # 1. Lọc theo Loại (Nước/Khô)
                if mon["loai"] != target_loai:
                    continue
                
                # 2. Lọc theo Tỉnh (Nếu có chọn tỉnh trên bản đồ)
                if criteria.get("tinh") != "Tất cả" and mon["tinh"] != criteria["tinh"]:
                    continue

                # 3. Lọc theo Vị (Kiểm tra Checkbox hoặc ComboBox)
                if criteria.get("cay") and "Cay" not in mon["vi"]:
                    continue
                
                # 4. Lọc theo Mùa
                if criteria.get("mua") != "Tất cả" and mon["mua"] != criteria["mua"]:
                    continue

                found_dishes.append(mon)
            
            # Hiển thị kết quả
            if not found_dishes:
                no_res = QLabel("Không tìm thấy món ăn nào phù hợp với yêu cầu của bạn.")
                no_res.setStyleSheet("font-size: 16px; color: #D32F2F; font-weight: bold;")
                no_res.setAlignment(Qt.AlignCenter)
                self.result_p.res_layout.addWidget(no_res)
            else:
                self.result_p.show_dishes(found_dishes)
            
            self.stack.setCurrentIndex(2) 
        except Exception as e:
            print(f"Lỗi xử lý logic: {e}")