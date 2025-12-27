import os
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

        # Giữ lại Menu Bar cho các chức năng phụ để màn hình chính sạch sẽ
        self._create_menu_bar()

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

    def _create_menu_bar(self):
        """Thanh menu trên cùng cho Hướng dẫn/Liên hệ"""
        menu = self.menuBar()
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #2E7D32;
                border-radius: 8px;
                padding: 5px;
            }
            QMenu::item {
                padding: 10px 30px 10px 20px;
                font-size: 15px;
                font-weight: bold; /* Làm chữ đậm lên */
                color: #333333; /* Màu chữ đen đậm rõ ràng */
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #2E7D32; /* Màu nền khi rê chuột vào */
                color: white; /* Chữ trắng nổi bật trên nền xanh */
            }
        """)
        help_menu = menu.addMenu("⚙️ Tùy chọn hệ thống")
        
        actions = [
            ("📖 Hướng dẫn sử dụng", self._show_instruction),
            ("📞 Thông tin liên hệ", self._show_contact),
            ("⚖️ Điều khoản sử dụng", self._show_terms),
            ("❌ Thoát ứng dụng", QApplication.instance().quit)
        ]
        
        for text, slot in actions:
            act = QAction(text, self)
            act.triggered.connect(slot)
            help_menu.addAction(act)

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

        # Load ảnh nền trang chủ (Sử dụng đường dẫn bạn đã thiết lập)
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        img_path = os.path.normpath(os.path.join(base, "assets", "images", "Trang chủ.png"))
        self.bg_pixmap = QPixmap(img_path)

    def _paint_home_background(self, event):
        """Vẽ nền ảnh phủ kín màn hình"""
        if not self.bg_pixmap.isNull():
            painter = QPainter(self.home)
            painter.drawPixmap(self.home.rect(), self.bg_pixmap.scaled(
                self.home.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            ))

    def _setup_connections(self):
        """Kết nối logic điều hướng"""
        self.btn_start.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.input_p.btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.input_p.submitted.connect(self._on_data_submitted)

    # --- Các hàm hiển thị thông báo (Giữ nguyên) ---
    def _show_instruction(self):
        QMessageBox.information(self, "Hướng dẫn sử dụng", "- Chọn hệ chuyên gia: để hỗ trợ lựa chọn quyết định món ăn khi đến vùng ĐBSCL.\n" \
        "+ Nhấn chọn đầy đủ các tiêu chí của món ăn và Chờ kết quả. \n- Phần liên hệ: Để xem thông tin liên hệ. \n- Phần điều khoản sử dụng: Xem chính sách đối với các thông tin được cung cấp.")

    def _show_contact(self):
        QMessageBox.information(self, "Liên hệ", "Sinh viên thực hiện:\n- Lê Thị Thu Nguyệt ĐHSTIN23B\n- Nguyễn Tuấn Dinh ĐHSTIN23B")

    def _show_terms(self):
        QMessageBox.information(self, "Điều khoản sử dụng", "- Mục đích phục vụ học tập BTL môn Trí Tuệ Nhân Tạo.\n- Các thông tin chỉ mang tính chất tham khảo do thu thập từ nhiều nguồn khác nhau.")

    def _on_data_submitted(self, criteria):
        self.stack.setCurrentWidget(self.result_p)
        self.result_p.clear_results()
        
        # Gọi bộ máy suy diễn
        results = infer_dishes(criteria, DATA_MON_AN)
        
        # Hiển thị kết quả (Sửa lỗi gọi hàm add_result_card thành show_dishes)
        self.result_p.show_dishes(results)
        # 3. Xử lý hiển thị kết quả
        if not results:
            # Nếu không có kết quả phù hợp
            if hasattr(self.result_p, 'show_no_result'):
                self.result_p.show_no_result()
            else:
                lb_empty = QLabel("😔Rất tiếc, không tìm thấy món ăn nào khớp với lựa chọn của bạn.\nHãy thử thay đổi một vài tiêu chí nhé!")
                lb_empty.setStyleSheet("font-size: 18px; color: #7f8c8d; font-weight: bold; margin-top: 50px;")
                lb_empty.setAlignment(Qt.AlignCenter)
                self.result_p.res_layout.addWidget(lb_empty, 0, 0)
        else:
            # Duyệt qua danh sách kết quả và hiển thị lên giao diện
            for mon in results:
               self.result_p.show_dishes(results)

    def keyPressEvent(self, event):
        """Phím tắt F11 toàn màn hình"""
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showMaximized()
            else:
                self.showFullScreen()
        elif event.key() == Qt.Key_Escape and self.isFullScreen():
            self.showMaximized()