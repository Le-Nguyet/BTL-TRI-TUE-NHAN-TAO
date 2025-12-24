from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
from PySide6.QtCore import Qt

class ResultPanel(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        
        # Tiêu đề kết quả
        title = QLabel("DANH SÁCH MÓN ĂN GỢI Ý")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2E7D32; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        lay.addWidget(title)

        self.scroll = QScrollArea()
        self.container = QWidget()
        self.res_layout = QVBoxLayout(self.container)
        self.res_layout.setAlignment(Qt.AlignTop) # Đẩy các card lên phía trên
        self.scroll.setWidget(self.container)
        self.scroll.setWidgetResizable(True)
        lay.addWidget(self.scroll)

        self.btn_back = QPushButton("QUAY LẠI")
        self.btn_exit = QPushButton("THOÁT")
        
        # Style cho nút
        button_style = "padding: 10px; font-weight: bold; border-radius: 5px;"
        self.btn_back.setStyleSheet(button_style + "background-color: #f0f0f0;")
        self.btn_exit.setStyleSheet(button_style + "background-color: #FFCDD2; color: #C62828;")
        
        lay.addWidget(self.btn_back)
        lay.addWidget(self.btn_exit)

    def clear_results(self):
        while self.res_layout.count() > 0:
            item = self.res_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    def show_dishes(self, dishes):
        for mon in dishes:
            # Format danh sách vị thành chuỗi để hiển thị
            vi_str = ", ".join(mon['vi']) if isinstance(mon['vi'], list) else mon['vi']
            
            # Tạo thẻ hiển thị món ăn chi tiết
            info_text = (
                f"<b style='font-size: 16px; color: #1B5E20;'>🍲 {mon['ten']}</b><br>"
                f"📍 <b>Tỉnh:</b> {mon['tinh']}<br>"
                f"👅 <b>Vị đặc trưng:</b> {vi_str}<br>"
                f"🍂 <b>Mùa ngon nhất:</b> {mon['mua']}<br>"
                f"📝 <b>Mô tả:</b> {mon.get('mo_ta', 'Đang cập nhật...')}"
            )
            
            card = QLabel(info_text)
            card.setWordWrap(True)
            card.setStyleSheet("""
                QLabel {
                    background: #FFFFFF; 
                    border: 1px solid #C8E6C9; 
                    padding: 15px; 
                    border-radius: 12px; 
                    margin-bottom: 10px;
                }
            """)
            self.res_layout.addWidget(card)