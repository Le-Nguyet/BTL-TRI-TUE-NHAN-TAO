from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QCheckBox, QComboBox, QFrame, QGridLayout)
from PySide6.QtCore import Qt, Signal
from .map_widget import MekongDeltaMap

class InputPanel(QWidget):
    submitted = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #F8F9F9;") 
        
        # Layout chính của toàn bộ Panel (Dọc)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 20)

        # --- 1. TIÊU ĐỀ (Phía trên cùng) ---
        header = QFrame()
        h_lay = QVBoxLayout(header)
        title = QLabel("KHÁM PHÁ ẨM THỰC MIỀN TÂY")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1B5E20;")
        subtitle = QLabel("Hệ chuyên gia tư vấn món ăn đặc sản Đồng bằng sông Cửu Long")
        h_lay.addWidget(title, alignment=Qt.AlignCenter)
        h_lay.addWidget(subtitle, alignment=Qt.AlignCenter)
        main_layout.addWidget(header)

        # --- 2. VÙNG NỘI DUNG CHÍNH (Layout hàng ngang) ---
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # --- BÊN TRÁI: BẢN ĐỒ ---
        map_container = QFrame()
        map_v_lay = QVBoxLayout(map_container)
        
        self.label_tinh = QLabel("📍 BƯỚC 1: CHỌN TỈNH THÀNH")
        self.label_tinh.setStyleSheet("font-weight: bold; color: #2E7D32; font-size: 14px;")
        map_v_lay.addWidget(self.label_tinh)

        self.map_selector = MekongDeltaMap()
        # Cho phép bản đồ mở rộng linh hoạt
        self.map_selector.setMinimumSize(600, 600) 
        self.map_selector.provinceSelected.connect(self._on_province_selected)
        map_v_lay.addWidget(self.map_selector)
        
        content_layout.addWidget(map_container, stretch=2) # Chiếm 2 phần không gian

        # --- BÊN PHẢI: BẢNG LỰA CHỌN ---
        filter_frame = QFrame()
        filter_frame.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #E0E0E0;")
        filter_v_lay = QVBoxLayout(filter_frame)
        filter_v_lay.setContentsMargins(20, 20, 20, 20)
        filter_v_lay.setSpacing(15)

        filter_title = QLabel("🍴 BƯỚC 2: CHỌN KHẨU VỊ")
        filter_title.setStyleSheet("font-weight: bold; font-size: 14px; border: none; color: #2E7D32;")
        filter_v_lay.addWidget(filter_title)

        # Sử dụng QGridLayout để xếp các lựa chọn gọn gàng theo chiều dọc bên phải
        grid = QGridLayout()
        grid.setSpacing(10)

        self.chk_nuoc = QCheckBox("🍲 Món có nước")
        self.chk_cay = QCheckBox("🌶️ Vị cay")
        self.chk_beo = QCheckBox("🥥 Vị béo")
        self.chk_ngot = QCheckBox("🍰 Món ngọt")
        
        # Xếp các checkbox thành 2 cột
        grid.addWidget(self.chk_nuoc, 0, 0)
        grid.addWidget(self.chk_cay, 0, 1)
        grid.addWidget(self.chk_beo, 1, 0)
        grid.addWidget(self.chk_ngot, 1, 1)
        
        filter_v_lay.addLayout(grid)

        # ComboBoxes xếp dọc
        filter_v_lay.addWidget(QLabel("👅 Vị chủ đạo:"))
        self.combo_vi = QComboBox()
        self.combo_vi.addItems(["Tất cả", "Cay", "Chua", "Ngọt", "Mặn", "Đậm đà"])
        filter_v_lay.addWidget(self.combo_vi)

        filter_v_lay.addWidget(QLabel("🍂 Mùa ngon nhất:"))
        self.combo_mua = QComboBox()
        self.combo_mua.addItems(["Tất cả", "Mùa mưa", "Mùa nắng", "Mùa nước nổi", "Quanh năm"])
        filter_v_lay.addWidget(self.combo_mua)

        filter_v_lay.addStretch() # Đẩy các thành phần lên trên

        content_layout.addWidget(filter_frame, stretch=1) # Chiếm 1 phần không gian
        
        main_layout.addLayout(content_layout)

        # --- 3. HÀNG NÚT BẤM (Phía dưới cùng) ---
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
            "beo": self.chk_beo.isChecked(),
            "ngot": self.chk_ngot.isChecked(), 
            "vi": self.combo_vi.currentText(),
            "mua": self.combo_mua.currentText()
        }
        self.submitted.emit(data)