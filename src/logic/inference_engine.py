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
    """
    criteria: dict chứa {tinh, mua, loai, vi:[]} từ giao diện
    data_mon_an: danh sách các món ăn trong knowledge_base.py
    """
    found_ids = set()
    
    # Tìm đường dẫn file raw_rules.txt (nằm ở thư mục gốc)
    # Nếu file nằm cùng cấp với main.py, ta dùng đường dẫn tương đối
    rules_path = "raw_rules.txt"
    
    if not os.path.exists(rules_path):
        print(f"Lỗi: Không tìm thấy file {rules_path}")
        return []

    # Regex bắt 6 yếu tố và ID kết quả (D1, D2...)
    pattern = r"(T\d+)\s*\^\s*(L\d+)\s*\^\s*(M\d+)\s*\^\s*(N\d+)\s*\^\s*(P\d+)\s*\^\s*(V\d+)\s*=>\s*(D\d+)"

    with open(rules_path, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(pattern, line)
            if match:
                t, l, m, n, p, v, d = match.groups()

                # TIẾN HÀNH SO KHỚP (Dùng MAPPER để dịch mã sang chữ)
                # 1. Kiểm tra Tỉnh
                match_tinh = (criteria['tinh'] == "Tất cả" or MAPPER.get(t) == criteria['tinh'])
                
                # 2. Kiểm tra Mùa
                match_mua = (criteria['mua'] == "Tất cả" or MAPPER.get(m) == criteria['mua'])
                
                # 3. Kiểm tra Loại món
                match_loai = (criteria['loai'] == "Tất cả" or MAPPER.get(l) == criteria['loai'])

                # 4. Kiểm tra Vị (Nếu người dùng chọn ít nhất 1 vị trùng với vị trong luật)
                # MAPPER.get(v) trả về 'Chua', criteria['vi'] là danh sách ['Chua', 'Cay']
                match_vi = False
                if not criteria['vi']: # Nếu không chọn vị nào thì mặc định khớp
                    match_vi = True
                else:
                    if MAPPER.get(v) in criteria['vi']:
                        match_vi = True

                # Nếu tất cả các vế IF đều đúng
                if match_tinh and match_mua and match_loai and match_vi:
                    found_ids.add(d)

    # Lấy thông tin chi tiết món ăn từ DATA_MON_AN dựa trên list ID vừa tìm được
    results = [mon for mon in data_mon_an if mon['id'] in found_ids]
    return results