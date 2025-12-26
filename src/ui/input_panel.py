from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Signal
from .map_widget import MekongDeltaMap

class InputPanel(QWidget):
    submitted = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #F8F9F9;") 
        
        # Layout chính của toàn bộ Panel (Dọc)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 10)

        # --- 1. TIÊU ĐỀ ---
        header = QFrame()
        h_lay = QVBoxLayout(header)
        title = QLabel("KHÁM PHÁ ẨM THỰC MIỀN TÂY")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1B5E20;")
        subtitle = QLabel("Hệ chuyên gia tư vấn món ăn đặc sản Đồng bằng sông Cửu Long")
        h_lay.addWidget(title, alignment=Qt.AlignCenter)
        h_lay.addWidget(subtitle, alignment=Qt.AlignCenter)
        main_layout.addWidget(header)

        # --- 2. VÙNG NỘI DUNG CHÍNH ---
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # BÊN TRÁI: BẢN ĐỒ
        map_container = QFrame()
        map_v_lay = QVBoxLayout(map_container)
        
        # Thêm dấu * đỏ cho Bước 1
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

        # STYLE CHUNG CHO CHECKBOX (TICK XANH)
        checkbox_style = """
            QCheckBox::indicator:checked {
                background-color: #2E7D32;
                border: 2px solid #2E7D32;
                image: url(assets/icons/tick_xanh.png); 
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #BDC3C7;
                background-color: white;
            }
            QCheckBox { font-size: 13px; spacing: 8px; }
        """

        # BƯỚC 2: CHỌN MÙA (Chỉ chọn 1)
        f_lay.addWidget(QLabel("<b>🍂 BƯỚC 2: CHỌN MÙA <font color='red'>*</font></b>"))
        self.group_mua = QButtonGroup(self)
        self.group_mua.setExclusive(True)
        grid_mua = QGridLayout()
        mua_opts = ["Mùa nước nổi", "Mùa mưa", "Mùa khô", "Mùa Tết", "Mùa trái cây", "Quanh năm"]
        for i, text in enumerate(mua_opts):
            chk = QCheckBox(text)
            chk.setStyleSheet(checkbox_style)
            self.group_mua.addButton(chk)
            grid_mua.addWidget(chk, i // 2, i % 2)
        f_lay.addLayout(grid_mua)

        # BƯỚC 3: CHỌN LOẠI MÓN ĂN
        f_lay.addWidget(QLabel("<b>🍲 BƯỚC 3: LOẠI MÓN ĂN</b>"))
        self.combo_loai = QComboBox()
        self.combo_loai.addItems(["Tất cả", "Món nước", "Món khô", "Món tráng miệng", "Món gỏi", 
                                  "Món nướng", "Món xào", "Món hấp", "Món lẩu", "Món cháo", "Món bánh"])
        f_lay.addWidget(self.combo_loai)

        # BƯỚC 4: Nguyên liệu chính
        f_lay.addWidget(QLabel("<b>🐟 BƯỚC 4: NGUYÊN LIỆU CHÍNH</b>"))
        self.combo_nlc = QComboBox()
        self.combo_nlc.addItems(["Tất cả", "Hải sản", "Cá", "Bún", "Hủ tiếu", "Bánh tằm", 
                                 "Bột", "Nếp", "Gạo", "Thịt", "Trứng", "Trái cây"])
        f_lay.addWidget(self.combo_nlc)

        # BƯỚC 5: Nguyên liệu phụ
        f_lay.addWidget(QLabel("<b>🌿 BƯỚC 5: NGUYÊN LIỆU PHỤ</b>"))
        self.combo_nlp = QComboBox()
        self.combo_nlp.addItems(["Tất cả", "Sen", "Mắm", "Bông điên điển", "Lá chúc", 
                                 "Rau đắng", "Nước cốt dừa", "Rau củ quả", "Chao"])
        f_lay.addWidget(self.combo_nlp)

        # BƯỚC 6: KHẨU VỊ (Bắt buộc)
        f_lay.addWidget(QLabel("<b>👅 Bước 6: Chọn khẩu vị <font color='red'>*</font></b>"))
        self.group_vi = QButtonGroup(self)
        self.group_vi.setExclusive(True) # Đảm bảo chỉ được tick 1 ô vị

        grid_vi = QGridLayout()
        self.chk_cay = QCheckBox("🌶️ Cay (V1)");    self.chk_ngot = QCheckBox("🍰 Ngọt (V2)")
        self.chk_chua = QCheckBox("🍋 Chua (V3)");   self.chk_man = QCheckBox("🧂 Mặn (V4)")
        self.chk_beo = QCheckBox("🥥 Béo (V5)");    self.chk_thanh = QCheckBox("🍃 Thanh (V6)")
        self.chk_bui = QCheckBox("🥜 Bùi (V7)");     self.chk_dang = QCheckBox("☕ Đắng (V8)")
        
        grid_vi.addWidget(self.chk_cay, 0, 0); grid_vi.addWidget(self.chk_ngot, 0, 1)
        grid_vi.addWidget(self.chk_chua, 1, 0); grid_vi.addWidget(self.chk_man, 1, 1)
        grid_vi.addWidget(self.chk_beo, 2, 0); grid_vi.addWidget(self.chk_thanh, 2, 1)
        grid_vi.addWidget(self.chk_bui, 3, 0); grid_vi.addWidget(self.chk_dang, 3, 1)
        f_lay.addLayout(grid_vi)

        f_lay.addStretch()
        content_layout.addWidget(filter_frame, stretch=1)
        main_layout.addLayout(content_layout)

        # --- 3. HÀNG NÚT BẤM ---
        btn_lay = QHBoxLayout()
        self.btn_back = QPushButton("⬅ QUAY LẠI")
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.setStyleSheet("border: none; color: #1976D2; text-decoration: underline;")
        
        self.btn_submit = QPushButton("XEM GỢI Ý MÓN ĂN 🍽️")
        self.btn_submit.setFixedSize(220, 50)
        self.btn_submit.setCursor(Qt.PointingHandCursor)
        self.btn_submit.setStyleSheet("""
            QPushButton { 
                background-color: #2E7D32; 
                color: white; 
                font-weight: bold; 
                font-size: 16px; 
                border-radius: 8px; 
            }
            QPushButton:hover { background-color: #1B5E20; }
        """)
        
        btn_lay.addWidget(self.btn_back)
        btn_lay.addStretch()
        btn_lay.addWidget(self.btn_submit)
        main_layout.addLayout(btn_lay)

        # --- 4. FOOTER ---
        author_lbl = QLabel("© 2025 - Tác giả: [Thu Nguyệt & Tuấn Dinh] | ĐHSTIN23B | Dự án BTL Trí Tuệ Nhân Tạo")
        author_lbl.setStyleSheet("color: #7F8C8D; font-size: 11px; font-style: italic;")
        main_layout.addWidget(author_lbl, alignment=Qt.AlignRight)

        # Kết nối sự kiện
        self.selected_tinh = "Tất cả"
        self.btn_submit.clicked.connect(self._send_data)

    def _on_province_selected(self, name):
        self.selected_tinh = name
        self.label_tinh.setText(f"📍 ĐÃ CHỌN: {name.upper()}")

    def _send_data(self):
        # 1. Kiểm tra Tỉnh thành
        if self.selected_tinh == "Tất cả":
            QMessageBox.warning(self, "Thông báo", "⚠️ Hãy chọn đầy đủ: Vui lòng chọn một tỉnh thành trên bản đồ!")
            return
        
         # Kiểm tra Mùa
        selected_mua = self.group_mua.checkedButton()
        if not selected_mua:
            QMessageBox.warning(self, "Thông báo", "⚠️ Hãy chọn đầy đủ: Vui lòng chọn 1 mùa!")
            return


        # 2. Kiểm tra các ComboBox (Nếu cần bắt buộc chọn cụ thể, bỏ "Tất cả")
        if self.combo_loai.currentText() == "Tất cả" or \
           self.combo_nlc.currentText() == "Tất cả" or \
           self.combo_nlp.currentText() == "Tất cả":
            QMessageBox.warning(self, "Thông báo", "⚠️ Hãy chọn đầy đủ các thông tin mục Bước 3 đến Bước 5!")
            return

        # 3. Kiểm tra Khẩu vị
        selected_vi = []
        if self.chk_cay.isChecked(): selected_vi.append("Cay")
        if self.chk_ngot.isChecked(): selected_vi.append("Ngọt")
        if self.chk_chua.isChecked(): selected_vi.append("Chua")
        if self.chk_man.isChecked(): selected_vi.append("Mặn")
        if self.chk_beo.isChecked(): selected_vi.append("Béo")
        if self.chk_thanh.isChecked(): selected_vi.append("Thanh")
        if self.chk_bui.isChecked(): selected_vi.append("Bùi")
        if self.chk_dang.isChecked(): selected_vi.append("Đắng")

        if not selected_vi:
            QMessageBox.warning(self, "Thông báo", "⚠️ Hãy chọn đầy đủ: Vui lòng chọn ít nhất một khẩu vị ở Bước 6!")
            return

        # 4. Gửi dữ liệu
        data = {
            "tinh": self.selected_tinh, 
            "mua": selected_mua.text(),
            "loai": self.combo_loai.currentText(),
            "nlc": self.combo_nlc.currentText(), 
            "nlp": self.combo_nlp.currentText(), 
            "vi": selected_vi
        }
        self.submitted.emit(data)