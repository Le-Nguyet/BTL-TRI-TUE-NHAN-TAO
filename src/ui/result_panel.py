import os
import webbrowser  # Thêm thư viện để mở web
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QScrollArea, QFrame, QHBoxLayout, QMessageBox)
from PySide6.QtCore import Qt, Signal  # Thêm Signal
from PySide6.QtGui import QPixmap, QFont, QGuiApplication

class ResultPanel(QWidget):
    # Tạo tín hiệu để báo cho MainWindow biết khi người dùng nhấn xem bản đồ
    view_map_signal = Signal(str)

    def __init__(self):
        super().__init__()
        # ... (Giữ nguyên phần init cũ của bạn) ...
        self.setStyleSheet("background-color: #F9FBF9;")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 20, 30, 30)

        self.title = QLabel("KẾT QUẢ TƯ VẤN MÓN ĂN ĐẶC SẢN")
        self.title.setStyleSheet("font-size: 28px; font-weight: bold; color: #1B5E20; margin-bottom: 10px;")
        self.layout.addWidget(self.title, alignment=Qt.AlignCenter)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")

        self.res_container = QWidget()
        self.res_layout = QVBoxLayout(self.res_container)
        self.res_layout.setSpacing(20)
        self.res_layout.setAlignment(Qt.AlignTop)

        self.scroll.setWidget(self.res_container)
        self.layout.addWidget(self.scroll)

        bottom_layout = QHBoxLayout()
        self.btn_back = QPushButton("🔍 TÌM KIẾM LẠI")
        self.btn_exit = QPushButton("❌ THOÁT")

        btn_style = "padding: 12px 30px; font-weight: bold; border-radius: 10px; font-size: 15px;"
        self.btn_back.setStyleSheet(btn_style + "background-color: #2E7D32; color: white;")
        self.btn_exit.setStyleSheet(btn_style + "background-color: #C62828; color: white;")

        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_exit.setCursor(Qt.PointingHandCursor)

        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_back)
        bottom_layout.addWidget(self.btn_exit)
        bottom_layout.addStretch()
        self.layout.addLayout(bottom_layout)

    def clear_results(self):
        while self.res_layout.count():
            item = self.res_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def show_dishes(self, dishes):
        self.clear_results()
        for mon in dishes:
            card = self.create_dish_card(mon)
            self.res_layout.addWidget(card)
            
    def _share_result(self, mon):
        text = f"Hệ chuyên gia gợi ý tôi món: {mon['ten']} tại {mon['tinh']}. Thật tuyệt vời!"
        QGuiApplication.clipboard().setText(text)
        QMessageBox.information(self, "Chia sẻ", "Đã sao chép thông tin món ăn vào bộ nhớ tạm!")

    def create_dish_card(self, mon):
        # Định nghĩa bộ icon để không bị lỗi NameError
        icons_mua = {
            "Mùa nước nổi": "🌊", "Mùa mưa": "🌧️", "Mùa khô": "☀️",
            "Mùa Tết": "🧧", "Mùa trái cây": "🍎"
        }

        card = QFrame()
        card.setMinimumHeight(350)
        card.setStyleSheet("QFrame { background-color: white; border-radius: 20px; border: 1px solid #D1D1D1; } QFrame:hover { border: 2px solid #2E7D32; }")

        main_h_lay = QHBoxLayout(card)
        main_h_lay.setContentsMargins(20, 20, 20, 20)
        main_h_lay.setSpacing(30)

        # --- BÊN TRÁI: HÌNH ẢNH ---
        left_widget = QWidget()
        left_widget.setFixedWidth(600)
        left_lay = QVBoxLayout(left_widget)

        img_label = QLabel()
        img_label.setFixedSize(600, 450)
        img_label.setScaledContents(True)
        img_label.setStyleSheet("border-radius: 10px; border: 1px solid #EEEEEE;")

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        img_path = os.path.normpath(os.path.join(base_dir, "assets", "images", mon.get('hinh_anh', 'default.png')))
        pixmap = QPixmap(img_path)
        if not pixmap.isNull(): 
            img_label.setPixmap(pixmap)

        name_label = QLabel(mon['ten'].upper())
        name_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #1B5E20; margin-top: 10px;")
        name_label.setAlignment(Qt.AlignCenter)

        left_lay.addWidget(img_label)
        left_lay.addWidget(name_label)

        # --- BÊN PHẢI: THÔNG TIN CHI TIẾT ---
        right_widget = QWidget()
        right_lay = QVBoxLayout(right_widget)

        # Tiêu đề món ăn (Bên phải)
        name = QLabel(mon['ten'].upper())
        name.setStyleSheet("font-size: 22px; font-weight: bold; color: #2E7D32;")
        right_lay.addWidget(name)

        # Tỉnh và Mùa
        icon_m = icons_mua.get(mon.get('mua'), "📅")
        info_style = "font-size: 14px; color: #444;"
        right_lay.addWidget(QLabel(f"📍 <b>Tỉnh:</b> {mon['tinh']}", styleSheet=info_style))
        right_lay.addWidget(QLabel(f"{icon_m} <b>Mùa:</b> {mon.get('mua')}", styleSheet=info_style))

        # 1. Giải thích lý do (Explanation Facility)
        explanation = QFrame()
        explanation.setStyleSheet("background-color: #F1F8E9; border-left: 4px solid #4CAF50; border-radius: 0px;")
        ex_lay = QVBoxLayout(explanation)
        ex_text = QLabel(
            f"💡 <b>Lý do gợi ý:</b> Vì bạn thích vị <i>{mon.get('vi',[''])[0]}</i>, "
            f"hệ thống nhận thấy {mon['ten']} là đặc sản tại {mon['tinh']} vào {mon.get('mua')}."
        )
        ex_text.setWordWrap(True)
        ex_text.setStyleSheet("border: none; color: #2E7D32; font-size: 13px;")
        ex_lay.addWidget(ex_text)
        right_lay.addWidget(explanation)

        # 2. Gợi ý phụ (Related Suggestions)
        suggest_text = QLabel(f"🍴 <b>Ăn kèm:</b> {mon.get('ten')} ngon nhất khi dùng nóng với nước chấm đặc trưng.")
        suggest_text.setWordWrap(True)
        suggest_text.setStyleSheet("font-size: 13px; color: #666; font-style: italic; border: none;")
        right_lay.addWidget(suggest_text)

        # --- PHẦN MÔ TẢ (Đã chuyển lên trên nút bấm) ---
        desc_box = QFrame()
        desc_box.setStyleSheet("background-color: #F1F8E9; border-radius: 10px; margin-top: 10px;")
        desc_lay = QVBoxLayout(desc_box)
        desc_label = QLabel(mon['mo_ta'])
        desc_label.setWordWrap(True)
        desc_lay.addWidget(desc_label)
        right_lay.addWidget(desc_box)

        right_lay.addStretch() # Đẩy các nút bấm xuống dưới cùng của card

        # --- HÀNG NÚT BẤM (Nằm dưới mô tả) ---
        btn_lay = QHBoxLayout()
        
        btn_map = QPushButton("📍 XEM ĐỊA CHỈ QUÁN")
        btn_map.setCursor(Qt.PointingHandCursor)
        btn_map.setStyleSheet("""
            QPushButton {
                background-color: #1976D2; color: white; font-weight: bold; 
                padding: 10px; border-radius: 8px; font-size: 14px;
            }
            QPushButton:hover { background-color: #1565C0; }
        """)
        btn_map.clicked.connect(lambda: self.view_map_signal.emit(f"{mon['ten']} tại {mon['tinh']}"))

        btn_share = QPushButton("📤 CHIA SẺ")
        btn_share.setCursor(Qt.PointingHandCursor)
        btn_share.setStyleSheet("""
            QPushButton {
                background: #FB8C00; color: white; font-weight: bold; 
                padding: 10px; border-radius: 8px; font-size: 14px;
            }
            QPushButton:hover { background-color: #EF6C00; }
        """)
        btn_share.clicked.connect(lambda checked, m=mon: self._share_result(m))

        btn_lay.addWidget(btn_map)
        btn_lay.addWidget(btn_share)
        right_lay.addLayout(btn_lay)

        main_h_lay.addWidget(left_widget)
        main_h_lay.addWidget(right_widget)
        
        return card

    