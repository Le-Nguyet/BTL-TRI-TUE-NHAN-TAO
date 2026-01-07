import os
import webbrowser
from PySide6.QtWidgets import *
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt

# Import Panels
from src.ui.input_panel import InputPanel
from src.ui.result_panel import ResultPanel

# Import dữ liệu và logic suy diễn
from src.logic.knowledge_base import get_data_from_db
from src.logic.inference_engine import infer_dishes

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HỆ CHUYÊN GIA TƯ VẤN MÓN ĂN")
        
        # Thiết lập kích thước
        self.resize(1100, 800)
        self.showMaximized()

        # Ẩn thanh menu bar mặc định
        self.menuBar().hide() 

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # 1. Khởi tạo giao diện Trang chủ (Home)
        self.home = QWidget()
        self.home.paintEvent = self._paint_home_background
        
        # 2. Khởi tạo các Panel chức năng
        self.input_p = InputPanel()
        self.result_p = ResultPanel()
        self.last_dish = ""

        self.stack.addWidget(self.home)      # Index 0
        self.stack.addWidget(self.input_p)   # Index 1
        self.stack.addWidget(self.result_p)  # Index 2

        self._init_home_ui()
        self._setup_connections()

    def _init_home_ui(self):
        """Thiết kế giao diện trang chủ với menu Tùy chọn và nút Bắt đầu"""
        main_layout = QVBoxLayout(self.home)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # --- PHẦN 1: NÚT TÙY CHỌN HỆ THỐNG (GÓC PHẢI TRÊN) ---
        top_layout = QHBoxLayout()
        top_layout.addStretch() 
        
        # Đường dẫn icon mũi tên (assets/icons/mui_ten.png)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        icon_path = os.path.normpath(os.path.join(base_dir, "assets", "icons", "mui_ten.png")).replace("\\", "/")

        self.btn_system_options = QPushButton("⚙️Tùy chọn")
        self.btn_system_options.setFixedSize(145, 40)
        self.btn_system_options.setCursor(Qt.PointingHandCursor)
        
        # StyleSheet: Xóa khung trắng quanh mũi tên, chỉnh mũi tên nhỏ lại
        self.btn_system_options.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 0, 0, 0.75);
                color: white;
                border-radius: 12px;
                font-weight: 900;
                font-size: 16px;
                border: 2px solid white;
                padding-right: 20px;
            }}
            QPushButton:hover {{ background-color: #2E7D32; }}
            
            QPushButton::menu-indicator {{
                image: url("{icon_path}");
                subcontrol-origin: padding;
                subcontrol-position: right center;
                right: 10px;
                width: 12px;
                height: 12px;
                background: none;
                border: none;
            }}
        """)
        
        # Menu thả xuống
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
        system_menu.addAction("❌ Thoát ứng dụng", self._on_exit_app)
        
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

        # Load ảnh nền trang chủ
        img_path = os.path.normpath(os.path.join(base_dir, "assets", "images", "Trang chủ.png"))
        self.bg_pixmap = QPixmap(img_path)

    def _paint_home_background(self, event):
        if not self.bg_pixmap.isNull():
            painter = QPainter(self.home)
            painter.drawPixmap(self.home.rect(), self.bg_pixmap.scaled(
                self.home.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            ))

    def _setup_connections(self):
        """Kết nối tín hiệu giữa các màn hình"""
        self.btn_start.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.input_p.btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.input_p.submitted.connect(self._on_data_submitted)
        
        if hasattr(self.result_p, 'btn_back'):
            self.result_p.btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        
        if hasattr(self.result_p, 'btn_exit'):
            self.result_p.btn_exit.clicked.connect(self._on_exit_app)
        
        if hasattr(self.result_p, 'view_map_signal'):
            self.result_p.view_map_signal.connect(self._open_food_map)

        # Kết nối Menu từ trang chủ sang trang nhập liệu
        if hasattr(self.input_p, 'btn_system_options'):
            self.input_p.btn_system_options.setMenu(self.btn_system_options.menu())
            self.input_p.btn_system_options.setStyleSheet(self.btn_system_options.styleSheet())

    def _open_food_map(self, food_query):
        """Mở Google Maps tìm địa chỉ quán ăn"""
        search_url = f"https://www.google.com/maps/search/{food_query}+ngon+nhất"
        webbrowser.open(search_url)

    def _on_exit_app(self):
        """Xác nhận và hiển thị lời chúc trước khi thoát"""
        confirm = QMessageBox(self)
        confirm.setWindowTitle("Xác nhận")
        confirm.setText("Bạn có chắc chắn muốn thoát ứng dụng không?")
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)
        confirm.button(QMessageBox.Yes).setText("Thoát")
        confirm.button(QMessageBox.No).setText("Ở lại")
        
        if confirm.exec() == QMessageBox.Yes:
            thanks = QMessageBox(self)
            thanks.setWindowTitle("Tạm biệt")
            thanks.setText("Cảm ơn bạn đã tin tưởng lựa chọn chúng tôi!\n\n"
                          "Chúc bạn sẽ thưởng thức trọn vẹn món ăn và có những kỷ niệm thật đẹp tại vùng đất Chín Rồng này bạn nhé!!!.")
            thanks.setStyleSheet("QLabel{ font-size: 14px; color: #1B5E20; font-weight: bold; }")
            thanks.exec()
            QApplication.instance().quit()

    def _show_instruction(self):
        QMessageBox.information(self, "Hướng dẫn", 
            "- Bước 1: Nhấn 'Bắt đầu tư vấn' để vào giao diện nhập liệu.\n"
            "- Bước 2: Chọn tỉnh mà bạn muốn trải nghiệm ẩm thực đặc sản của vùng.\n"
            "- Bước 3: Chọn các tiêu chí ( từ 2 --> 6) của món ăn mà bạn mong muốn được thưởng thức.\n"
            "- Bước 4: Xem kết quả và nhấn 'Xem địa chỉ' để tìm quán ăn gần nhất.")

    def _show_contact(self):
        QMessageBox.information(self, "Liên hệ", "Sinh viên thực hiện:\n1. Lê Thị Thu Nguyệt - ĐHSTIN23B\n2. Nguyễn Tuấn Dinh - ĐHSTIN23B")

    def _show_terms(self):
        QMessageBox.information(self, "Điều khoản", "Ứng dụng phục vụ mục đích học tập và tham khảo văn hóa ẩm thực.")

    def _on_data_submitted(self, criteria):
        """Thực hiện suy diễn tri thức và điều hướng màn hình theo yêu cầu"""
        self.stack.setCurrentWidget(self.result_p)
        self.result_p.clear_results()
        
        # Lấy dữ liệu từ Database và thực hiện suy diễn
        results = infer_dishes(criteria, None)
        
        # Ngắt kết nối cũ của nút quay lại 
        try:
            self.result_p.btn_back.clicked.disconnect()
        except:
            pass
        
        if results:
            # --- TRƯỜNG HỢP CÓ KẾT QUẢ ---
            self.result_p.show_dishes(results)
            
            # Gán chức năng cho nút quay lại
            self.result_p.btn_back.clicked.connect(self._reset_and_go_back)
        else:
            # --- TRƯỜNG HỢP KHÔNG CÓ KẾT QUẢ ---
            lb_empty = QLabel("😔 Rất tiếc, hệ thống chưa tìm thấy món ăn phù hợp với yêu cầu của bạn.\nHãy thử thay đổi một vài tiêu chí nhé!")
            lb_empty.setStyleSheet("font-size: 20px; color: #7f8c8d; font-weight: bold; border: none;")
            lb_empty.setAlignment(Qt.AlignCenter)
            
            self.result_p.res_layout.addStretch()
            self.result_p.res_layout.addWidget(lb_empty)
            self.result_p.res_layout.addStretch()
            
            # Gán chức năng cho nút quay lại
            self.result_p.btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(1))

    def _reset_and_go_back(self):
        """Hàm hỗ trợ: Xóa sạch lựa chọn ở InputPanel và quay lại"""
        self.input_p.reset_filters()
        self.stack.setCurrentIndex(1)
    def keyPressEvent(self, event):
        """Phím tắt F11 toàn màn hình"""
        if event.key() == Qt.Key_F11:
            if self.isFullScreen(): 
                self.showMaximized()
            else: 
                self.showFullScreen()
        elif event.key() == Qt.Key_Escape and self.isFullScreen():
            self.showMaximized()
  