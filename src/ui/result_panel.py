import os
import webbrowser
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

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

        ## Cấu hình ScrollArea thông minh
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("border: none; background: transparent;")

        self.res_container = QWidget()
        self.res_layout = QVBoxLayout(self.res_container)
        self.res_layout.setSpacing(15)
        self.res_layout.setAlignment(Qt.AlignTop)

        self.scroll.setWidget(self.res_container)
        self.layout.addWidget(self.scroll)

       # --- ĐỊNH VỊ NÚT BẤM DƯỚI CÙNG ---
        bottom_layout = QHBoxLayout()
        self.btn_back = QPushButton("🔍 TÌM KIẾM LẠI")
        self.btn_exit = QPushButton("❌ THOÁT")
        
        btn_style = "padding: 12px 30px; font-weight: bold; border-radius: 10px; font-size: 15px;"
        self.btn_back.setStyleSheet(btn_style + "background-color: #2E7D32; color: white;")
        self.btn_exit.setStyleSheet(btn_style + "background-color: #C62828; color: white;")

        # Tìm kiếm lại bên trái, Thoát bên phải
        bottom_layout.addWidget(self.btn_back) 
        bottom_layout.addStretch() 
        bottom_layout.addWidget(self.btn_exit) 
        self.layout.addLayout(bottom_layout)

        # Kết nối sự kiện nhấp nháy cho 2 nút điều hướng
        self.btn_back.clicked.connect(lambda: self.flash_effect(self.btn_back, "#2E7D32", "#66BB6A"))
        self.btn_exit.clicked.connect(lambda: self.flash_effect(self.btn_exit, "#C62828", "#EF5350"))

   # SỬ DỤNG QSS ĐỂ TẠO HIỆU ỨNG NHẤP NHÁY KHI HOVER (LIA CHUỘT)
        self.btn_back.setStyleSheet("""
            QPushButton {
                padding: 12px 30px; font-weight: bold; border-radius: 10px; font-size: 15px; 
                background-color: #2E7D32; color: white;
            }
            QPushButton:hover {
                background-color: #45a049;  /* Màu sáng hơn khi lia chuột tới */
                border: 2px solid white;
            }
        """)

        self.btn_exit.setStyleSheet("""
            QPushButton {
                padding: 12px 30px; font-weight: bold; border-radius: 10px; font-size: 15px; 
                background-color: #C62828; color: white;
            }
            QPushButton:hover {
                background-color: #e53935;  /* Màu đỏ tươi hơn khi lia chuột tới */
                border: 2px solid white;
            }
        """)

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
        left_widget.setFixedWidth(500) # Điều chỉnh lại độ rộng cho cân đối
        left_lay = QVBoxLayout(left_widget)
        
        img_label = QLabel()
        img_label.setFixedSize(480, 360) # Kích thước ảnh chuẩn 4:3
        img_label.setScaledContents(True)
        img_label.setStyleSheet("border-radius: 10px; border: 1px solid #EEEEEE; background-color: #f0f0f0;")

        # --- XỬ LÝ ĐƯỜNG DẪN ẢNH CHUẨN ---
        # Lấy thư mục gốc của dự án (Project Root) dựa trên vị trí file main.py
        import os
        # Đường dẫn từ file hiện tại (src/ui/result_panel.py) lên 2 cấp để ra gốc dự án
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        
        # Tên file ảnh từ database (nếu rỗng thì dùng default.png) 
        file_name = mon.get('image_path')
        if not file_name or str(file_name).strip() == "" or file_name == "None":
            file_name = "default.png"
            
        img_path = os.path.join(base_dir, "assets", "images", file_name)
        img_path = os.path.normpath(img_path)

        # Kiểm tra và load ảnh
        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            print(f"⚠️ Cảnh báo: Không tìm thấy ảnh tại: {img_path}")
            # Thử tìm ảnh default nếu ảnh chính lỗi
            default_path = os.path.join(base_dir, "assets", "images", "default.png")
            pixmap = QPixmap(default_path)
            if pixmap.isNull():
                img_label.setText("❌ Không có ảnh")
            else:
                img_label.setPixmap(pixmap)
        else:
            img_label.setPixmap(pixmap)

        name_label = QLabel(mon['ten'].upper())
        name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #E91E63; margin-top: 10px;")
        name_label.setAlignment(Qt.AlignCenter)
        
        left_lay.addWidget(img_label)
        left_lay.addWidget(name_label)

        # --- BÊN PHẢI: THÔNG TIN ---
        right_widget = QWidget()
        right_lay = QVBoxLayout(right_widget)

        name = QLabel(mon['ten'].upper())
        name.setStyleSheet("font-size: 22px; font-weight: bold; color: #2E7D32;")
        right_lay.addWidget(name)

        # 1. HIỂN THỊ CÂY SUY LUẬN 
        reasoning_box = QFrame()
        reasoning_box.setStyleSheet("background-color: #E3F2FD; border-left: 5px solid #2196F3; border-radius: 0px;")
        res_v_lay = QVBoxLayout(reasoning_box)
        
        # 2. GÓC NHÌN HỆ CHUYÊN GIA
        expert_box = QFrame()
        expert_box.setStyleSheet("background-color: #F1F8E9; border-left: 5px solid #4CAF50; border-radius: 0px; margin-top: 10px;")
        expert_lay = QVBoxLayout(expert_box)
        expert_text = f"""
        <div style='line-height: 150%;'>
            <b style='color: #1B5E20;'>❶ GÓC NHÌN "HỆ CHUYÊN GIA"</b><br>
            • <b> {mon.get('mo_ta', 'Đang cập nhật mô tả chuyên sâu...')}<br>
        </div>
        """
        expert_label = QLabel(expert_text)
        expert_label.setWordWrap(True)
        expert_lay.addWidget(expert_label)
        right_lay.addWidget(expert_box)

        steps = f"""
        <div style='line-height: 160%;'>
            ❷ 🧠 <b>LỘ TRÌNH SUY LUẬN CHUYÊN GIA:</b><br>
            • <b>Ngữ cảnh:</b> {mon['tinh']} ➔ {mon.get('mua')} <br>
            • <b>Phân loại:</b> {mon.get('loai')}<br>
            • <b>Nguyên liệu chính:</b> {mon.get('nlc')}<br>
            • <b>Thành phần phụ:</b> {mon.get('nlp')}<br>
            • <b>Hương vị đặc trưng:</b> {mon.get('vi')}<br>
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

        # 3. KẾT LUẬN & ĐÁNH GIÁ PHÙ HỢP
        match_box = QLabel(f"""
            <div style='margin-top: 10px; line-height: 140%; color: #E65100;'>
                <b>❸ TẠI SAO MÓN NÀY KHỚP VỚI BẠN?</b><br>
                ✅ Hệ thống đã lọc bỏ các món khác để chọn ra đặc sản <b>{mon['ten']}</b> 
                phù hợp nhất với vùng đất {mon['tinh']} bạn tìm kiếm.
            </div>
        """)
        match_box.setWordWrap(True)
        right_lay.addWidget(match_box)

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