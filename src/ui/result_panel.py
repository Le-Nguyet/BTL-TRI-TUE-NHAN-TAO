from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QHBoxLayout, QLineEdit
)
from PySide6.QtCore import Qt, Signal

class ResultPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.all_current_dishes = [] # Lưu trữ kết quả gốc để tìm kiếm
        layout = QVBoxLayout(self)
        
        # Thanh tìm kiếm
        search_lay = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm tên món ăn trong kết quả...")
        self.search_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #2E7D32;")
        self.search_input.textChanged.connect(self.filter_results)
        search_lay.addWidget(self.search_input)
        layout.addLayout(search_lay)

        # Khu vực hiển thị danh sách
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.container = QWidget()
        self.res_layout = QVBoxLayout(self.container)
        self.res_layout.addStretch() 
        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)

        # Nút điều hướng
        btn_lay = QHBoxLayout()
        self.btn_back = QPushButton("TƯ VẤN LẠI")
        self.btn_exit = QPushButton("THOÁT ỨNG DỤNG")
        
        style = "QPushButton { padding: 10px; color: white; border-radius: 5px; font-weight: bold; }"
        self.btn_back.setStyleSheet(style + "background: #2E7D32;")
        self.btn_exit.setStyleSheet(style + "background: #C62828;")
        
        btn_lay.addWidget(self.btn_back)
        btn_lay.addWidget(self.btn_exit)
        layout.addLayout(btn_lay)

    def show_dishes(self, dishes):
        self.all_current_dishes = dishes
        self.search_input.clear()
        self.render_cards(dishes)

    def filter_results(self, text):
        filtered = [d for d in self.all_current_dishes if text.lower() in d['ten'].lower()]
        self.render_cards(filtered)

    def render_cards(self, dishes):
        # Xóa sạch các widget cũ
        while self.res_layout.count() > 1:
            item = self.res_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        for mon in dishes:
            card = QFrame() # Sửa lỗi QFrame is not defined
            card.setStyleSheet("background: white; border: 1px solid #ddd; border-radius: 10px; margin: 5px;")
            lay = QHBoxLayout(card)
            info = QLabel(f"<b style='color:#1B5E20; font-size:16px;'>{mon['ten']}</b><br>📍 {mon['dac_san']}")
            lay.addWidget(info)
            self.res_layout.insertWidget(self.res_layout.count() - 1, card)