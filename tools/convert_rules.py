import re

def convert_rules():
    input_file = "raw_rules.txt"
    # Regex để bắt các luật từ file text
    pattern = r"(L\d+)\s*\^\s*(C\d+).*=>\s*(S\d+)"
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read()
        matches = re.findall(pattern, content)
        print(f"Đã tìm thấy {len(matches)} luật.")
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    convert_rules()