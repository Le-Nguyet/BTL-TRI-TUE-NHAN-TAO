from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QGroupBox, QHBoxLayout
from PySide6.QtCore import Qt, Signal

class InputPanel(QWidget):
    # Tín hiệu gửi dữ liệu về MainWindow
    submitted = Signal(dict)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("BẠN MUỐN ĂN GÌ?")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #1B5E20;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # Nhóm chọn đặc điểm
        self.group = QGroupBox("Khẩu vị của bạn")
        group_lay = QVBoxLayout()
        self.chk_nuoc = QCheckBox("Món có nước (Lẩu, bún...)")
        self.chk_cay = QCheckBox("Thích vị cay")
        
        for chk in [self.chk_nuoc, self.chk_cay]:
            chk.setStyleSheet("font-size: 18px; padding: 5px;")
            group_lay.addWidget(chk)
        self.group.setLayout(group_lay)
        layout.addWidget(self.group)

        # Nút bấm
        btns = QHBoxLayout()
        self.btn_back = QPushButton("QUAY LẠI")
        self.btn_go = QPushButton("GỢI Ý MÓN ĂN")
        style = "QPushButton { padding: 12px; font-weight: bold; border-radius: 8px; }"
        self.btn_back.setStyleSheet(style + "background: #757575; color: white;")
        self.btn_go.setStyleSheet(style + "background: #2E7D32; color: white;")
        
        btns.addWidget(self.btn_back)
        btns.addWidget(self.btn_go)
        layout.addLayout(btns)

        self.btn_go.clicked.connect(self._send_data)

    def _send_data(self):
        # Gửi đúng từ khóa khớp với JSON
        data = {
            "loai": "Nước" if self.chk_nuoc.isChecked() else "Khô",
            "cay": self.chk_cay.isChecked()
        }
        self.submitted.emit(data)