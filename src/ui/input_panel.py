import os
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal
from .map_widget import MekongDeltaMap

class InputPanel(QWidget):
    submitted = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #F8F9F9;") 
        
        # Layout chính của toàn bộ Panel 
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 10, 20, 10)

        # --- 0. THANH CÔNG CỤ PHÍA TRÊN (TOP BAR) ---
        self.top_bar = QHBoxLayout()
        
        self.btn_system_options = QPushButton("⚙️ Tùy chọn")
        self.btn_system_options.setFixedSize(145, 40)
        self.btn_system_options.setCursor(Qt.PointingHandCursor)
        
        self.top_bar.addStretch()  # Đẩy nút sang bên phải
        self.top_bar.addWidget(self.btn_system_options)
        self.main_layout.addLayout(self.top_bar)

        # --- 1. TIÊU ĐỀ ---
        header = QFrame()
        h_lay = QVBoxLayout(header)
        title = QLabel("TINH HOA ẨM THỰC PHƯƠNG NAM")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #1B5E20;")
        
        subtitle = QLabel("Hệ thống trí tuệ nhân tạo hỗ trợ khám phá đặc sản ĐBSCL qua lăng kính công nghệ số")
        
        h_lay.addWidget(title, alignment=Qt.AlignCenter)
        h_lay.addWidget(subtitle, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(header)

        # --- 2. VÙNG NỘI DUNG CHÍNH ---
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # BÊN TRÁI: BẢN ĐỒ
        map_container = QFrame()
        map_v_lay = QVBoxLayout(map_container)
        
        self.label_tinh = QLabel("📍 BƯỚC 1: CHỌN TỈNH THÀNH <font color='red'>*</font>")
        self.label_tinh.setStyleSheet("font-weight: bold; color: #2E7D32; font-size: 14px;")
        map_v_lay.addWidget(self.label_tinh)

        self.map_selector = MekongDeltaMap()
        self.map_selector.setMinimumSize(600, 600) 
        self.map_selector.provinceSelected.connect(self._on_province_selected)
        map_v_lay.addWidget(self.map_selector)
        
        content_layout.addWidget(map_container, stretch=2)

        # BÊN PHẢI: CÁC BƯỚC LỰA CHỌN
        filter_frame = QFrame()
        filter_frame.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #E0E0E0;")
        f_lay = QVBoxLayout(filter_frame)
        f_lay.setSpacing(12)

        # STYLE CHO CHECKBOX
        checkbox_style = """
            QCheckBox {
                font-size: 16px;
                spacing: 10px;    
                color: #2C3E50;
                min-height: 20px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #BDC3C7;
                border-radius: 4px;
                background-color: white;
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:checked {
                border: none;
                background-color: transparent;
                image: url(assets/icons/tick_xanh.png); 
                width: 24px;
                height: 24px;
            }
            QCheckBox::indicator:unchecked:hover {
                border: 2px solid #2E7D32;
            }
        """

        # BƯỚC 2: CHỌN MÙA
        f_lay.addWidget(QLabel("<b>🍂 BƯỚC 2: CHỌN MÙA <font color='red'>*</font></b>"))
        self.group_mua = QButtonGroup(self)
        self.group_mua.setExclusive(True)
        grid_mua = QGridLayout()
        mua_opts = ["Mùa nước nổi", "Mùa mưa", "Mùa khô", "Mùa Tết", "Mùa trái cây", " Quanh năm"]
        for i, text in enumerate(mua_opts):
            chk = QCheckBox(text)
            chk.setStyleSheet(checkbox_style)
            self.group_mua.addButton(chk)
            grid_mua.addWidget(chk, i // 2, i % 2)
        f_lay.addLayout(grid_mua)

        # BƯỚC 3: LOẠI MÓN ĂN
        f_lay.addWidget(QLabel("<b>🍲 BƯỚC 3: LOẠI MÓN ĂN <font color='red'>*</font></b>"))
        self.group_loai = QButtonGroup(self)
        self.group_loai.setExclusive(True)
        grid_loai = QGridLayout()
        loai_opts = ["Món nước", "Món khô", "Món tráng miệng", "Món gỏi", "Món nướng", 
                     "Món xào", "Món hấp", "Món lẩu", "Món cháo", "Món bánh"]
        for i, text in enumerate(loai_opts):
            chk = QCheckBox(text)
            chk.setStyleSheet(checkbox_style)
            self.group_loai.addButton(chk)
            grid_loai.addWidget(chk, i // 2, i % 2)
        f_lay.addLayout(grid_loai)
        
        # BƯỚC 4: NGUYÊN LIỆU CHÍNH
        f_lay.addWidget(QLabel("<b>🐟 BƯỚC 4: NGUYÊN LIỆU CHÍNH <font color='red'>*</font></b>"))
        self.combo_nlc = QComboBox()
        self.combo_nlc.addItems(["Tất cả", "Hải sản", "Cá", "Bún", "Hủ tiếu", "Bánh tằm", 
                                 "Bột", "Nếp", "Gạo", "Thịt", "Trứng", "Trái cây"])
        f_lay.addWidget(self.combo_nlc)

        # BƯỚC 5: NGUYÊN LIỆU PHỤ
        f_lay.addWidget(QLabel("<b>🌿 BƯỚC 5: NGUYÊN LIỆU PHỤ <font color='red'>*</font></b>"))
        self.combo_nlp = QComboBox()
        self.combo_nlp.addItems(["Tất cả", "Sen", "Mắm", "Bông điên điển", "Lá chúc", 
                                 "Rau đắng", "Nước cốt dừa", "Rau củ quả", "Chao", " á giang", "Dầu mè"])
        f_lay.addWidget(self.combo_nlp)

        # BƯỚC 6: CHỌN KHẨU VỊ
        f_lay.addWidget(QLabel("<b>👅 Bước 6: Chọn khẩu vị <font color='red'>*</font></b>"))
        self.group_vi = QButtonGroup(self)
        self.group_vi.setExclusive(True)
        grid_vi = QGridLayout()
        
        self.vi_options = [
            ("🌶️ Cay", "Cay"), ("🍰 Ngọt", "Ngọt"), ("🍋 Chua", "Chua"), 
            ("🧂 Mặn", "Mặn"), ("🥥 Béo", "Béo"), ("☕ Đắng", "Đắng")
        ]

        for i, (display, value) in enumerate(self.vi_options):
            chk = QCheckBox(display)
            chk.setStyleSheet(checkbox_style)
            self.group_vi.addButton(chk)
            grid_vi.addWidget(chk, i // 2, i % 2)
        f_lay.addLayout(grid_vi)

        f_lay.addStretch()
        content_layout.addWidget(filter_frame, stretch=1)
        self.main_layout.addLayout(content_layout)

        # --- 3. HÀNG NÚT BẤM ---
        btn_lay = QHBoxLayout()
        self.btn_back = QPushButton("⬅ QUAY LẠI")
        self.btn_back.setStyleSheet("border: none; color: #1976D2; text-decoration: underline;")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        
        self.btn_submit = QPushButton("XEM GỢI Ý MÓN ĂN 🍽️")
        self.btn_submit.setFixedSize(220, 50)
        self.btn_submit.setCursor(Qt.PointingHandCursor)
        self.btn_submit.setStyleSheet("""
            QPushButton { 
                background-color: #2E7D32; 
                color: white; font-weight: bold; font-size: 16px; border-radius: 8px; 
            }
            QPushButton:hover { background-color: #1B5E20; }
        """)
        
        btn_lay.addWidget(self.btn_back)
        btn_lay.addStretch()
        btn_lay.addWidget(self.btn_submit)
        self.main_layout.addLayout(btn_lay)

        # --- 4. FOOTER ---
        author_lbl = QLabel("© 2025 - Tác giả: [Thu Nguyệt & Tuấn Dinh] | ĐHSTIN23B | Dự án BTL Trí Tuệ Nhân Tạo")
        author_lbl.setStyleSheet("color: #7F8C8D; font-size: 11px; font-style: italic;")
        self.main_layout.addWidget(author_lbl, alignment=Qt.AlignRight)

        # Khởi tạo dữ liệu
        self.selected_tinh = "Tất cả"
        self.btn_submit.clicked.connect(self._send_data)

    def _on_province_selected(self, name):
        self.selected_tinh = name
        self.label_tinh.setText(f"📍 ĐÃ CHỌN: {name.upper()}")

    def _send_data(self):
        # 1. Kiểm tra Tỉnh thành
        if self.selected_tinh == "Tất cả":
            QMessageBox.warning(self, "Thông báo", "⚠️ Vui lòng chọn một tỉnh thành trên bản đồ ở Bước 1!")
            return
        
        # 2. Kiểm tra Mùa
        selected_mua = self.group_mua.checkedButton()
        if not selected_mua:
            QMessageBox.warning(self, "Thông báo", "⚠️ Vui lòng chọn 1 mùa ở Bước 2!")
            return
        
        # 3. Kiểm tra Loại món ăn
        selected_loai = self.group_loai.checkedButton()
        if not selected_loai:
            QMessageBox.warning(self, "Thông báo", "⚠️ Vui lòng chọn 1 Loại món ăn ở Bước 3!")
            return

        # 4. Kiểm tra Nguyên liệu chính
        if self.combo_nlc.currentText() == "Tất cả":
            QMessageBox.warning(self, "Thông báo", "⚠️ Vui lòng chọn Nguyên liệu chính ở Bước 4!")
            return

        # 5. Kiểm tra Nguyên liệu phụ
        if self.combo_nlp.currentText() == "Tất cả":
            QMessageBox.warning(self, "Thông báo", "⚠️ Vui lòng chọn Nguyên liệu phụ ở Bước 5!")
            return

        # 6. Kiểm tra Khẩu vị
        selected_vi_btn = self.group_vi.checkedButton()
        if not selected_vi_btn:
            QMessageBox.warning(self, "Thông báo", "⚠️ Vui lòng chọn 1 khẩu vị ở Bước 6!")
            return

        # Tách lấy tên vị
        flavor_text = selected_vi_btn.text().split(' ')[1] 
        
        data = {
            "tinh": self.selected_tinh, 
            "mua": selected_mua.text(),
            "loai": selected_loai.text(),
            "nlc": self.combo_nlc.currentText(), 
            "nlp": self.combo_nlp.currentText(), 
            "vi": [flavor_text]
        }
        self.submitted.emit(data)