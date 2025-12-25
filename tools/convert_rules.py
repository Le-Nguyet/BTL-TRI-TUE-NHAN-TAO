import re

# Bộ từ điển chuyển đổi (Dựa trên file DOCX của bạn)
MAPPER = {
    'T1': 'Long An', 'T3': 'Đồng Tháp', 'T4': 'An Giang', 'T9': 'Kiên Giang', 'T10': 'Cần Thơ', 'T13': 'Sóc Trăng',
    'L1': 'Món nước', 'L2': 'Món khô', 'L4': 'Món gỏi', 'L7': 'Món hấp', 'L8': 'Món lẩu', 'L9': 'Món cháo', 'L10': 'Món bánh',
    'M1': 'Mùa nước nổi', 'M2': 'Mùa mưa', 'M3': 'Mùa khô', 'M4': 'Mùa Tết', 'M5': 'Mùa trái cây',
    'N1': 'Hải sản', 'N2': 'Cá', 'N3': 'Bún', 'N5': 'Bánh tằm', 'N6': 'Bột', 'N9': 'Thịt',
    'P2': 'Mắm', 'P3': 'Bông điên điển', 'P5': 'Rau đắng', 'P7': 'Rau củ quả', 'P8': 'Chao',
    'V1': 'Cay', 'V2': 'Ngọt', 'V3': 'Chua', 'V4': 'Mặn', 'V5': 'Béo', 'V8': 'Đắng'
}

def convert_rules():
    input_file = "raw_rules.txt"
    rules_converted = []
    
    # Regex bắt 6 yếu tố: T, L, M, N, P, V và kết quả D
    pattern = r"(T\d+)\s*\^\s*(L\d+)\s*\^\s*(M\d+)\s*\^\s*(N\d+)\s*\^\s*(P\d+)\s*\^\s*(V\d+)\s*=>\s*(D\d+)"
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                match = re.search(pattern, line)
                if match:
                    t, l, m, n, p, v, d = match.groups()
                    rule = {
                        "tinh": MAPPER.get(t),
                        "loai": MAPPER.get(l),
                        "mua": MAPPER.get(m),
                        "nlc": MAPPER.get(n),
                        "nlp": MAPPER.get(p),
                        "vi": MAPPER.get(v),
                        "id_mon": d
                    }
                    rules_converted.append(rule)
        
        print(f"✅ Đã chuyển đổi thành công {len(rules_converted)} luật sang tiếng Việt.")
        return rules_converted
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return []

if __name__ == "__main__":
    data = convert_rules()
    for r in data[:3]: print(r) # Xem thử 3 luật đầu