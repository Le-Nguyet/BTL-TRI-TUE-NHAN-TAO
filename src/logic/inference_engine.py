import re
import os
from .knowledge_base import MAPPER, get_data_from_db

def infer_dishes(criteria, unused_data):
    # Lấy dữ liệu mới nhất từ Database
    data_mon_an = get_data_from_db()
    found_ids = set()
    
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    rules_path = os.path.join(base_path, "raw_rules.txt")
    
    if not os.path.exists(rules_path):
        return []

    pattern = r"(T\d+)\s*\^\s*(L\d+)\s*\^\s*(M\d+)\s*\^\s*(N\d+)\s*\^\s*(P\d+)\s*\^\s*(V\d+)\s*=>\s*(D\d+)"

    with open(rules_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(pattern, line)
            if match:
                t, l, m, n, p, v, d = match.groups()
                
                # Logic so khớp (Giữ nguyên như bạn đã viết)
                match_tinh = (criteria.get('tinh') == "Tất cả" or MAPPER.get(t) == criteria.get('tinh'))
                match_mua = (criteria.get('mua') == "Tất cả" or MAPPER.get(m) == criteria.get('mua'))
                match_loai = (criteria.get('loai') == "Tất cả" or MAPPER.get(l) == criteria.get('loai'))
                match_nlc = (criteria.get('nlc') == "Tất cả" or MAPPER.get(n) == criteria.get('nlc'))
                match_nlp = (criteria.get('nlp') == "Tất cả" or MAPPER.get(p) == criteria.get('nlp'))
                
                selected_vi = criteria.get('vi', [])
                match_vi = (not selected_vi or MAPPER.get(v) in selected_vi)

                if match_tinh and match_mua and match_loai and match_nlc and match_nlp and match_vi:
                    found_ids.add(d)

    return [mon for mon in data_mon_an if mon['id'] in found_ids]