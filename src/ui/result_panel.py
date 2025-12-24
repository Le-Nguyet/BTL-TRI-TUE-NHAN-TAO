from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
from PySide6.QtCore import Qt

class ResultPanel(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        
        self.scroll = QScrollArea()
        self.container = QWidget()
        self.res_layout = QVBoxLayout(self.container)
        self.scroll.setWidget(self.container)
        self.scroll.setWidgetResizable(True)
        lay.addWidget(self.scroll)

        self.btn_back = QPushButton("QUAY LẠI")
        self.btn_exit = QPushButton("THOÁT")
        lay.addWidget(self.btn_back)
        lay.addWidget(self.btn_exit)

    def clear_results(self):
        while self.res_layout.count() > 0:
            item = self.res_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    def show_dishes(self, dishes):
        for mon in dishes:
            card = QLabel(f"🍲 {mon['ten']} - Đặc sản: {mon['dac_san']}\n{mon['mo_ta']}")
            card.setWordWrap(True)
            card.setStyleSheet("background: white; border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin-bottom: 10px;")
            self.res_layout.addWidget(card)