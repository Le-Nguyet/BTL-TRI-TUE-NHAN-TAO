import re
import os

# Bộ từ điển ánh xạ (Dán trực tiếp vào đây hoặc import từ knowledge_base)
MAPPER = {
    'T1': 'Long An', 'T3': 'Đồng Tháp', 'T4': 'An Giang', 'T9': 'Kiên Giang', 'T10': 'Cần Thơ', 'T13': 'Sóc Trăng',
    'L1': 'Món nước', 'L2': 'Món khô', 'L4': 'Món gỏi', 'L7': 'Món hấp', 'L8': 'Món lẩu', 'L9': 'Món cháo', 'L10': 'Món bánh',
    'M1': 'Mùa nước nổi', 'M2': 'Mùa mưa', 'M3': 'Mùa khô', 'M4': 'Mùa Tết', 'M5': 'Mùa trái cây',
    'N1': 'Hải sản', 'N2': 'Cá', 'N3': 'Bún', 'N5': 'Bánh tằm', 'N6': 'Bột', 'N9': 'Thịt',
    'P2': 'Mắm', 'P3': 'Bông điên điển', 'P5': 'Rau đắng', 'P7': 'Rau củ quả', 'P8': 'Chao',
    'V1': 'Cay', 'V2': 'Ngọt', 'V3': 'Chua', 'V4': 'Mặn', 'V5': 'Béo', 'V8': 'Đắng'
}

def infer_dishes(criteria, data_mon_an):
    found_ids = set()
    # Lấy đường dẫn tuyệt đối đến file raw_rules.txt
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    rules_path = os.path.normpath(os.path.join(base_path, "raw_rules.txt"))
    
    if not os.path.exists(rules_path):
        print(f"LỖI: Không tìm thấy file tại {rules_path}")
        return []

    pattern = r"(T\d+)\s*\^\s*(L\d+)\s*\^\s*(M\d+)\s*\^\s*(N\d+)\s*\^\s*(P\d+)\s*\^\s*(V\d+)\s*=>\s*(D\d+)"

    with open(rules_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(pattern, line)
            if match:
                t, l, m, n, p, v, d = match.groups()
                
                # So khớp logic (Chuyển mã T1, L1... sang chữ tiếng Việt qua MAPPER)
                match_tinh = (criteria['tinh'] == "Tất cả" or MAPPER.get(t) == criteria['tinh'])
                match_mua = (criteria['mua'] == "Tất cả" or MAPPER.get(m) == criteria['mua'])
                match_loai = (criteria['loai'] == "Tất cả" or MAPPER.get(l) == criteria['loai'])
                
                match_vi = False
                if not criteria['vi'] or MAPPER.get(v) in criteria['vi']:
                    match_vi = True

                if match_tinh and match_mua and match_loai and match_vi:
                    found_ids.add(d)

    # TRẢ VỀ ĐỐI TƯỢNG ĐẦY ĐỦ (Cần thiết để hiện ảnh và mô tả)
    return [mon for mon in data_mon_an if mon['id'] in found_ids]
