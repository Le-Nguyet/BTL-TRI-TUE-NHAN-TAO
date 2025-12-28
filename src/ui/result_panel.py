import os
import webbrowser # Thêm thư viện để mở web
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QScrollArea, QFrame, QGridLayout, QHBoxLayout)
from PySide6.QtCore import Qt, Signal # Thêm Signal
from PySide6.QtGui import QPixmap, QFont

class ResultPanel(QWidget):
    # Tạo tín hiệu để báo cho MainWindow biết khi người dùng nhấn xem bản đồ
    view_map_signal = Signal(str) 

    def __init__(self):
        super().__init__()
        # ... (Giữ nguyên phần init cũ của bạn) ...
        self.setStyleSheet("background-color: #F9FBF9;")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 20, 30, 30)

        self.title = QLabel("KẾT QUẢ TƯ VẤN MÓN ĂN ĐẶC SẢN")
        self.title.setStyleSheet("font-size: 28px; font-weight: bold; color: #1B5E20; margin-bottom: 10px;")
        self.layout.addWidget(self.title, alignment=Qt.AlignCenter)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")
        
        self.res_container = QWidget()
        self.res_layout = QVBoxLayout(self.res_container)
        self.res_layout.setSpacing(20)
        self.res_layout.setAlignment(Qt.AlignTop)
        
        self.scroll.setWidget(self.res_container)
        self.layout.addWidget(self.scroll)

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
        while self.res_layout.count():
            item = self.res_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def show_dishes(self, dishes):
        self.clear_results()
        for mon in dishes:
            card = self.create_dish_card(mon)
            self.res_layout.addWidget(card)

    def create_dish_card(self, mon):
        card = QFrame()
        card.setMinimumHeight(350)
        card.setStyleSheet("QFrame { background-color: white; border-radius: 20px; border: 1px solid #D1D1D1; } QFrame:hover { border: 2px solid #2E7D32; }")
        
        main_h_lay = QHBoxLayout(card)
        main_h_lay.setContentsMargins(20, 20, 20, 20)
        main_h_lay.setSpacing(30)

        # --- BÊN TRÁI ---
        left_widget = QWidget()
        left_widget.setFixedWidth(600)
        left_lay = QVBoxLayout(left_widget)
        
        img_label = QLabel()
        img_label.setFixedSize(600, 450)
        img_label.setScaledContents(True)
        img_label.setStyleSheet("border-radius: 10px; border: 1px solid #EEEEEE;")

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        img_path = os.path.normpath(os.path.join(base_dir, "assets", "images", mon.get('hinh_anh', 'default.png')))
        pixmap = QPixmap(img_path)
        if not pixmap.isNull(): img_label.setPixmap(pixmap)

        name_label = QLabel(mon['ten'].upper())
        name_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #1B5E20; margin-top: 10px;")
        name_label.setAlignment(Qt.AlignCenter)

        left_lay.addWidget(img_label)
        left_lay.addWidget(name_label)

        # --- BÊN PHẢI ---
        right_widget = QWidget()
        right_lay = QVBoxLayout(right_widget)
        
        info_style = "font-size: 15px; color: #2E7D32; font-weight: 500;"
        right_lay.addWidget(QLabel(f"📍 <b>Tỉnh:</b> {mon['tinh']}", styleSheet=info_style))
        right_lay.addWidget(QLabel(f"👨‍🍳 <b>Nguyên liệu chính:</b> {mon.get('nlc', '...')}", styleSheet=info_style))
        right_lay.addWidget(QLabel(f"📅 <b>Mùa:</b> {mon.get('mua')}", styleSheet=info_style))
        
        # NÚT XEM BẢN ĐỒ
        btn_map = QPushButton("📍 XEM ĐỊA CHỈ QUÁN")
        btn_map.setCursor(Qt.PointingHandCursor)
        btn_map.setStyleSheet("""
            QPushButton {
                background-color: #1976D2; color: white; font-weight: bold; 
                padding: 10px; border-radius: 8px; font-size: 14px; margin-top: 10px;
            }
            QPushButton:hover { background-color: #1565C0; }
        """)
        # Phát tín hiệu kèm tên món và tỉnh để tìm chính xác hơn
        btn_map.clicked.connect(lambda: self.view_map_signal.emit(f"{mon['ten']} tại {mon['tinh']}"))
        
        right_lay.addWidget(btn_map)

        desc_box = QFrame()
        desc_box.setStyleSheet("background-color: #F1F8E9; border-radius: 10px;")
        desc_lay = QVBoxLayout(desc_box)
        desc_label = QLabel(mon['mo_ta'])
        desc_label.setWordWrap(True)
        desc_lay.addWidget(desc_label)

        right_lay.addStretch()
        right_lay.addWidget(desc_box)

        main_h_lay.addWidget(left_widget)
        main_h_lay.addWidget(right_widget)
        return card