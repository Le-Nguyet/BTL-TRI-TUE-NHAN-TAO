#Tệp quản lý "thời trang" của ứng dụng (màu sắc, phông chữ, kích thước nút bấm).
import os
from PySide6.QtGui import QFontDatabase

def load_fonts():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Tìm đến assets/fonts/Nunito-ExtraBold.ttf từ src/ui
    font_path = os.path.normpath(os.path.join(current_dir, "../../assets/fonts/Nunito-ExtraBold.ttf"))
    
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id != -1:
        families = QFontDatabase.applicationFontFamilies(font_id)
        if families: return families[0]
    return "Arial"

def get_main_style():
    family = load_fonts()
    return f"""
        QWidget {{ font-family: '{family}'; font-size: 14px; background-color: #f5f5f5; }}
        QPushButton {{ background-color: #2E7D32; color: white; border-radius: 8px; padding: 10px; font-weight: bold; }}
        QPushButton:hover {{ background-color: #1B5E20; }}
    """