import os
from PySide6.QtGui import QFontDatabase, QFont

def load_fonts():
    # Lấy đường dẫn tuyệt đối để tránh lỗi khi chạy từ các thư mục khác nhau
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Đường dẫn: src/ui -> src -> root -> assets/fonts/Nunito-ExtraBold.ttf
    font_path = os.path.normpath(os.path.join(current_dir, "../../assets/fonts/Nunito-ExtraBold.ttf"))
    
    font_id = QFontDatabase.addApplicationFont(font_path)
    
    if font_id != -1:
        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            return families[0]
    
    print(f"Cảnh báo: Không tìm thấy font tại {font_path}. Sử dụng Arial thay thế.")
    return "Arial"

def get_main_style():
    family = load_fonts()
    return f"""
        QWidget {{
            font-family: '{family}';
            font-size: 14px;
            background-color: #f5f5f5;
        }}
        QPushButton {{
            background-color: #2c3e50;
            color: white;
            border-radius: 5px;
            padding: 8px 15px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: #34495e;
        }}
        QLabel {{
            color: #333;
        }}
    """