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
        main_layout.setContentsMargins(20, 10, 20, 10) # Giảm lề dưới một chút cho Footer

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
        
        self.label_tinh = QLabel("📍 BƯỚC 1: CHỌN TỈNH THÀNH")
        self.label_tinh.setStyleSheet("font-weight: bold; color: #2E7D32; font-size: 14px;")
        map_v_lay.addWidget(self.label_tinh)

        self.map_selector = MekongDeltaMap()
        self.map_selector.setMinimumSize(600, 600) 
        self.map_selector.provinceSelected.connect(self._on_province_selected)
        map_v_lay.addWidget(self.map_selector)
        
        content_layout.addWidget(map_container, stretch=2)

        # BÊN PHẢI: CÁC BƯỚC LỰA CHỌN (BƯỚC 2 -> 5)
        filter_frame = QFrame()
        filter_frame.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #E0E0E0;")
        f_lay = QVBoxLayout(filter_frame)
        f_lay.setSpacing(12)
        # BƯỚC 2: CHỌN MÙA
        f_lay.addWidget(QLabel("<b>🍂 BƯỚC 2: CHỌN MÙA</b>"))
        self.combo_mua = QComboBox()
        self.combo_mua.addItems([ "Mùa nước nổi", "Mùa mưa", "Mùa khô", "Mùa tết", " Mùa trái cây"])
        f_lay.addWidget(self.combo_mua)

        # BƯỚC 3: CHỌN LOẠI MÓN ĂN
        f_lay.addWidget(QLabel("<b>🍲 BƯỚC 3: LOẠI MÓN ĂN</b>"))
        self.combo_loai = QComboBox()
        self.combo_loai.addItems(["Món nước", "Món khô", "Món tráng miệng", "Món gỏi", "Món nướng", "Món xào",
                                  "Món hấp", "Món lẩu", "Món cháo", "Món bánh" ])
        f_lay.addWidget(self.combo_loai)
        # BƯỚC 4: Nguyên liệu chính (N)
        f_lay.addWidget(QLabel("<b>🐟 BƯỚC 4: NGUYÊN LIỆU CHÍNH</b>"))
        self.combo_nlc = QComboBox()
        self.combo_nlc.addItems([ "Hải sản", "Cá", "Bún", "Hủ tiếu", "Bánh tằm", "Bột", "Nếp", "Gạo", "Thịt", "Trứng", "Trái cây"])
        f_lay.addWidget(self.combo_nlc)

        # BƯỚC 5: Nguyên liệu phụ (P)
        f_lay.addWidget(QLabel("<b>🌿 BƯỚC 5: NGUYÊN LIỆU PHỤ</b>"))
        self.combo_nlp = QComboBox()
        self.combo_nlp.addItems([ "Sen", "Mắm", "Bông điên điển", "Lá chúc", "Rau đắng", "Nước cốt dừa", "Rau củ quả", "Chao"])
        f_lay.addWidget(self.combo_nlp)
        

        # 6. KHẨU VỊ (V) - 8 Checkboxes
        f_lay.addWidget(QLabel("<b>👅 Bước 6: Chọn khẩu vị</b>"))
        grid_vi = QGridLayout()
        self.chk_cay = QCheckBox("🌶️ Cay (V1)");    
        self.chk_ngot = QCheckBox("🍰 Ngọt (V2)")
        self.chk_chua = QCheckBox("🍋 Chua (V3)");  
        self.chk_man = QCheckBox("🧂 Mặn (V4)")
        self.chk_beo = QCheckBox("🥥 Béo (V5)");   
        self.chk_thanh = QCheckBox("🍃 Thanh (V6)")
        self.chk_bui = QCheckBox("🥜 Bùi (V7)");    
        self.chk_dang = QCheckBox("☕ Đắng (V8)")
        grid_vi.addWidget(self.chk_cay, 0, 0); grid_vi.addWidget(self.chk_ngot, 0, 1)
        grid_vi.addWidget(self.chk_chua, 1, 0); grid_vi.addWidget(self.chk_man, 1, 1)
        grid_vi.addWidget(self.chk_beo, 1, 0); grid_vi.addWidget(self.chk_thanh, 1, 1)
        grid_vi.addWidget(self.chk_bui, 1, 0); grid_vi.addWidget(self.chk_dang, 1, 1)
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

        # --- 4. THÔNG TIN TÁC GIẢ (Footer) ---
        author_lay = QHBoxLayout()
        author_lbl = QLabel("© 2025 - Tác giả: [Thu Nguyệt & Tuấn Dinh] | ĐHSTIN23B | Dự án BTL Trí Tuệ Nhân Tạo")
        author_lbl.setStyleSheet("color: #7F8C8D; font-size: 11px; font-style: italic;")
        author_lay.addStretch()
        author_lay.addWidget(author_lbl)
        main_layout.addLayout(author_lay)

        # Kết nối sự kiện
        self.selected_tinh = "Tất cả"
        self.btn_submit.clicked.connect(self._send_data)

    def _on_province_selected(self, name):
        self.selected_tinh = name
        self.label_tinh.setText(f"📍 ĐÃ CHỌN: {name.upper()}")

    def _send_data(self):
        data = {
            "tinh": self.selected_tinh, 
            "nuoc": self.chk_nuoc.isChecked(),
            "cay": self.chk_cay.isChecked(), 
            "ngot": self.chk_ngot.isChecked(), 
            "chua": self.chk_chua.isChecked(),
            "man": self.chk_man.isChecked(),
            "beo": self.chk_beo.isChecked(),
            "thanh": self.chk_thanh.isChecked(),
            "bui": self.chk_bui.isChecked(),
            "dang": self.chk_dang.isChecked(),
            "vi": self.combo_vi.currentText(),
            "mua": self.combo_mua.currentText()
        }
        self.submitted.emit(data)