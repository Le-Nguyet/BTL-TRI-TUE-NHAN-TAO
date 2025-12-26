import re
import os
from .knowledge_base import MAPPER, DATA_MON_AN

def infer_dishes(criteria, data_mon_an):
    found_ids = set()
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    rules_path = os.path.join(base_path, "raw_rules.txt")
    
    if not os.path.exists(rules_path):
        print(f"LỖI: Không thấy file {rules_path}")
        return []

    # Pattern khớp với: T ^ L ^ M ^ N ^ P ^ V => D
    pattern = r"(T\d+)\s*\^\s*(L\d+)\s*\^\s*(M\d+)\s*\^\s*(N\d+)\s*\^\s*(P\d+)\s*\^\s*(V\d+)\s*=>\s*(D\d+)"

    with open(rules_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(pattern, line)
            if match:
                t, l, m, n, p, v, d = match.groups()
                
                # 1. So khớp Tỉnh, Mùa, Loại
                match_tinh = (criteria.get('tinh') == "Tất cả" or MAPPER.get(t) == criteria.get('tinh'))
                match_mua = (criteria.get('mua') == "Tất cả" or MAPPER.get(m) == criteria.get('mua'))
                match_loai = (criteria.get('loai') == "Tất cả" or MAPPER.get(l) == criteria.get('loai'))
                
                # 2. So khớp Nguyên liệu chính (nlc - mã N)
                match_nlc = (criteria.get('nlc') == "Tất cả" or MAPPER.get(n) == criteria.get('nlc'))
                
                # 3. So khớp Nguyên liệu phụ (nlp - mã P)
                match_nlp = (criteria.get('nlp') == "Tất cả" or MAPPER.get(p) == criteria.get('nlp'))
                
                # 4. So khớp Vị (criteria['vi'] thường là một danh sách)
                match_vi = False
                selected_vi = criteria.get('vi', [])
                if not selected_vi or MAPPER.get(v) in selected_vi:
                    match_vi = True

                # CHỈ KHI TẤT CẢ ĐỀU KHỚP
                if match_tinh and match_mua and match_loai and match_nlc and match_nlp and match_vi:
                    found_ids.add(d)

    # TRẢ VỀ FULL DATA (Giúp hiện ảnh và mô tả)
    return [mon for mon in data_mon_an if mon['id'] in found_ids]