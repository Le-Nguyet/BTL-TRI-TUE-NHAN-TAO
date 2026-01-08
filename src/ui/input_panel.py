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
        mua_opts = ["Mùa nước nổi", "Mùa mưa", "Mùa khô", "Mùa tết", "Mùa trái cây", "Quanh năm"]
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
                                 "Bột", "Nếp", "Gạo", "Thịt", "Trứng", "Trái cây", "Côn trùng"])
        f_lay.addWidget(self.combo_nlc)

        # BƯỚC 5: NGUYÊN LIỆU PHỤ
        f_lay.addWidget(QLabel("<b>🌿 BƯỚC 5: NGUYÊN LIỆU PHỤ <font color='red'>*</font></b>"))
        self.combo_nlp = QComboBox()
        self.combo_nlp.addItems(["Tất cả", "Sen", "Mắm", "Bông điên điển", "Lá chúc", 
                                 "Rau đắng", "Nước cốt dừa", "Rau củ quả", "Chao", "Lá giang", "Dầu mè"])
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
        """Kiểm tra logic và gửi dữ liệu đi để suy diễn"""
        
        # 1. Kiểm tra Bước 1: Tỉnh thành
        if not hasattr(self, 'selected_tinh') or self.selected_tinh == "Tất cả":
            QMessageBox.warning(self, "Thông báo", "⚠️ Bước 1: Vui lòng chọn một tỉnh trên bản đồ!")
            return

        # 2. Kiểm tra Bước 2: Mùa
        selected_mua = self.group_mua.checkedButton()
        if not selected_mua:
            QMessageBox.warning(self, "Thông báo", "⚠️ Bước 2: Bạn chưa chọn Mùa!")
            return
        
        # 3. Kiểm tra Bước 3: Loại món ăn
        selected_loai = self.group_loai.checkedButton()
        if not selected_loai:
            QMessageBox.warning(self, "Thông báo", "⚠️ Bước 3: Bạn chưa chọn Loại món ăn!")
            return

        # 4. Kiểm tra Bước 4: Nguyên liệu chính
        nlc_text = self.combo_nlc.currentText().strip()
        if nlc_text == "Tất cả":
            QMessageBox.warning(self, "Thông báo", "⚠️ Bước 4: Vui lòng chọn Nguyên liệu chính!")
            return

        # 5. Kiểm tra Bước 5: Nguyên liệu phụ (RÀNG BUỘC MỚI)
        nlp_text = self.combo_nlp.currentText().strip()
        
        # Logic: Nếu NLC khác "Trái cây" mà NLP lại chọn "Tất cả" -> Báo lỗi
        if nlc_text != "Trái cây" and nlp_text == "Tất cả":
            QMessageBox.warning(self, "Thông báo", f"⚠️ Với nguyên liệu chính là '{nlc_text}', bạn bắt buộc phải chọn một Nguyên liệu phụ cụ thể ở Bước 5!")
            return

        # --- ĐỒNG BỘ HÓA CHO TRÁI CÂY (D63) ---
        # Nếu là Trái cây, ép NLP về "Tất cả" để khớp với mã P11 trong file luật
        if nlc_text == "Trái cây":
            final_nlp = "Tất cả"
        else:
            final_nlp = nlp_text

        # 6. Kiểm tra Bước 6: Khẩu vị
        selected_vi_btn = self.group_vi.checkedButton()
        if not selected_vi_btn:
            QMessageBox.warning(self, "Thông báo", "⚠️ Bước 6: Bạn chưa chọn Khẩu vị!")
            return

        # 7. CHUẨN HÓA DỮ LIỆU GỬI ĐI
        raw_vi_text = selected_vi_btn.text()
        flavor_text = raw_vi_text.split(' ')[1] if ' ' in raw_vi_text else raw_vi_text

        data = {
            "tinh": self.selected_tinh.strip(), 
            "mua": selected_mua.text().strip(),
            "loai": selected_loai.text().strip(),
            "nlc": nlc_text, 
            "nlp": final_nlp, 
            "vi": [flavor_text.strip()]
        }

        # Phát tín hiệu gửi dữ liệu sang MainWindow
        self.submitted.emit(data)
    
    def reset_filters(self):
        """Reset toàn bộ các lựa chọn về trạng thái mặc định bao gồm cả bản đồ"""
        # 1. Reset biến lưu trữ tỉnh thành và nhãn hiển thị
        self.selected_tinh = "Tất cả"
        self.label_tinh.setText("📍 BƯỚC 1: CHỌN TỈNH THÀNH <font color='red'>*</font>")
        
        # 2. Reset trạng thái trên bản đồ (MekongDeltaMap)
        if hasattr(self, 'map_selector'):
            self.map_selector.selected_province = None 
            if hasattr(self.map_selector, 'clicked_province'):
                self.map_selector.clicked_province = None
            
            # Quan trọng: Gọi update() để bản đồ vẽ lại 
            self.map_selector.update() 
        
        # 3. Reset các nhóm nút (Mùa, Loại, Vị)
        for group in [self.group_mua, self.group_loai, self.group_vi]:
            checked = group.checkedButton()
            if checked:
                group.setExclusive(False)
                checked.setChecked(False)
                group.setExclusive(True)

        # 4. Reset các ComboBox 
        self.combo_nlc.setCurrentIndex(0)
        self.combo_nlp.setCurrentIndex(0)