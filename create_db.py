import sqlite3
import os

# Đường dẫn file database
DB_PATH = os.path.join("data", "monan.db")

# Đảm bảo thư mục data tồn tại
if not os.path.exists("data"):
    os.makedirs("data")

def create_database():
    # 1. Kết nối và xóa bảng cũ nếu tồn tại để cập nhật cấu trúc mới
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS products")

    # 2. Tạo bảng products với nlc và nlp 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        ten TEXT,
        loai TEXT,
        vi TEXT,
        tinh TEXT,
        mua TEXT,
        nlc TEXT,
        nlp TEXT,
        mo_ta TEXT,
        image_path TEXT
    )
    """)

    # 3. Dữ liệu chuẩn khớp với MAPPER và raw_rules 
    DATA_RAW = [
        {
            "id": "D1",
            "ten": "Canh chua cá linh bông điên điển",
            "loai": "Món nước",
            "vi": ["Chua", "Ngọt"],
            "tinh": "An Giang",
            "mua": "Mùa nước nổi",
            "nlc": "Cá",
            "nlp": "Bông điên điển",
            "mo_ta": "Món ăn đặc trưng của mùa nước nổi với vị chua thanh và hoa điên điển vàng rực.",
            "hinh_anh": "D1.png"
        },
        {
            "id": "D2",
            "ten": "Nem chua Lai Vung",
            "loai": "Món khô",
            "vi": ["Chua", "Cay", "Mặn"],
            "tinh": "Đồng Tháp",
            "mua": "Mùa Tết",
            "nlc": "Thịt",
            "nlp": "Chao",
            "mo_ta": "Đặc sản nổi tiếng với vị chua thanh, giòn sần sật của bì heo và nồng nàn vị tỏi ớt.",
            "hinh_anh": "D2.png"
        },
        {
            "id": "D3",
            "ten": "Lẩu cá kèo lá giang",
            "loai": "Món lẩu",
            "vi": ["Chua", "Ngọt"],
            "tinh": "Sóc Trăng",
            "mua": ["Mùa mưa", "Mùa nước nổi", "Mùa Tết"],
            "nlc": "Cá",
            "nlp": "Rau đắng",
            "mo_ta": "Sự kết hợp hoàn hảo giữa cá kèo tươi sống và vị chua đặc trưng của lá giang.",
            "hinh_anh": "D3.png"
        },
        {
            "id": "D4",
            "ten": "Gỏi xoài cá sặc",
            "loai": "Món gỏi",
            "vi": ["Chua", "Ngọt", "Mặn"],
            "tinh": "Long An",
            "mua": "Mùa trái cây",
            "nlc": "Cá",
            "nlp": "Rau củ quả",
            "mo_ta": "Vị chua của xoài xanh hòa quyện cùng vị mặn đặc trưng của khô cá sặc nướng.",
            "hinh_anh": "D4.png"
        },
        {
            "id": "D5",
            "ten": "Cháo cá lóc rau đắng",
            "loai": "Món cháo",
            "vi": ["Đắng", "Ngọt", "Mặn"],
            "tinh": "Long An",
            "mua": "Mùa mưa",
            "nlc": "Cá",
            "nlp": "Rau đắng",
            "mo_ta": "Món ăn ấm bụng ngày mưa với cá lóc đồng và rau đắng đất giải nhiệt.",
            "hinh_anh": "D5.png"
        },
        {
            "id": "D6",
            "ten": "Bánh Pía",
            "loai": "Tráng miệng",
            "vi": ["Ngọt", "Béo"],
            "tinh": "Sóc Trăng",
            "mua": "Mùa Tết",
            "nlc": "Bột",
            "nlp": "Rau củ quả",
            "mo_ta": "Vỏ bánh nhiều lớp mỏng bao bọc nhân sầu riêng và trứng muối béo ngậy.",
            "hinh_anh": "D6.png"
        },
        {
            "id": "D7",
            "ten": "Bún kèn Hà Tiên",
            "loai": "Món nước",
            "vi": ["Béo", "Mặn", "Cay"],
            "tinh": "Kiên Giang",
            "mua": "Mùa khô",
            "nlc": "Cá",
            "nlp": "Rau củ quả",
            "mo_ta": "Nước dùng sền sệt từ cá xay nhuyễn và cốt dừa thơm béo.",
            "hinh_anh": "D7.png"
        },
        {
            "id": "D8",
            "ten": "Bánh tằm bì",
            "loai": "Món bánh",
            "vi": ["Béo", "Mặn", "Ngọt"],
            "tinh": "Cần Thơ",
            "mua": "Quanh năm",
            "nlc": "Bánh tằm",
            "nlp": "Rau củ quả",
            "mo_ta": "Sợi bánh tằm trắng ngần ăn kèm bì heo và nước cốt dừa đậm đà.",
            "hinh_anh": "D8.png"
        },
        {
            "id": "D9",
            "ten": "Bún nước lèo Sóc Trăng",
            "loai": "Món nước",
            "vi": ["Mặn", "Ngọt"],
            "tinh": "Sóc Trăng",
            "mua": ["Mùa mưa", "Mùa khô"],
            "nlc": "Cá",
            "nlp": "Mắm",
            "mo_ta": "Hương vị nồng nàn từ mắm bò hóc kết hợp với ngải bún và cá lóc đồng.",
            "hinh_anh": "D9.png"
        },
        {
            "id": "D10",
            "ten": "Mực trứng nhồi nhum biển",
            "loai": "Món khô",
            "vi": ["Ngọt", "Béo", "Mặn"],
            "tinh": "Kiên Giang",
            "mua": "Mùa khô",
            "nlc": "Hải sản",
            "nlp": "Rau củ quả",
            "mo_ta": "Đặc sản biển Phú Quốc với sự hòa quyện giữa mực tươi và nhum biển giàu dinh dưỡng.",
            "hinh_anh": "D10.png"
        }
    ]

    # Chuẩn bị dữ liệu để đưa vào SQL
    processed_data = []
    for m in DATA_RAW:
        # Chuyển đổi list thành chuỗi để lưu vào SQLite
        vi_str = ", ".join(m["vi"]) if isinstance(m["vi"], list) else m["vi"]
        mua_str = ", ".join(m["mua"]) if isinstance(m["mua"], list) else m["mua"]
        
        processed_data.append((
            m["id"], m["ten"], m["loai"], vi_str, m["tinh"], 
            mua_str, m["nlc"], m["nlp"], m["mo_ta"], m["hinh_anh"]
        ))

    # 4. Thực hiện Insert dữ liệu 
    cursor.executemany("""
    INSERT OR REPLACE INTO products (id, ten, loai, vi, tinh, mua, nlc, nlp, mo_ta, image_path)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, processed_data)

    conn.commit()
    conn.close()
    print(">>> Đã khởi tạo Database thành công tại: data/monan.db")
    print(f">>> Đã cập nhật {len(DATA_RAW)} món với các trường nlc và nlp.")

if __name__ == "__main__":
    create_database()