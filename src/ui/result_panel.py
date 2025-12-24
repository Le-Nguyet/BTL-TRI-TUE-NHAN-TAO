from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QCheckBox, QComboBox, QHBoxLayout, QFrame, QGridLayout, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

class InputPanel(QWidget):
    submitted = Signal(dict)

    def __init__(self):
        super().__init__()
        # Thiết lập nền tổng thể xanh nhạt thanh khiết
        self.setStyleSheet("background-color: #F9FBF9;") 
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 30, 50, 50)
        main_layout.setSpacing(25)

        # --- PHẦN TIÊU ĐỀ (BANNER) ---
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #E8F5E9;
                border-radius: 20px;
                border: 1px solid #C8E6C9;
            }
        """)
        header_lay = QVBoxLayout(header_frame)
        header_lay.setContentsMargins(20, 30, 20, 30)

        title = QLabel("KHÁM PHÁ ẨM THỰC MIỀN TÂY")
        title.setStyleSheet("font-size: 36px; font-weight: 800; color: #1B5E20; font-family: 'Segoe UI';")
        
        subtitle = QLabel("Hệ chuyên gia tư vấn món ăn đặc sản Đồng bằng sông Cửu Long")
        subtitle.setStyleSheet("font-size: 18px; color: #455A64; font-weight: 500;")
        
        header_lay.addWidget(title, alignment=Qt.AlignCenter)
        header_lay.addWidget(subtitle, alignment=Qt.AlignCenter)
        main_layout.addWidget(header_frame)

        # --- PHẦN THẺ LỰA CHỌN (SELECTION CARD) ---
        card = QFrame()
        card.setStyleSheet("background-color: white; border-radius: 25px; padding: 30px;")
        
        # Tạo hiệu ứng đổ bóng cho chuyên nghiệp
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        
        prompt = QLabel("Bạn đang cảm thấy thế nào?")
        prompt.setStyleSheet("font-size: 22px; font-weight: bold; color: #2E7D32; margin-bottom: 10px;")
        card_layout.addWidget(prompt)

        grid = QGridLayout()
        grid.setSpacing(20)

        # Định nghĩa Checkbox với CSS hiện đại và Tick xanh
        chk_style = """
            QCheckBox {
                font-size: 18px;
                padding: 15px;
                background-color: #FAFAFA;
                border: 2px solid #F0F0F0;
                border-radius: 12px;
                color: #37474F;
            }
            QCheckBox:hover {
                background-color: #F1F8E9;
                border: 2px solid #A5D6A7;
            }
            QCheckBox::indicator {
                width: 28px;
                height: 28px;
                border: 2px solid #CFD8DC;
                border-radius: 8px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #2E7D32;
                border: 2px solid #2E7D32;
                image: url(https://img.icons8.com/material-sharp/24/ffffff/checkmark.png);
            }
        """

        self.chk_nuoc = QCheckBox("🍲 Món có nước (Lẩu, bún...)")
        self.chk_cay = QCheckBox("🌶️ Thích vị cay nồng")
        self.chk_beo = QCheckBox("🥥 Thích vị béo (Cốt dừa...)")
        self.chk_ngot = QCheckBox("🍰 Món ngọt / Bánh đặc sản")

        checkboxes = [self.chk_nuoc, self.chk_cay, self.chk_beo, self.chk_ngot]
        for i, chk in enumerate(checkboxes):
            chk.setStyleSheet(chk_style)
            chk.setCursor(Qt.PointingHandCursor)
            grid.addWidget(chk, i // 2, i % 2)

        card_layout.addLayout(grid)
        card_layout.addSpacing(20)

        # Địa phương
        loc_label = QLabel("📍 Bạn muốn tìm đặc sản tại tỉnh nào?")
        loc_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2E7D32;")
        card_layout.addWidget(loc_label)

        self.cbo_tinh = QComboBox()
        self.cbo_tinh.addItems([
            "Tất cả các tỉnh", "An Giang", "Bạc Liêu", "Bến Tre", "Cần Thơ", 
            "Đồng Tháp", "Kiên Giang", "Long An", "Sóc Trăng", "Tiền Giang", "Trà Vinh"
        ])
        self.cbo_tinh.setStyleSheet("""
            QComboBox {
                padding: 15px; font-size: 18px; border: 2px solid #E0E0E0;
                border-radius: 12px; background: white; color: #455A64;
            }
            QComboBox:hover { border: 2px solid #A5D6A7; }
        """)
        card_layout.addWidget(self.cbo_tinh)
        
        main_layout.addWidget(card)

        # --- HÀNH ĐỘNG (ACTIONS) ---
        actions_layout = QHBoxLayout()
        
        # Sửa lỗi AttributeError: định nghĩa self.btn_back rõ ràng
        self.btn_back = QPushButton("← QUAY LẠI")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.setStyleSheet("""
            QPushButton {
                background-color: transparent; color: #607D8B; font-size: 18px;
                font-weight: bold; padding: 15px; border: none;
            }
            QPushButton:hover { color: #2E7D32; }
        """)

        self.btn_go = QPushButton("🔍 GỢI Ý MÓN NGON")
        self.btn_go.setCursor(Qt.PointingHandCursor)
        self.btn_go.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32; color: white; font-size: 20px;
                font-weight: bold; padding: 20px 60px; border-radius: 15px;
            }
            QPushButton:hover { background-color: #1B5E20; }
        """)

        actions_layout.addWidget(self.btn_back)
        actions_layout.addStretch()
        actions_layout.addWidget(self.btn_go)
        
        main_layout.addLayout(actions_layout)

        # Kết nối sự kiện bên trong panel nếu cần, hoặc main_window sẽ kết nối
        self.btn_go.clicked.connect(self.send_data)

    def send_data(self):
        self.submitted.emit({
            "nuoc": self.chk_nuoc.isChecked(),
            "cay": self.chk_cay.isChecked(),
            "beo": self.chk_beo.isChecked(),
            "ngot": self.chk_ngot.isChecked(),
            "tinh": self.cbo_tinh.currentText()
        })