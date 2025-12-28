import os
import webbrowser 
from PySide6.QtWidgets import *
from PySide6.QtGui import QPixmap, QPainter, QAction
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
        
        # Thiết lập kích thước
        self.resize(1100, 800)
        self.showMaximized()

        # Ẩn thanh menu bar mặc định để sử dụng giao diện tùy chỉnh sạch sẽ hơn
        self.menuBar().hide() 

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # 1. Khởi tạo giao diện Trang chủ (Home)
        self.home = QWidget()
        self.home.paintEvent = self._paint_home_background
        
        # 2. Khởi tạo các Panel chức năng
        self.input_p = InputPanel()
        self.result_p = ResultPanel()

        self.stack.addWidget(self.home)      # Index 0
        self.stack.addWidget(self.input_p)   # Index 1
        self.stack.addWidget(self.result_p)  # Index 2

        self._init_home_ui()
        self._setup_connections()

    def _init_home_ui(self):
        """Thiết kế giao diện trang chủ với menu Tùy chọn to đậm ở góc phải trên"""
        main_layout = QVBoxLayout(self.home)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # --- PHẦN 1: NÚT TÙY CHỌN HỆ THỐNG ---
        top_layout = QHBoxLayout()
        top_layout.addStretch() 
        
        self.btn_system_options = QPushButton("⚙️Tùy chọn")
        self.btn_system_options.setFixedSize(145, 40)
        self.btn_system_options.setCursor(Qt.PointingHandCursor)
        self.btn_system_options.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.75);
                color: white;
                border-radius: 12px;
                font-weight: 900;
                font-size: 16px;
                border: 2px solid white;
            }
            QPushButton:hover { background-color: #2E7D32; }
        """)
        
        # Menu thả xuống rõ nét
        system_menu = QMenu(self)
        system_menu.setStyleSheet("""
            QMenu { background-color: white; border: 2px solid #2E7D32; border-radius: 10px; padding: 5px; }
            QMenu::item { padding: 12px 30px; font-size: 15px; font-weight: bold; color: #000000; }
            QMenu::item:selected { background-color: #2E7D32; color: white; }
        """)

        system_menu.addAction("📖 Hướng dẫn sử dụng", self._show_instruction)
        system_menu.addAction("📞 Thông tin liên hệ", self._show_contact)
        system_menu.addAction("⚖️ Điều khoản sử dụng", self._show_terms)
        system_menu.addSeparator()
        system_menu.addAction("❌ Thoát ứng dụng", QApplication.instance().quit)
        
        self.btn_system_options.setMenu(system_menu)
        top_layout.addWidget(self.btn_system_options)
        main_layout.addLayout(top_layout)

        # --- PHẦN 2: NÚT BẮT ĐẦU TƯ VẤN ---
        main_layout.addStretch(85) 
        
        bottom_container = QHBoxLayout()
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
        
        bottom_container.addStretch()
        bottom_container.addWidget(self.btn_start)
        bottom_container.addStretch()
        main_layout.addLayout(bottom_container)
        main_layout.addStretch()

        # Load ảnh nền
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        img_path = os.path.normpath(os.path.join(base, "assets", "images", "Trang chủ.png"))
        self.bg_pixmap = QPixmap(img_path)

    def _paint_home_background(self, event):
        if not self.bg_pixmap.isNull():
            painter = QPainter(self.home)
            painter.drawPixmap(self.home.rect(), self.bg_pixmap.scaled(
                self.home.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            ))

    def _setup_connections(self):
        """Kết nối các tín hiệu giữa các màn hình"""
        self.btn_start.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.input_p.btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.input_p.submitted.connect(self._on_data_submitted)
        
        # Từ Kết quả -> Quay lại Nhập liệu
        if hasattr(self.result_p, 'btn_back'):
            self.result_p.btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        
        # Nút thoát ứng dụng
        if hasattr(self.result_p, 'btn_exit'):
            self.result_p.btn_exit.clicked.connect(QApplication.instance().quit)
        
        # KẾT NỐI TÍN HIỆU BẢN ĐỒ 
        if hasattr(self.result_p, 'view_map_signal'):
            self.result_p.view_map_signal.connect(self._open_food_map)

    def _open_food_map(self, food_query):
        """Hàm mở Google Maps để tìm 3 quán ngon nhất dựa trên tên món"""
        # Tạo câu lệnh tìm kiếm: "quán [tên món] ngon nhất"
        search_url = f"https://www.google.com/maps/search/+{food_query}+ngon+nhất"
        webbrowser.open(search_url)

    def _show_instruction(self):
        QMessageBox.information(self, "Hướng dẫn sử dụng", 
            "- Bước 1: Nhấn 'Bắt đầu' để vào giao diện nhập liệu.\n"
            "- Bước 2: Chọn các tiêu chí món ăn bạn mong muốn.\n"
            "- Bước 3: Xem kết quả và nhấn 'Xem địa chỉ' để tìm quán ăn gần nhất.")

    def _show_contact(self):
        QMessageBox.information(self, "Liên hệ", "Đội ngũ phát triển:\n- Lê Thị Thu Nguyệt - ĐHSTIN23B\n- Nguyễn Tuấn Dinh - ĐHSTIN23B")

    def _show_terms(self):
        QMessageBox.information(self, "Điều khoản", "Ứng dụng phục vụ mục đích học tập và tham khảo văn hóa ẩm thực.")

    def _on_data_submitted(self, criteria):
        """Xử lý logic khi người dùng nhấn gửi yêu cầu tư vấn"""
        self.stack.setCurrentWidget(self.result_p)
        self.result_p.clear_results()
        
        results = infer_dishes(criteria, DATA_MON_AN)
        
        if not results:
            # Tạo nhãn thông báo khi không có kết quả
            lb_empty = QLabel("😔 Rất tiếc, không tìm thấy món ăn nào khớp với lựa chọn của bạn.\nHãy thử thay đổi một vài tiêu chí nhé!")
            lb_empty.setStyleSheet("font-size: 20px; color: #7f8c8d; font-weight: bold; border: none;")
            lb_empty.setAlignment(Qt.AlignCenter)
            
            # Sử dụng Stretch để căn giữa dòng chữ theo chiều dọc
            self.result_p.res_layout.addStretch()
            self.result_p.res_layout.addWidget(lb_empty)
            self.result_p.res_layout.addStretch()
        else:
            # Hiển thị danh sách món ăn
            self.result_p.show_dishes(results)

    def keyPressEvent(self, event):
        """Xử lý các phím tắt toàn cục"""
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showMaximized()
            else:
                self.showFullScreen()
        elif event.key() == Qt.Key_Escape and self.isFullScreen():
            self.showMaximized()