import re
import os
from .knowledge_base import MAPPER, DATA_MON_AN

def infer_dishes(criteria, data_mon_an):
    found_ids = set()
    # Lấy đường dẫn chuẩn đến file raw_rules.txt
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    rules_path = os.path.join(base_path, "raw_rules.txt")
    
    if not os.path.exists(rules_path):
        print(f"Không tìm thấy file luật tại: {rules_path}")
        return []

    pattern = r"(T\d+)\s*\^\s*(L\d+)\s*\^\s*(M\d+)\s*\^\s*(N\d+)\s*\^\s*(P\d+)\s*\^\s*(V\d+)\s*=>\s*(D\d+)"

    with open(rules_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(pattern, line)
            if match:
                t, l, m, n, p, v, d = match.groups()
                
                # So khớp logic qua MAPPER
                match_tinh = (criteria['tinh'] == "Tất cả" or MAPPER.get(t) == criteria['tinh'])
                match_mua = (criteria['mua'] == "Tất cả" or MAPPER.get(m) == criteria['mua'])
                match_loai = (criteria['loai'] == "Tất cả" or MAPPER.get(l) == criteria['loai'])
                
                match_vi = False
                if not criteria['vi'] or MAPPER.get(v) in criteria['vi']:
                    match_vi = True

                if match_tinh and match_mua and match_loai and match_vi:
                    found_ids.add(d)

    # TRẢ VỀ DANH SÁCH MÓN ĂN ĐẦY ĐỦ (Chứa cả mo_ta và hinh_anh)
    return [mon for mon in data_mon_an if mon['id'] in found_ids]