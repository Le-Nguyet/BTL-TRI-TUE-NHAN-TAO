from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QCheckBox, QComboBox, QHBoxLayout, QFrame, QGridLayout)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor

class InputPanel(QWidget):
    submitted = Signal(dict)

    def __init__(self):
        super().__init__()
        # Thiết lập nền tổng thể cho trang
        self.setStyleSheet("background-color: #F1F8E9;") 
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 20, 40, 40)
        main_layout.setSpacing(20)

        # --- PHẦN TIÊU ĐỀ ---
        header_frame = QFrame()
        header_lay = QVBoxLayout(header_frame)
        
        title = QLabel("KHÁM PHÁ ẨM THỰC MIỀN TÂY")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #1B5E20; font-family: 'Segoe UI';")
        
        subtitle = QLabel("Hệ chuyên gia tư vấn món ăn đặc sản Đồng bằng sông Cửu Long") 
        subtitle.setStyleSheet("font-size: 16px; color: #455A64; margin-bottom: 20px;")
        
        header_lay.addWidget(title, alignment=Qt.AlignCenter)
        header_lay.addWidget(subtitle, alignment=Qt.AlignCenter)
        main_layout.addWidget(header_frame)

        # --- PHẦN LỰA CHỌN SỞ THÍCH (GRID) ---
        selection_group = QFrame()
        selection_group.setStyleSheet("background-color: white; border-radius: 15px; padding: 20px;")
        grid_lay = QGridLayout(selection_group)
        
        # Nhãn hướng dẫn
        prompt_label = QLabel("Bạn đang cảm thấy thế nào?")
        prompt_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2E7D32; border: none;")
        grid_lay.addWidget(prompt_label, 0, 0, 1, 2)

        # Các Checkbox với Emoji sinh động
        self.chk_nuoc = QCheckBox("🍲 Món có nước (Lẩu, bún, cháo...)")
        self.chk_cay = QCheckBox("🌶️ Thích vị cay nồng")
        self.chk_beo = QCheckBox("🥥 Thích vị béo (Cốt dừa, chao...)")
        self.chk_ngot = QCheckBox("🍰 Món ngọt / Bánh đặc sản")

        checkboxes = [self.chk_nuoc, self.chk_cay, self.chk_beo, self.chk_ngot]
        for i, chk in enumerate(checkboxes):
            chk.setStyleSheet("""
                QCheckBox { font-size: 16px; spacing: 10px; padding: 10px; border: none; }
                QCheckBox::indicator { width: 20px; height: 20px; }
            """)
            grid_lay.addWidget(chk, (i // 2) + 1, i % 2)

        main_layout.addWidget(selection_group)

        # --- PHẦN ĐỊA PHƯƠNG ---
        location_frame = QFrame()
        location_lay = QVBoxLayout(location_frame)
        
        loc_label = QLabel("📍 Chọn địa phương bạn muốn khám phá:")
        loc_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #33691E;")
        
        self.cbo_tinh = QComboBox()
        # Danh sách tỉnh thành dựa trên dữ liệu thu thập [cite: 45, 51, 58, 66, 82, 91, 99, 130, 152, 170, 202]
        self.cbo_tinh.addItems([
            "Tất cả các tỉnh", "An Giang", "Bạc Liêu", "Bến Tre", "Cần Thơ", 
            "Đồng Tháp", "Kiên Giang", "Long An", "Sóc Trăng", "Tiền Giang", "Trà Vinh"
        ])
        self.cbo_tinh.setStyleSheet("""
            QComboBox { 
                padding: 10px; font-size: 16px; border: 2px solid #A5D6A7; 
                border-radius: 8px; background: white; 
            }
        """)
        # Thêm vào phần khởi tạo giao diện trong InputPanel
        self.cbo_mua = QComboBox()
        self.cbo_mua.addItems(["Tất cả các mùa", "Mùa nước nổi", "Mùa mưa", "Mùa hè", "Quanh năm"])
        self.cbo_mua.setStyleSheet("""
            QComboBox { padding: 10px; font-size: 16px; border: 2px solid #A5D6A7; 
                border-radius: 8px; background: white; }
        """)

        # Thêm nhãn và widget vào layout
        main_layout.addWidget(QLabel("📅 Chọn thời điểm du lịch:"))
        main_layout.addWidget(self.cbo_mua)  
        
        location_lay.addWidget(loc_label)
        location_lay.addWidget(self.cbo_tinh)
        main_layout.addWidget(location_frame)

        # --- PHẦN NÚT ĐIỀU KHIỂN ---
        btn_lay = QHBoxLayout()
        
        self.btn_go = QPushButton("🔍 GỢI Ý MÓN NGON")
        self.btn_go.setCursor(Qt.PointingHandCursor)
        self.btn_go.setStyleSheet("""
            QPushButton { 
                background-color: #2E7D32; color: white; font-size: 18px; 
                font-weight: bold; padding: 15px; border-radius: 10px; 
            }
            QPushButton:hover { background-color: #1B5E20; }
        """)

        self.btn_back = QPushButton("QUAY LẠI")
        self.btn_back.setStyleSheet("font-size: 14px; color: #607D8B; border: none; text-decoration: underline;")

        btn_lay.addStretch()
        btn_lay.addWidget(self.btn_back)
        btn_lay.addSpacing(20)
        btn_lay.addWidget(self.btn_go, 2) # Nút Gợi ý lớn hơn
        btn_lay.addStretch()
        
        main_layout.addLayout(btn_lay)

        # Kết nối sự kiện
        self.btn_go.clicked.connect(self.send_data)

    def send_data(self):
        data = {
            "nuoc": self.chk_nuoc.isChecked(),
            "cay": self.chk_cay.isChecked(),
            "beo": self.chk_beo.isChecked(),
            "ngot": self.chk_ngot.isChecked(),
            "tinh": self.cbo_tinh.currentText()
        }
        self.submitted.emit(data)