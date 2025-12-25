import os
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QPushButton, QLabel, QApplication
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt

# Import Panels
from src.ui.input_panel import InputPanel
from src.ui.result_panel import ResultPanel

# Import dữ liệu và logic suy diễn
from src.logic.knowledge_base import DATA_MON_AN 
from src.logic.inference_engine import infer_dishes

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HỆ CHUYÊN GIA TƯ VẤN MÓN ĂN")
        
        # Thiết lập kích thước mặc định và mở rộng tối đa
        self.resize(1100, 800)
        self.showMaximized() 

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # 1. Khởi tạo giao diện Trang chủ (Home)
        self.home = QWidget()
        self.home.paintEvent = self._paint_home_background 
        
        # 2. Khởi tạo các Panel chức năng
        self.input_p = InputPanel()
        self.result_p = ResultPanel()

        # Thêm vào Stack điều hướng
        self.stack.addWidget(self.home)      # Index 0
        self.stack.addWidget(self.input_p)   # Index 1
        self.stack.addWidget(self.result_p)  # Index 2

        self._init_home_ui()
        self._setup_connections()

    def _init_home_ui(self):
        """Thiết kế nút bấm trên trang chủ"""
        lay = QVBoxLayout(self.home)
        
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

        # Đẩy nút xuống vị trí 3/4 màn hình
        lay.addStretch(250) 
        lay.addWidget(self.btn_start, alignment=Qt.AlignCenter)
        lay.addStretch(5)

        # Load ảnh nền trang chủ
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        img_path = os.path.join(base, "assets", "images", "Trang chủ.png")
        self.bg_pixmap = QPixmap(img_path)

    def _paint_home_background(self, event):
        """Vẽ hình nền tự động co giãn"""
        if not self.bg_pixmap.isNull():
            painter = QPainter(self.home)
            painter.drawPixmap(self.home.rect(), self.bg_pixmap.scaled(
                self.home.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            ))

    def _setup_connections(self):
        """Kết nối các tín hiệu điều hướng giữa các trang"""
        # Từ Home -> Nhập liệu
        self.btn_start.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        
        # Từ Nhập liệu -> Quay lại Home
        self.input_p.btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        
        # Từ Kết quả -> Quay lại Nhập liệu
        if hasattr(self.result_p, 'btn_back'):
            self.result_p.btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        
        # Khi nhấn nút "Xem gợi ý" ở InputPanel
        self.input_p.submitted.connect(self._on_data_submitted)
        
        # Nút thoát
        if hasattr(self.result_p, 'btn_exit'):
            self.result_p.btn_exit.clicked.connect(QApplication.instance().quit)

    def _on_data_submitted(self, criteria):
        self.stack.setCurrentWidget(self.result_p)
        self.result_p.clear_results()
        
        # Gọi bộ máy suy diễn từ tập luật .txt
        from src.logic.inference_engine import infer_dishes
        results = infer_dishes(criteria, DATA_MON_AN)
        
        if not results:
            self.result_p.show_no_result() # Bạn nên thêm hàm này trong ResultPanel
        else:
            for mon in results:
                self.result_p.add_result_card(mon)
        
        # 4. Hiển thị lên màn hình
        if not results:
            lb_empty = QLabel("😔 Rất tiếc, không tìm thấy món ăn nào khớp với lựa chọn của bạn.\nHãy thử thay đổi một vài tiêu chí nhé!")
            lb_empty.setStyleSheet("font-size: 18px; color: #7f8c8d; font-weight: bold; margin-top: 50px;")
            lb_empty.setAlignment(Qt.AlignCenter)
            self.result_p.res_layout.addWidget(lb_empty, 0, 0)
        else:
            for index, mon in enumerate(results):
                # Gọi hàm vẽ Card món ăn (Hàm này có xử lý load ảnh D1.png, D2.png...)
                self.result_p.add_result_card(mon)

    def keyPressEvent(self, event):
        """Phím tắt F11 toàn màn hình"""
        if event.key() == Qt.Key_F11:
            if self.isFullScreen(): self.showMaximized()
            else: self.showFullScreen()
        elif event.key() == Qt.Key_Escape and self.isFullScreen():
            self.showMaximized()
     