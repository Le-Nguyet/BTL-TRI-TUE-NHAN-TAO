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

    # 2. Regex chỉ bắt các mã hiệu chuẩn (T1, L2...), KHÔNG bắt dấu hỏi '?'
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
                    
                    # Kiểm tra so khớp từng tiêu chí giữa Luật và Lựa chọn của người dùng
                    match_tinh = (criteria.get('tinh') == "Tất cả" or MAPPER.get(t) == criteria.get('tinh'))
                    match_mua  = (criteria.get('mua') == "Tất cả" or MAPPER.get(m) == criteria.get('mua'))
                    match_loai = (criteria.get('loai') == "Tất cả" or MAPPER.get(l) == criteria.get('loai'))
                    match_nlc  = (criteria.get('nlc') == "Tất cả" or MAPPER.get(n) == criteria.get('nlc'))
                    match_nlp  = (criteria.get('nlp') == "Tất cả" or MAPPER.get(p) == criteria.get('nlp'))
                    
                    # Xử lý Vị: Kiểm tra xem vị trong Luật có nằm trong danh sách vị người dùng chọn không
                    selected_vi = criteria.get('vi', [])
                    match_vi = (not selected_vi or MAPPER.get(v) in selected_vi)

                    # Nếu tất cả tiêu chí của dòng luật đều khớp
                    if match_tinh and match_mua and match_loai and match_nlc and match_nlp and match_vi:
                        found_ids.add(d)

    except Exception as e:
        print(f"❌ Lỗi khi đọc file luật: {e}")

    # 3. Kết hợp với Database để trả về thông tin chi tiết món ăn
    results = []
    for mon in data_mon_an:
        if mon['id'] in found_ids:
            db_vi = mon.get('vi', '') 
            user_vi_list = criteria.get('vi', []) 
            
            if not user_vi_list:
                results.append(mon)
            else:
                if any(vi_val in db_vi for vi_val in user_vi_list):
                    results.append(mon)           
    return results