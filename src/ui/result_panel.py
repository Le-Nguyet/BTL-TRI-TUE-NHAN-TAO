import os
import webbrowser
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QScrollArea, QFrame, QHBoxLayout, QMessageBox, QFileDialog)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QFont, QGuiApplication

class ResultPanel(QWidget):
    view_map_signal = Signal(str)

    def __init__(self):
        super().__init__()
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
        
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_back)
        bottom_layout.addWidget(self.btn_exit)
        bottom_layout.addStretch()
        self.layout.addLayout(bottom_layout)

    def clear_results(self):
        while self.res_layout.count():
            item = self.res_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    def show_dishes(self, dishes):
        self.clear_results()
        for mon in dishes:
            card = self.create_dish_card(mon)
            self.res_layout.addWidget(card)

    def _share_result(self, mon, card_widget):
        pixmap = card_widget.grab()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Lưu kết quả tư vấn", f"DacSan_{mon['ten']}.png", "Images (*.png *.jpg)"
        )

        if file_path:
            if pixmap.save(file_path):
                confirm = QMessageBox(self)
                confirm.setIcon(QMessageBox.Question)
                confirm.setWindowTitle("Lưu thành công")
                confirm.setText(f"<b style='color: #2E7D32; font-size: 16px;'>Đã lưu ảnh món {mon['ten']}!</b>")
                confirm.setInformativeText("Bạn có muốn mở Zalo để gửi ảnh ngay không?")
                
                # Style cho nút bấm không bị trắng
                confirm.setStyleSheet("QMessageBox { background-color: white; } QPushButton { padding: 8px 20px; font-weight: bold; min-width: 120px; }")
                
                yes_button = confirm.addButton("Có, gửi qua Zalo", QMessageBox.YesRole)
                yes_button.setStyleSheet("background-color: #0068FF; color: white; border: none;")
                
                no_button = confirm.addButton("Không, chỉ lưu thôi", QMessageBox.NoRole)
                no_button.setStyleSheet("background-color: #E0E0E0; color: #333; border: 1px solid #CCC;")

                confirm.exec()
                if confirm.clickedButton() == yes_button:
                    os.startfile(os.path.dirname(file_path))
                    webbrowser.open("zalo://")
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể lưu được ảnh.")

    def create_dish_card(self, mon):
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
        if not pixmap.isNull(): img_label.setPixmap(pixmap)

        name_label = QLabel(mon['ten'].upper())
        name_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #1B5E20; margin-top: 10px;")
        name_label.setAlignment(Qt.AlignCenter)
        left_lay.addWidget(img_label)
        left_lay.addWidget(name_label)

        # --- BÊN PHẢI: THÔNG TIN ---
        right_widget = QWidget()
        right_lay = QVBoxLayout(right_widget)

        name = QLabel(mon['ten'].upper())
        name.setStyleSheet("font-size: 22px; font-weight: bold; color: #2E7D32;")
        right_lay.addWidget(name)

        # 1. HIỂN THỊ CÂY SUY LUẬN (REASONING EXPLANATION)
        reasoning_box = QFrame()
        reasoning_box.setStyleSheet("background-color: #E3F2FD; border-left: 5px solid #2196F3; border-radius: 0px;")
        res_v_lay = QVBoxLayout(reasoning_box)
        steps = f"""
        <div style='line-height: 160%;'>
            🧠 <b>LỘ TRÌNH SUY LUẬN CHUYÊN GIA:</b><br>
            ❶ <b>Ngữ cảnh:</b> {mon['tinh']} ➔ {mon.get('mua')} <br>
            ❷ <b>Phân loại:</b> <span style='color: #E91E63; font-weight: bold;'>{mon.get('loai')}</span><br>
            ❸ <b>Nguyên liệu chính:</b> {mon.get('nlc')}<br>
            ❹ <b>Thành phần phụ:</b> {mon.get('nlp')}<br>
            ❺ <b>Hương vị đặc trưng:</b> {mon.get('vi')}<br>
            ➔ ✅ <b>KẾT LUẬN:</b> Gợi ý món <b>{mon['ten']}</b>
        </div>
        """
        res_label = QLabel(steps)
        res_label.setWordWrap(True)
        res_label.setStyleSheet("border: none; color: #1565C0; font-size: 13px;")
        res_v_lay.addWidget(res_label)
        right_lay.addWidget(reasoning_box)

        # Gợi ý phụ & Mô tả
        suggest_text = QLabel(f"🍴 <b>Ăn kèm:</b> {mon.get('ten')} dùng kèm với nước chấm đặc trưng.")
        suggest_text.setStyleSheet("font-size: 13px; color: #666; font-style: italic; margin-top: 5px;")
        right_lay.addWidget(suggest_text)

        desc_box = QFrame()
        desc_box.setStyleSheet("background-color: #F1F8E9; border-radius: 10px; margin-top: 5px;")
        desc_lay = QVBoxLayout(desc_box)
        desc_label = QLabel(mon['mo_ta'])
        desc_label.setWordWrap(True)
        desc_lay.addWidget(desc_label)
        right_lay.addWidget(desc_box)

        right_lay.addStretch()

        # Hàng nút bấm
        btn_lay = QHBoxLayout()
        btn_map = QPushButton("📍 XEM ĐỊA CHỈ QUÁN")
        btn_map.setStyleSheet("background-color: #1976D2; color: white; font-weight: bold; padding: 10px; border-radius: 8px;")
        btn_map.clicked.connect(lambda: self.view_map_signal.emit(f"{mon['ten']} tại {mon['tinh']}"))

        btn_share = QPushButton("📤 CHIA SẺ")
        btn_share.setStyleSheet("background: #FB8C00; color: white; font-weight: bold; padding: 10px; border-radius: 8px;")
        btn_share.clicked.connect(lambda checked, m=mon, c=card: self._share_result(m, c))

        btn_lay.addWidget(btn_map)
        btn_lay.addWidget(btn_share)
        right_lay.addLayout(btn_lay)

        main_h_lay.addWidget(left_widget)
        main_h_lay.addWidget(right_widget)
        return card