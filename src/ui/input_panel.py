from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QHBoxLayout
from PySide6.QtCore import Qt, Signal

class InputPanel(QWidget):
    submitted = Signal(dict)

    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        
        title = QLabel("BẠN MUỐN ĂN GÌ?")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E7D32;")
        lay.addWidget(title, alignment=Qt.AlignCenter)

        self.chk_nuoc = QCheckBox("Món có nước (Lẩu, bún...)")
        self.chk_cay = QCheckBox("Thích vị cay")
        
        for chk in [self.chk_nuoc, self.chk_cay]:
            chk.setStyleSheet("font-size: 18px;")
            lay.addWidget(chk, alignment=Qt.AlignCenter)

        self.btn_go = QPushButton("GỢI Ý MÓN ĂN")
        self.btn_back = QPushButton("QUAY LẠI")
        
        lay.addWidget(self.btn_go)
        lay.addWidget(self.btn_back)

        self.btn_go.clicked.connect(self.send_data)

    def send_data(self):
        self.submitted.emit({
            "nuoc": self.chk_nuoc.isChecked(),
            "cay": self.chk_cay.isChecked()
        })