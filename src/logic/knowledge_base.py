import sqlite3
import os

# Đường dẫn đến file db
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(base_dir, "data", "monan.db")

def get_data_from_db():
    """Hàm tự động lấy toàn bộ tri thức từ Database"""
    if not os.path.exists(DB_PATH):
        return []
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    
    data = []
    for row in rows:
        item = dict(row)
        # Chuyển chuỗi Vị "Chua, Ngọt" thành List ["Chua", "Ngọt"]
        if isinstance(item['vi'], str):
            item['vi'] = [v.strip() for v in item['vi'].split(',')]
        data.append(item)
    
    conn.close()
    return data

# Tri thức tĩnh
MAPPER = {
    'T1': 'Long An', 'T3': 'Đồng Tháp', 'T4': 'An Giang', 'T9': 'Kiên Giang', 'T10': 'Cần Thơ', 'T13': 'Sóc Trăng',
    'L1': 'Món nước', 'L2': 'Món khô', 'L4': 'Món gỏi', 'L7': 'Món hấp', 'L8': 'Món lẩu', 'L9': 'Món cháo', 'L10': 'Món bánh',
    'M1': 'Mùa nước nổi', 'M2': 'Mùa mưa', 'M3': 'Mùa khô', 'M4': 'Mùa Tết', 'M5': 'Mùa trái cây',
    'N1': 'Hải sản', 'N2': 'Cá', 'N3': 'Bún', 'N5': 'Bánh tằm', 'N6': 'Bột', 'N9': 'Thịt',
    'P2': 'Mắm', 'P3': 'Bông điên điển', 'P5': 'Rau đắng', 'P7': 'Rau củ quả', 'P8': 'Chao',
    'V1': 'Cay', 'V2': 'Ngọt', 'V3': 'Chua', 'V4': 'Mặn', 'V5': 'Béo', 'V8': 'Đắng'
}