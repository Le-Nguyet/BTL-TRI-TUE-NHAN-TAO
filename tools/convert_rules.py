import re
import os
import sqlite3
from src.logic.knowledge_base import MAPPER

# Đường dẫn file
DB_PATH = os.path.join("data", "monan.db")
RULES_FILE = "raw_rules.txt"

# 1. TẠO BẢN ĐỒ NGƯỢC 
INVERSE_MAPPER = {v: k for k, v in MAPPER.items()}

def check_sync_with_db():
    """
    Hàm này dùng để KIỂM TRA xem 25 luật trong raw_rules.txt 
    có khớp với dữ liệu thực tế trong monan.db hay không.
    """
    if not os.path.exists(RULES_FILE):
        print("❌ Không tìm thấy file raw_rules.txt")
        return

    print("🔍 Đang kiểm tra tính nhất quán của hệ chuyên gia...")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products")
        db_ids = {row[0] for row in cursor.fetchall()}
        conn.close()

        with open(RULES_FILE, "r", encoding="utf-8") as f:
            rules_content = f.readlines()

        missing_in_db = []
        for line in rules_content:
            match = re.search(r"=>\s*(D\d+)", line)
            if match:
                rule_id = match.group(1)
                if rule_id not in db_ids:
                    missing_in_db.append(rule_id)

        if missing_in_db:
            print(f"⚠️ CẢNH BÁO: Các món {set(missing_in_db)} có trong LUẬT nhưng thiếu trong DATABASE!")
            print("👉 Bạn cần nạp thêm các món này vào file Excel để hiển thị được ảnh/mô tả.")
        else:
            print("✅ Tuyệt vời! Tất cả các luật đều có dữ liệu tương ứng trong Database.")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

def convert_rules_to_vietnamese():
    """Giải mã 25 luật của bạn sang tiếng Việt để đọc hiểu"""
    rules_converted = []
    pattern = r"(T\d+)\s*\^\s*(L\d+)\s*\^\s*(M\d+)\s*\^\s*(N\d+)\s*\^\s*(P\d+)\s*\^\s*(V\d+)\s*=>\s*(D\d+)"
    
    if not os.path.exists(RULES_FILE):
        return []

    try:
        with open(RULES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                match = re.search(pattern, line)
                if match:
                    t, l, m, n, p, v, d = match.groups()
                    rule = {
                        "tinh": MAPPER.get(t, f"Lỗi({t})"),
                        "loai": MAPPER.get(l, f"Lỗi({l})"),
                        "mua": MAPPER.get(m, f"Lỗi({m})"),
                        "nlc": MAPPER.get(n, f"Lỗi({n})"),
                        "nlp": MAPPER.get(p, f"Lỗi({p})"),
                        "vi": MAPPER.get(v, f"Lỗi({v})"),
                        "id_mon": d
                    }
                    rules_converted.append(rule)
        
        print(f"✅ Đã giải mã {len(rules_converted)} luật hiện có.")
        return rules_converted
    except Exception as e:
        print(f"❌ Lỗi giải mã: {e}")
        return []

