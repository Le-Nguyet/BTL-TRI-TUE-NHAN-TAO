import re
import os
from .knowledge_base import MAPPER, get_data_from_db

def infer_dishes(criteria, unused_data):
    # 1. Lấy dữ liệu thực tế mới nhất từ Database
    data_mon_an = get_data_from_db()
    found_ids = set()
    
    # Xác định đường dẫn tuyệt đối đến file raw_rules.txt
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    rules_path = os.path.join(base_path, "raw_rules.txt")
    
    if not os.path.exists(rules_path):
        print(f"⚠️ Không tìm thấy file luật tại: {rules_path}")
        return []

    # 2. Regex bắt các mã hiệu chuẩn
    pattern = r"(T\d+)\s*\^\s*(L\d+)\s*\^\s*(M\d+)\s*\^\s*(N\d+)\s*\^\s*(P\d+)\s*\^\s*(V\d+)\s*=>\s*(D\d+)"

    try:
        with open(rules_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "?" in line:
                    continue 
                
                match = re.search(pattern, line)
                if match:
                    t, l, m, n, p, v, d = match.groups()
                    
                    # Lấy giá trị từ người dùng và chuẩn hóa
                    c_tinh = str(criteria.get('tinh', '')).strip()
                    c_mua  = str(criteria.get('mua', '')).strip()
                    c_loai = str(criteria.get('loai', '')).strip()
                    c_nlc  = str(criteria.get('nlc', '')).strip()
                    c_nlp  = str(criteria.get('nlp', '')).strip()

                    # So khớp từng tiêu chí 
                    match_tinh = (c_tinh == "Tất cả" or str(MAPPER.get(t, '')).strip() == c_tinh)
                    match_mua  = (c_mua == "Tất cả" or str(MAPPER.get(m, '')).strip() == c_mua)
                    match_loai = (c_loai == "Tất cả" or str(MAPPER.get(l, '')).strip() == c_loai)
                    match_nlc  = (c_nlc == "Tất cả" or str(MAPPER.get(n, '')).strip() == c_nlc)
                    
                    # Logic cho món Trái cây: Nếu chọn "Tất cả" thì khớp mọi mã P
                    match_nlp  = (c_nlp == "Tất cả" or str(MAPPER.get(p, '')).strip() == c_nlp)
                    
                    # Xử lý Vị
                    selected_vi = criteria.get('vi', [])
                    mapper_vi_val = str(MAPPER.get(v, '')).strip()
                    match_vi = (not selected_vi or mapper_vi_val in selected_vi)

                    # Nếu tất cả tiêu chí khớp, thêm ID món ăn vào danh sách kết quả
                    if match_tinh and match_mua and match_loai and match_nlc and match_nlp and match_vi:
                        found_ids.add(d)

    except Exception as e:
        print(f"❌ Lỗi khi đọc file luật: {e}")

    # 3. Kết hợp với Database để trả về thông tin chi tiết
    results = []
    for mon in data_mon_an:
        if mon['id'] in found_ids:
            # Lấy vị từ DB (có thể là chuỗi "Chua, Ngọt")
            db_vi = str(mon.get('vi', ''))
            user_vi_list = criteria.get('vi', []) 
            
            if not user_vi_list:
                results.append(mon)
            else:
                # Nếu có bất kỳ vị nào người dùng chọn nằm trong món ăn
                if any(vi_val.strip() in db_vi for vi_val in user_vi_list):
                    results.append(mon)
                    
    return results