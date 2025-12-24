import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QScrollArea, QFrame, QGridLayout, QHBoxLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class ResultPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #F9FBF9;")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 20, 30, 30)

        # Tiêu đề kết quả
        self.title = QLabel("KẾT QUẢ TƯ VẤN ĐẶC SẢN")
        self.title.setStyleSheet("font-size: 28px; font-weight: bold; color: #1B5E20; margin-bottom: 10px;")
        self.layout.addWidget(self.title, alignment=Qt.AlignCenter)

        # Vùng cuộn hiển thị danh sách món ăn
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")
        
        self.res_container = QWidget()
        self.res_layout = QGridLayout(self.res_container)
        self.res_layout.setSpacing(25)
        
        self.scroll.setWidget(self.res_container)
        self.layout.addWidget(self.scroll)

        # Thanh nút bấm điều hướng
        bottom_layout = QHBoxLayout()
        self.btn_back = QPushButton("🔍 TÌM KIẾM LẠI")
        self.btn_exit = QPushButton("❌ THOÁT")
        
        btn_style = "padding: 12px 30px; font-weight: bold; border-radius: 10px; font-size: 15px;"
        self.btn_back.setStyleSheet(btn_style + "background-color: #2E7D32; color: white;")
        self.btn_exit.setStyleSheet(btn_style + "background-color: #C62828; color: white;")
        
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_exit.setCursor(Qt.PointingHandCursor)

        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_back)
        bottom_layout.addWidget(self.btn_exit)
        bottom_layout.addStretch()
        self.layout.addLayout(bottom_layout)

    def clear_results(self):
        """Xóa trắng danh sách hiển thị cũ"""
        while self.res_layout.count():
            item = self.res_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def show_dishes(self, dishes):
        """Hiển thị danh sách món ăn dưới dạng thẻ ảnh"""
        self.clear_results()
        
        if not dishes:
            no_res = QLabel("Rất tiếc, không tìm thấy món ăn nào phù hợp với yêu cầu của bạn.")
            no_res.setStyleSheet("font-size: 18px; color: #757575; font-style: italic;")
            self.res_layout.addWidget(no_res, 0, 0, alignment=Qt.AlignCenter)
            return

        for i, mon in enumerate(dishes):
            card = self.create_dish_card(mon)
            self.res_layout.addWidget(card, i // 2, i % 2)

    def create_dish_card(self, mon):
        """Tạo thẻ món ăn với hình ảnh và mô tả"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white; border-radius: 15px;
                border: 1px solid #E0E0E0;
            }
            QFrame:hover { border: 2px solid #A5D6A7; background-color: #F1F8E9; }
        """)
        
        card_lay = QVBoxLayout(card)
        card_lay.setContentsMargins(15, 15, 15, 15)

        # 1. Hiển thị hình ảnh từ assets/images/
        img_label = QLabel()
        img_label.setFixedSize(300, 180)
        img_label.setScaledContents(True)
        img_label.setStyleSheet("border-radius: 10px; border: 1px solid #EEE;")
        
        # Lấy đường dẫn ảnh từ DATA_MON_AN
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        img_file = mon.get('hinh_anh', 'default.png')
        img_path = os.path.join(base_path, "assets", "images", img_file)
        
        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            img_label.setText("🖼️ Hình ảnh đang cập nhật")
            img_label.setAlignment(Qt.AlignCenter)
            img_label.setStyleSheet("background: #F5F5F5; color: #AAA; border-radius: 10px;")
        else:
            img_label.setPixmap(pixmap)

        # 2. Thông tin văn bản
        name = QLabel(mon['ten'].upper())
        name.setStyleSheet("font-size: 18px; font-weight: bold; color: #1B5E20; border: none;")
        name.setWordWrap(True)

        location = QLabel(f"📍 {mon['tinh']}")
        location.setStyleSheet("font-weight: bold; color: #2E7D32; font-size: 14px; border: none;")

        desc = QLabel(mon['mo_ta'])
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #455A64; font-size: 13px; border: none; line-height: 18px;")

        # Thêm các thành phần vào thẻ
        card_lay.addWidget(img_label, alignment=Qt.AlignCenter)
        card_lay.addWidget(name)
        card_lay.addWidget(location)
        card_lay.addWidget(desc)
        
        return card