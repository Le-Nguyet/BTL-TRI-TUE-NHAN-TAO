import os
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QFrame
from PySide6.QtGui import QPixmap, QPainter, QScreen
from PySide6.QtCore import Qt

# Import file màn hình tư vấn/kết quả của bạn
from src.ui.result_panel import ConsultWidget 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HỆ CHUYÊN GIA TƯ VẤN MÓN ĂN ĐBSCL")
        self.resize(1100, 750) # Kích thước mặc định tối ưu

        # 1. Quản lý các màn hình bằng QStackedWidget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 2. Khởi tạo các trang
        self.home_page = QWidget()
        self.consult_page = ConsultWidget() # File result_panel.py của bạn
        
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.consult_page)

        # 3. Load ảnh nền trang chủ (Lưu bản gốc để đảm bảo độ nét)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.bg_path = os.path.join(base_dir, "assets", "images", "Trang chủ.png")
        self.bg_pixmap = QPixmap(self.bg_path)

        # 4. Thiết lập giao diện và kết nối
        self._setup_home_ui()
        self._setup_connections()

    def _setup_home_ui(self):
        """Thiết kế các nút bấm đè lên ảnh nền tại Trang Chủ"""
        layout = QVBoxLayout(self.home_page)
        layout.setAlignment(Qt.AlignCenter)

        # Container cho các nút để tạo khoảng cách hợp lý
        button_container = QFrame()
        btn_layout = QVBoxLayout(button_container)
        
        self.btn_start = QPushButton("BẮT ĐẦU TƯ VẤN")
        self.btn_exit = QPushButton("THOÁT ỨNG DỤNG")

        # Định dạng Style cho nút bấm (có độ trong suốt để thấy nền)
        button_style = """
            QPushButton {
                background-color: rgba(20, 80, 20, 220); 
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: 2px solid #ffffff;
                border-radius: 15px;
                padding: 20px 40px;
                min-width: 300px;
            }
            QPushButton:hover {
                background-color: rgba(34, 139, 34, 255);
                border: 2px solid #aaffaa;
            }
            QPushButton:pressed {
                background-color: #004400;
            }
        """
        self.btn_start.setStyleSheet(button_style)
        self.btn_exit.setStyleSheet(button_style)

        btn_layout.addWidget(self.btn_start)
        btn_layout.addSpacing(30)
        btn_layout.addWidget(self.btn_exit)

        layout.addWidget(button_container)

    def _setup_connections(self):
        """Kết nối các sự kiện chuyển trang"""
        # Bấm Bắt đầu -> Chuyển sang trang Tư vấn (index 1)
        self.btn_start.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
        # Bấm Quay lại (nút nằm trong file result_panel.py) -> Về trang chủ (index 0)
        self.consult_page.btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        # Thoát ứng dụng
        self.btn_exit.clicked.connect(self.close)

    def paintEvent(self, event):
        """Vẽ hình nền trực tiếp từ file gốc để đạt độ nét cao nhất (DPI Aware)"""
        # Chỉ vẽ ảnh nền khi đang ở Trang chủ (index 0)
        if self.stacked_widget.currentIndex() == 0 and not self.bg_pixmap.isNull():
            painter = QPainter(self)
            
            # Cấu hình bộ vẽ chất lượng cao
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            
            # Tính toán scale ảnh phủ kín toàn bộ cửa sổ (Cover mode)
            window_size = self.size()
            scaled_bg = self.bg_pixmap.scaled(
                window_size, 
                Qt.KeepAspectRatioByExpanding, 
                Qt.SmoothTransformation
            )
            
            # Vẽ ảnh căn giữa màn hình
            x = (window_size.width() - scaled_bg.width()) // 2
            y = (window_size.height() - scaled_bg.height()) // 2
            
            painter.drawPixmap(x, y, scaled_bg)
            painter.end()

    def resizeEvent(self, event):
        """Cập nhật lại hình nền khi người dùng kéo giãn cửa sổ"""
        super().resizeEvent(event)
        self.update() # Buộc app vẽ lại paintEvent