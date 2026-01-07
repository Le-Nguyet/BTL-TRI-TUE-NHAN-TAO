import re
import os
from .knowledge_base import MAPPER, get_data_from_db

def infer_dishes(criteria, unused_data=None):
    data_mon_an = get_data_from_db()
    found_ids = set()
    
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    rules_path = os.path.join(base_path, "raw_rules.txt")
    
    if not os.path.exists(rules_path): return []

    pattern = r"(T\d+)\s*\^\s*(L\d+)\s*\^\s*(M\d+)\s*\^\s*(N\d+)\s*\^\s*(P\d+)\s*\^\s*(V\d+)\s*=>\s*(D\d+)"

    try:
        with open(rules_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "?" in line: continue 
                
                match = re.search(pattern, line)
                if match:
                    t, l, m, n, p, v, d = match.groups()
                    
                    # Chuẩn hóa đầu vào
                    c_tinh = str(criteria.get('tinh', '')).strip()
                    c_mua  = str(criteria.get('mua', '')).strip()
                    c_loai = str(criteria.get('loai', '')).strip()
                    c_nlc  = str(criteria.get('nlc', '')).strip()
                    c_nlp  = str(criteria.get('nlp', '')).strip()

                    # So khớp Logic
                    match_tinh = (c_tinh == "Tất cả" or str(MAPPER.get(t)).strip() == c_tinh)
                    match_mua  = (c_mua == "Tất cả" or str(MAPPER.get(m)).strip() == c_mua)
                    match_loai = (c_loai == "Tất cả" or str(MAPPER.get(l)).strip() == c_loai)
                    match_nlc  = (c_nlc == "Tất cả" or str(MAPPER.get(n)).strip() == c_nlc)
                    match_nlp  = (c_nlp == "Tất cả" or str(MAPPER.get(p)).strip() == c_nlp)
                    
                    # Xử lý Vị
                    selected_vi = criteria.get('vi', [])
                    mapper_vi = str(MAPPER.get(v)).strip()
                    match_vi = (not selected_vi or mapper_vi in selected_vi)

                    if all([match_tinh, match_mua, match_loai, match_nlc, match_nlp, match_vi]):
                        found_ids.add(d)
    except Exception as e:
        print(f"❌ Lỗi Engine: {e}")

    # Lọc lại với DB để đảm bảo chính xác
    results = []
    for mon in data_mon_an:
        if mon['id'] in found_ids:
            # Nếu người dùng chọn Trái cây, DB cũng phải ghi Trái cây
            if c_nlc != "Tất cả" and c_nlc not in str(mon.get('nlc')): continue
            results.append(mon)
    return results