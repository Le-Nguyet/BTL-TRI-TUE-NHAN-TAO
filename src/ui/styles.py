import os
from PySide6.QtGui import QFontDatabase

def load_fonts():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_dir = os.path.normpath(os.path.join(current_dir, "../../assets/fonts/"))
    
    # Đường dẫn tới 2 file font
    reg_path = os.path.join(font_dir, "Nunito-Regular.ttf")
    bold_path = os.path.join(font_dir, "Nunito-ExtraBold.ttf")
    
    # Font dự phòng chuẩn tiếng Việt
    fallback = "Segoe UI" if os.name == 'nt' else "Arial"

    # Nạp font chữ thường (Regular)
    font_id_reg = QFontDatabase.addApplicationFont(reg_path)
    # Nạp font chữ đậm (ExtraBold)
    font_id_bold = QFontDatabase.addApplicationFont(bold_path)

    if font_id_reg != -1:
        families = QFontDatabase.applicationFontFamilies(font_id_reg)
        if families:
            return families[0] # Trả về tên font Nunito
            
    return fallback

def get_main_style():
    family = load_fonts()
    return f"""
        /* 1. Thiết lập mặc định cho toàn bộ ứng dụng: Chữ thường, không đậm */
        QWidget {{ 
            font-family: '{family}', 'Segoe UI', sans-serif; 
            font-size: 14px; 
            font-weight: normal; 
            background-color: #f5f5f5; 
            color: #2c3e50;
        }}
        
        /* 2. Chỉ những thành phần này mới được phép ĐẬM */
        QPushButton {{ 
            background-color: #2E7D32; 
            color: white; 
            border-radius: 8px; 
            padding: 10px; 
            font-size: 14px;
            font-weight: 800; /* Extra Bold cho nút bấm */
        }}
        
        QPushButton:hover {{ 
            background-color: #1B5E20; 
        }}

        /* 3. Đảm bảo các ô nhập liệu và nhãn không bị đậm */
        QLabel, QLineEdit, QTextEdit, QComboBox {{
            font-weight: normal;
        }}

        /* Đặt ID riêng cho các tiêu đề lớn trong code (ví dụ: setObjectName("title")) */
        QLabel#title {{
            font-size: 20px;
            font-weight: 800;
            color: #1B5E20;
        }}
    """