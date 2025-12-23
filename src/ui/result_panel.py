import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QHBoxLayout
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class ResultPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        self.title = QLabel("KẾT QUẢ GỢI Ý")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2E7D32;")
        layout.addWidget(self.title, alignment=Qt.AlignCenter)

        # Khu vực cuộn danh sách món ăn
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.container = QWidget()
        self.res_layout = QVBoxLayout(self.container)
        self.res_layout.addStretch() 
        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)

        self.btn_back = QPushButton("TƯ VẤN LẠI")
        self.btn_back.setStyleSheet("padding: 10px; background: #2E7D32; color: white; border-radius: 5px;")
        layout.addWidget(self.btn_back)

    def clear_results(self):
        """Xóa sạch các kết quả cũ"""
        while self.res_layout.count() > 1:
            item = self.res_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def add_dish_card(self, mon):
        """Tạo thẻ hiển thị món ăn"""
        card = QFrame() 
        card.setStyleSheet("background: white; border: 1px solid #ddd; border-radius: 12px; margin: 5px;")
        card_lay = QHBoxLayout(card)
        
        # Nội dung chữ
        info = QLabel(f"<b style='color:#1B5E20; font-size:18px;'>{mon['ten']}</b><br>"
                      f"📍 Đặc sản: {mon['dac_san']}<br>"
                      f"<i>{mon.get('mo_ta', '')}</i>")
        info.setWordWrap(True)
        info.setStyleSheet("border: none; padding: 5px;")
        
        card_lay.addWidget(info)
        # Chèn thẻ vào danh sách
        self.res_layout.insertWidget(self.res_layout.count() - 1, card)