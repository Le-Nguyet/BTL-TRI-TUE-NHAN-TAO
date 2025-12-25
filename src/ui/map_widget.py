import os
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont, QPen
from PySide6.QtCore import Qt, Signal, QPointF, QRectF

class MekongDeltaMap(QWidget):
    provinceSelected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        # Đường dẫn ảnh bản đồ
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        img_path = os.path.join(base_dir, "assets", "images", "ban-do-mien-tay.png")
        
        self.pixmap = QPixmap(img_path)
        self.selected_province = None
        
        # TỌA ĐỘ ĐÃ ĐIỀU CHỈNH ĐỂ NẰM GIỮA TÂM CÁC TỈNH
        # Tỷ lệ (x, y) dựa trên kích thước thực của ảnh bản đồ
        self.province_coords = {
            "An Giang": (0.40, 0.26),
            "Đồng Tháp": (0.59, 0.20),
            "Long An": (0.78, 0.15),
            "Tiền Giang": (0.76, 0.26),
            "Bến Tre": (0.90, 0.38),
            "Vĩnh Long": (0.70, 0.41),
            "Trà Vinh": (0.82, 0.52),
            "Cần Thơ": (0.55, 0.42),
            "Hậu Giang": (0.57, 0.54),
            "Sóc Trăng": (0.68, 0.64),
            "Bạc Liêu": (0.55, 0.72),
            "Cà Mau": (0.36, 0.81),
            "Kiên Giang": (0.43, 0.50)
        }

    def get_render_info(self):
        """Tính toán vị trí ảnh thực tế để chấm tròn không bị lệch khi co giãn"""
        if self.pixmap.isNull():
            return 0, 0, 1, 1
        
        # Lấy kích thước ảnh sau khi scale giữ tỷ lệ
        scaled_size = self.pixmap.size()
        scaled_size.scale(self.size(), Qt.KeepAspectRatio)
        
        # Tính khoảng bù (offset) để căn giữa bản đồ
        ox = (self.width() - scaled_size.width()) / 2
        oy = (self.height() - scaled_size.height()) / 2
        
        return ox, oy, scaled_size.width(), scaled_size.height()

    def paintEvent(self, event):
        if self.pixmap.isNull():
            return

        painter = QPainter(self)
        # Bật khử răng cưa và làm mượt ảnh khi phóng to
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        ox, oy, sw, sh = self.get_render_info()

        # Vẽ bản đồ
        target_rect = QRectF(ox, oy, sw, sh)
        painter.drawPixmap(target_rect, self.pixmap, QRectF(self.pixmap.rect()))

        # Vẽ các dấu chấm tròn nằm giữa tỉnh
        for name, (px, py) in self.province_coords.items():
            # Tính tọa độ thực trên màn hình
            rx = ox + (px * sw)
            ry = oy + (py * sh)
            
            # Cấu hình màu sắc
            if name == self.selected_province:
                color = QColor(231, 76, 60) # Màu đỏ khi chọn
                radius = 10
                painter.setPen(QPen(Qt.white, 2))
            else:
                color = QColor(46, 204, 113, 200) # Màu xanh lá mặc định
                radius = 8
                painter.setPen(Qt.transparent)

            painter.setBrush(color)
            # Vẽ hình tròn với tâm là rx, ry để đảm bảo nằm chính giữa
            painter.drawEllipse(QPointF(rx, ry), radius, radius)


    def mousePressEvent(self, event):
        """Xử lý khi người dùng click vào dấu chấm"""
        pos = event.position()
        ox, oy, sw, sh = self.get_render_info()
        
        found = False
        for name, (px, py) in self.province_coords.items():
            tx = ox + (px * sw)
            ty = oy + (py * sh)
            
            # Kiểm tra khoảng cách click (bán kính nhạy 25px)
            distance = ((pos.x() - tx)**2 + (pos.y() - ty)**2)**0.5
            if distance < 25:
                self.selected_province = name
                self.provinceSelected.emit(name)
                self.update()
                found = True
                break