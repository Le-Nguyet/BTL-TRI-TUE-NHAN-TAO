from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt

class ConsultWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # 1. Cơ sở tri thức đơn giản (Knowledge Base)
        self.data_mon_an = [
            {"ten": "Lẩu Mắm", "loai": "Nước", "vi": "Mặn", "dac_san": "An Giang/Cần Thơ"},
            {"ten": "Bún Mắm", "loai": "Nước", "vi": "Mặn", "dac_san": "Trà Vinh/Sóc Trăng"},
            {"ten": "Chuột Đồng Nướng", "loai": "Khô", "vi": "Cay", "dac_san": "Đồng Tháp"},
            {"ten": "Cá Linh Bông Điên Điển", "loai": "Nước", "vi": "Chua", "dac_san": "An Giang"},
            {"ten": "Hủ Tiếu Sa Đéc", "loai": "Nước", "vi": "Ngọt", "dac_san": "Đồng Tháp"},
            {"ten": "Bánh Xèo Cao Lãnh", "loai": "Khô", "vi": "Béo", "dac_san": "Đồng Tháp"}
        ]

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        # Tiêu đề
        title = QLabel("BẠN MUỐN ĂN GÌ HÔM NAY?")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #1B5E20;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # --- Khu vực chọn đặc điểm (Luật suy diễn) ---
        self.chk_nuoc = QCheckBox("Món có nước (Lẩu, bún, hủ tiếu...)")
        self.chk_cay = QCheckBox("Thích vị cay nồng")
        self.chk_chua = QCheckBox("Thích vị chua thanh")
        
        checkbox_style = "QCheckBox { font-size: 18px; color: #333; } QCheckBox::indicator { width: 25px; height: 25px; }"
        for chk in [self.chk_nuoc, self.chk_cay, self.chk_chua]:
            chk.setStyleSheet(checkbox_style)
            layout.addWidget(chk)

        # --- Nút hành động ---
        btn_layout = QHBoxLayout()
        
        self.btn_tu_van = QPushButton("ĐƯA RA GỢI Ý")
        self.btn_tu_van.setStyleSheet("background-color: #2E7D32; color: white; padding: 15px; font-weight: bold; border-radius: 10px;")
        self.btn_tu_van.clicked.connect(self.thuc_hien_suy_dien)

        self.btn_back = QPushButton("QUAY LẠI")
        self.btn_back.setStyleSheet("background-color: #757575; color: white; padding: 15px; border-radius: 10px;")

        btn_layout.addWidget(self.btn_back)
        btn_layout.addWidget(self.btn_tu_van)
        layout.addLayout(btn_layout)

        # --- Hiển thị kết quả ---
        self.lbl_ket_qua = QLabel("Kết quả sẽ hiển thị ở đây...")
        self.lbl_ket_qua.setStyleSheet("font-size: 20px; color: #d32f2f; font-style: italic; border: 2px dashed #ccc; padding: 20px;")
        self.lbl_ket_qua.setWordWrap(True)
        self.lbl_ket_qua.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_ket_qua)

    def thuc_hien_suy_dien(self):
        """Công cụ suy diễn (Inference Engine) dựa trên luật Forward Chaining"""
        ket_qua = []
        
        # Lấy điều kiện từ người dùng
        muon_an_nuoc = self.chk_nuoc.isChecked()
        thich_cay = self.chk_cay.isChecked()
        thich_chua = self.chk_chua.isChecked()

        # Duyệt qua cơ sở tri thức (Knowledge Base)
        for mon in self.data_mon_an:
            # Luật 1: Món nước
            match_loai = (mon["loai"] == "Nước") if muon_an_nuoc else (mon["loai"] == "Khô")
            
            # Luật 2: Vị cay
            match_vi = True
            if thich_cay and mon["vi"] != "Cay": match_vi = False
            if thich_chua and mon["vi"] != "Chua": match_vi = False

            if match_loai and match_vi:
                ket_qua.append(f"<b>{mon['ten']}</b> (Đặc sản: {mon['dac_san']})")

        # Hiển thị
        if ket_qua:
            self.lbl_ket_qua.setText("Hệ chuyên gia gợi ý cho bạn:<br>" + "<br>".join(ket_qua))
        else:
            self.lbl_ket_qua.setText("Rất tiếc, chưa tìm thấy món phù hợp với yêu cầu này!")