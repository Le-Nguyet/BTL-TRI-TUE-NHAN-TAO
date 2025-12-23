# tools/convert_rules.py
import re

def convert_rules():
    input_file = "raw_rules.txt"  # File chứa text copy từ Word
    
    # Regex để bắt dòng có dạng: L1 ^ C2 ^ ... => S15
    # Giải thích: Tìm chữ cái (L,C,D,G,H,X) theo sau là số, cách nhau bởi dấu ^
    pattern = r"(L\d+)\s*\^\s*(C\d+)\s*\^\s*(D\d+)\s*\^\s*(G\d+)\s*\^\s*(H\d+)\s*\^\s*(X\d+)\s*=>\s*(S\d+)"
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        matches = re.findall(pattern, content)
        
        print(f"✅ Đã tìm thấy {len(matches)} luật hợp lệ.\n")
        print("# DÁN ĐOẠN NÀY VÀO knowledge_base.py")
        print("RULE_MAP = {")
        
        for m in matches:
            # m là tuple: ('L2', 'C3', 'D1', 'G3', 'H1', 'X3', 'S15')
            # Format lại thành code Python
            key_part = f'    ("{m[0]}", "{m[1]}", "{m[2]}", "{m[3]}", "{m[4]}", "{m[5]}")'
            value_part = f'"{m[6]}"'
            print(f'{key_part}: {value_part},')
            
        print("}")
        
    except FileNotFoundError:
        print("❌ Lỗi: Không tìm thấy file 'raw_rules.txt'. Hãy tạo file này và paste nội dung luật vào.")

if __name__ == "__main__":
    convert_rules()