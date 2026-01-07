import sqlite3
import os

# Đường dẫn đến file db
base_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(base_dir)), "data", "monan.db")

def get_data_from_db():
    """Lấy dữ liệu và sắp xếp theo số ID (D1, D2, D3...)"""
    if not os.path.exists(DB_PATH): return []
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        # Sắp xếp theo số sau chữ D
        cursor.execute("SELECT * FROM products ORDER BY CAST(SUBSTR(id, 2) AS INTEGER) ASC")
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        for item in data:
            if isinstance(item.get('vi'), str):
                item['vi'] = [v.strip() for v in item['vi'].split(',')]
        conn.close()
        return data
    except: return []

# Tri thức tĩnh
MAPPER = {
    'T1': 'Long An', 'T2': 'Tiền Giang','T3': 'Đồng Tháp', 'T4': 'An Giang', 'T5': 'Vĩnh Long', 'T6': 'Trà Vinh', 'T7': 'Bến Tre', 'T8': 'Cà Mau', 'T9': 'Kiên Giang', 'T10': 'Cần Thơ', 'T11': 'Hậu Giang', 'T12': 'Bạc Liêu',  'T13': 'Sóc Trăng',
    'L1': 'Món nước', 'L2': 'Món khô', 'L4': 'Món gỏi', 'L7': 'Món hấp', 'L8': 'Món lẩu', 'L9': 'Món cháo', 'L10': 'Món bánh',
    'M1': 'Mùa nước nổi', 'M2': 'Mùa mưa', 'M3': 'Mùa khô', 'M4': 'Mùa tết', 'M5': 'Mùa trái cây', 'M6':'Quanh năm',
    'N1': 'Hải sản', 'N2': 'Cá', 'N3': 'Bún', 'N5': 'Bánh tằm', 'N6': 'Bột', 'N7': 'Nếp','N8': 'Gạo','N9': 'Thịt', 'N10': 'Trứng', 'N11': 'Trái cây',
    'P1': 'Sen', 'P2': 'Mắm', 'P3': 'Bông điên điển', 'P4': 'Lá chúc', 'P5': 'Rau đắng', 'P6': 'Nước cốt dừa', 'P7': 'Rau củ quả', 'P8': 'Chao', 'P9': 'Dầu mè', 'P10': 'Lá giang', 'P11': 'Tất cả',
    'V1': 'Cay', 'V2': 'Ngọt', 'V3': 'Chua', 'V4': 'Mặn', 'V5': 'Béo', 'V6': 'Đắng'
}