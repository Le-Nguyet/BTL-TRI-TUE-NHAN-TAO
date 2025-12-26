import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                             QScrollArea, QFrame, QGridLayout, QHBoxLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont

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
        # Thay đổi sang QVBoxLayout vì các thẻ bây giờ dàn hàng ngang chiếm hết chiều rộng
        self.res_layout = QVBoxLayout(self.res_container)
        self.res_layout.setSpacing(20)
        self.res_layout.setAlignment(Qt.AlignTop)
        
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
        """Tạo thẻ món ăn bố cục Ngang theo yêu cầu"""
        card = QFrame()
        card.setMinimumHeight(350)
        card.setStyleSheet("""
            QFrame {
                background-color: white; border-radius: 20px;
                border: 1px solid #D1D1D1;
            }
            QFrame:hover { border: 2px solid #2E7D32; }
        """)
        
        # Layout chính của thẻ là NGANG (QHBoxLayout)
        main_h_lay = QHBoxLayout(card)
        main_h_lay.setContentsMargins(20, 20, 20, 20)
        main_h_lay.setSpacing(30)

        # --- PHẦN BÊN TRÁI: ẢNH VÀ TÊN MÓN ---
        left_widget = QWidget()
        left_widget.setFixedWidth(600)
        left_lay = QVBoxLayout(left_widget)
        left_lay.setContentsMargins(0, 0, 0, 0)

        img_label = QLabel()
        img_label.setFixedSize(600, 500)
        img_label.setScaledContents(True)
        img_label.setStyleSheet("border-radius: 10px; border: 1px solid #EEEEEE;")

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        img_path = os.path.normpath(os.path.join(base_dir, "assets", "images", mon.get('hinh_anh', 'default.png')))
        
        pixmap = QPixmap(img_path)
        if not pixmap.isNull():
            img_label.setPixmap(pixmap)
        else:
            img_label.setText("🖼️ Đang cập nhật ảnh")
            img_label.setAlignment(Qt.AlignCenter)

        name_label = QLabel(mon['ten'].upper())
        name_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #1B5E20; margin-top: 10px;")
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignCenter)

        left_lay.addWidget(img_label)
        left_lay.addWidget(name_label)

        # --- VÙNG CHỈ (DASHED LINE) ---
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setStyleSheet("border-left: 1px dashed #A5D6A7; margin: 10px 0px;")

        # --- PHẦN BÊN PHẢI: THÔNG TIN CHI TIẾT ---
        right_widget = QWidget()
        right_lay = QVBoxLayout(right_widget)
        right_lay.setSpacing(15)

        # Style cho các dòng thông tin
        info_style = "font-size: 15px; color: #2E7D32; font-weight: 500;"
        
        loc_info = QLabel(f"📍 <b>Tỉnh:</b> {mon['tinh']}")
        loc_info.setStyleSheet(info_style)

        nlc_info = QLabel(f"👨‍🍳 <b>Nguyên liệu chính:</b> {mon.get('nlc', 'Đang cập nhật')}")
        nlc_info.setStyleSheet(info_style)

        nlp_info = QLabel(f"🌿 <b>Nguyên liệu phụ:</b> {mon.get('nlp', 'Đang cập nhật')}")
        nlp_info.setStyleSheet(info_style)

        mua_info = QLabel(f"📅 <b>Mùa:</b> {mon.get('mua', 'Quanh năm')}")
        mua_info.setStyleSheet(info_style)

        vi_info = QLabel(f"👅 <b>Vị:</b> {mon.get('vi', 'Đặc trưng')}")
        vi_info.setStyleSheet(info_style)

        # Mô tả tóm tắt ở dưới cùng
        desc_box = QFrame()
        desc_box.setStyleSheet("background-color: #F1F8E9; border-radius: 10px; border: none;")
        desc_lay = QVBoxLayout(desc_box)
        
        desc_label = QLabel(mon['mo_ta'])
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #455A64; font-size: 14px; font-style: italic; line-height: 20px; border: none;")
        desc_lay.addWidget(desc_label)

        right_lay.addWidget(loc_info)
        right_lay.addWidget(nlc_info)
        right_lay.addWidget(nlp_info)
        right_lay.addWidget(mua_info)
        right_lay.addWidget(vi_info)
        right_lay.addStretch()
        right_lay.addWidget(desc_box)

        # Thêm các thành phần vào Layout Ngang chính
        main_h_lay.addWidget(left_widget)
        main_h_lay.addWidget(line)
        main_h_lay.addWidget(right_widget)

        return card