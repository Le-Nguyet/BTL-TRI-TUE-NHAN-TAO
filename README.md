🌾 HỆ CHUYÊN GIA TƯ VẤN ẨM THỰC ĐẶC SẢN ĐBSCL
1. Hệ thống ứng dụng trí tuệ nhân tạo (AI) để hỗ trợ du khách lựa chọn món ăn đặc sản phù hợp dựa trên sở thích cá nhân, địa phương và mùa vụ tại vùng Đồng bằng sông Cửu Long

📌 GIỚI THIỆU ĐỀ TÀI
1. Mục tiêu: Xây dựng hệ chuyên gia bằng ngôn ngữ Python để số hóa tri thức ẩm thực miền Tây
2. Đối tượng: Du khách muốn khám phá văn hóa ẩm thực nhưng gặp khó khăn do thông tin phân tán
3. Công nghệ sử dụng: Python, PySide6 (Giao diện), Lập luận dựa trên luật (Rule-based reasoning)

📂 CẤU TRÚC THƯ MỤC Plaintext BTL TRI TUE NHAN TAO/
BTL TRI TUE NHAN TAO/
├── assets/
│   ├── fonts/           # Nunito-ExtraBold.ttf
│   └── images/          # D1.png, ..., ban-do-mien-tay.png, Trang chủ.png
├── src/
│   ├── logic/
│   │   ├── __init__.py
│   │   ├── knowledge_base.py    # Chứa DATA_MON_AN (có nlc, nlp) và MAPPER
│   │   └── inference_engine.py  # Bộ suy diễn (đã thêm so khớp nlc, nlp)
│   └── ui/
│       ├── __init__.py
│       ├── main_window.py       # Quản lý Stack chuyển trang
│       ├── input_panel.py       # Nhập liệu & chứa Map
│       ├── map_widget.py        # Widget bản đồ tương tác (Mới)
│       ├── result_panel.py      # Hiển thị kết quả (Dùng nlc, nlp)
│       └── styles.py            # Quản lý màu sắc, font
├── main.py              # File chạy chính
└── raw_rules.txt        # Tập luật (T ^ L ^ M ^ N ^ P ^ V => D)

🚀 HƯỚNG DẪN CÀI ĐẶT
1. Yêu cầu: Cài đặt Python 3.10 trở lên.
2. Cài đặt thư viện:Bashpip install PySide6
3. Chạy ứng dụng:Bashpython main.py

👥 THÀNH VIÊN THỰC HIỆN
1. Lê Thị Thu Nguyệt - Lớp ĐHSTIN23B 
2. Nguyễn Tuấn Dinh - Lớp ĐHSTIN23B 
GVHD: Thạc sĩ Lê Minh Thư 