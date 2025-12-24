from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QComboBox, QHBoxLayout
from PySide6.QtCore import Qt, Signal

class InputPanel(QWidget):
    submitted = Signal(dict)

    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        
        # Tiêu đề chính của đề tài [cite: 6]
        title = QLabel("TƯ VẤN ĐẶC SẢN ĐBSCL")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E7D32;")
        lay.addWidget(title, alignment=Qt.AlignCenter)

        sub_title = QLabel("Chọn sở thích ẩm thực của bạn:")
        sub_title.setStyleSheet("font-size: 16px; font-style: italic;")
        lay.addWidget(sub_title, alignment=Qt.AlignCenter)

        # Các tùy chọn lọc dựa trên dữ liệu trích xuất [cite: 22]
        self.chk_nuoc = QCheckBox("Món có nước (Bún, lẩu, cháo...)")
        self.chk_cay = QCheckBox("Thích vị cay nồng")
        self.chk_beo = QCheckBox("Thích vị béo (Nước cốt dừa, chao...)")
        self.chk_ngot = QCheckBox("Món ngọt / Bánh quà biếu")

        # Chọn tỉnh thành cụ thể trong khu vực ĐBSCL [cite: 7, 32]
        self.cbo_tinh = QComboBox()
        self.cbo_tinh.addItems([
            "Tất cả tỉnh thành", "An Giang", "Đồng Tháp", "Cần Thơ", 
            "Sóc Trăng", "Kiên Giang", "Bến Tre", "Long An", 
            "Tiền Giang", "Trà Vinh", "Bạc Liêu"
        ])
        self.cbo_tinh.setStyleSheet("font-size: 16px; padding: 5px; margin: 10px;")

        # Định dạng giao diện
        for chk in [self.chk_nuoc, self.chk_cay, self.chk_beo, self.chk_ngot]:
            chk.setStyleSheet("font-size: 17px; margin: 5px;")
            lay.addWidget(chk, alignment=Qt.AlignLeft)

        lay.addWidget(QLabel("Chọn địa phương muốn khám phá:"))
        lay.addWidget(self.cbo_tinh)

        # Nút bấm điều khiển [cite: 37]
        self.btn_go = QPushButton("GỢI Ý MÓN ĂN")
        self.btn_go.setStyleSheet("""
            QPushButton { background-color: #2E7D32; color: white; font-weight: bold; padding: 10px; border-radius: 5px; }
            QPushButton:hover { background-color: #388E3C; }
        """)
        
        self.btn_back = QPushButton("QUAY LẠI")
        
        lay.addWidget(self.btn_go)
        lay.addWidget(self.btn_back)

        self.btn_go.clicked.connect(self.send_data)

    def send_data(self):
        # Gửi dữ liệu về engine xử lý luật [cite: 36]
        self.submitted.emit({
            "nuoc": self.chk_nuoc.isChecked(),
            "cay": self.chk_cay.isChecked(),
            "beo": self.chk_beo.isChecked(),
            "ngot": self.chk_ngot.isChecked(),
            "tinh": self.cbo_tinh.currentText()
        })