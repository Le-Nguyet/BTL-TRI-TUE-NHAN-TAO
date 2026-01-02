import sqlite3
import re
import os
from src.logic.knowledge_base import MAPPER 

# Đường dẫn file
DB_PATH = os.path.join("data", "monan.db")
RULES_FILE = "raw_rules.txt"

def sync_all_data():
    if not os.path.exists(RULES_FILE):
        print("❌ Không tìm thấy file raw_rules.txt")
        return

    # Cấu trúc: { 'D1': { 'tinh': set(), 'mua': set(), ... }, ... }
    data_map = {}

    # Regex bắt các nhóm: T(tỉnh), L(loại), M(mùa), N(nlc), P(nlp), V(vị) => D(món)
    pattern = r"(T\d+).*?(L\d+).*?(M\d+).*?(N\d+).*?(P\d+).*?(V\d+).*?=>\s*(D\d+)"

    print("🔍 Đang đọc tập luật và giải mã tri thức...")
    
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(pattern, line)
            if match:
                t, l, m, n, p, v, d_id = match.groups()
                
                if d_id not in data_map:
                    data_map[d_id] = {
                        "tinh": set(), "loai": set(), "mua": set(), 
                        "nlc": set(), "nlp": set(), "vi": set()
                    }
                
                # Ánh xạ từ mã (T1, V2...) sang tên tiếng Việt trong MAPPER
                if t in MAPPER: data_map[d_id]["tinh"].add(MAPPER[t])
                if l in MAPPER: data_map[d_id]["loai"].add(MAPPER[l])
                if m in MAPPER: data_map[d_id]["mua"].add(MAPPER[m])
                if n in MAPPER: data_map[d_id]["nlc"].add(MAPPER[n])
                if p in MAPPER: data_map[d_id]["nlp"].add(MAPPER[p])
                if v in MAPPER: data_map[d_id]["vi"].add(MAPPER[v])

    # 2. Ghi vào SQLite
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print(f"🚀 Đang cập nhật Database cho {len(data_map)} món ăn...")
        
        for d_id, fields in data_map.items():
            # Chuyển set thành chuỗi, ví dụ: {"Chua", "Cay"} -> "Chua, Cay"
            tinh = ", ".join(sorted(list(fields['tinh'])))
            loai = ", ".join(sorted(list(fields['loai'])))
            mua = ", ".join(sorted(list(fields['mua'])))
            nlc = ", ".join(sorted(list(fields['nlc'])))
            nlp = ", ".join(sorted(list(fields['nlp'])))
            vi = ", ".join(sorted(list(fields['vi'])))

            # Cập nhật vào bảng products
            cursor.execute("""
                UPDATE products 
                SET tinh = ?, loai = ?, mua = ?, nlc = ?, nlp = ?, vi = ?
                WHERE id = ?
            """, (tinh, loai, mua, nlc, nlp, vi, d_id))

        conn.commit()
        conn.close()
        print("✅ ĐÃ CẬP NHẬT TẤT CẢ THUỘC TÍNH THÀNH CÔNG!")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    sync_all_data()