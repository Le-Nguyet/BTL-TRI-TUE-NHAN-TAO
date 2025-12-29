🌾 HỆ CHUYÊN GIA TƯ VẤN ẨM THỰC ĐẶC SẢN ĐBSCL
Hệ thống ứng dụng trí tuệ nhân tạo (AI) để hỗ trợ du khách lựa chọn món ăn đặc sản phù hợp dựa trên sở thích cá nhân, địa phương và mùa vụ tại vùng Đồng bằng sông Cửu Long.

📌 GIỚI THIỆU ĐỀ TÀI
1. Mục tiêu: Xây dựng hệ chuyên gia bằng ngôn ngữ Python để số hóa tri thức ẩm thực miền Tây với quy mô lớn lên đến 72 món ăn đặc sản.
2. Điểm nổi bật: Tích hợp Bản đồ số tương tác thời gian thực, cho phép người dùng chọn vùng địa lý trực quan để khởi chạy bộ máy suy luận ngay lập tức.
3. Công nghệ sử dụng: Python, PySide6 (Giao diện đồ họa), SQLite (Lưu trữ tri thức), Rule-based reasoning (Suy luận dựa trên luật).

📂 CẤU TRÚC THƯ MỤC

BTL TRI TUE NHAN TAO/
├── assets/
│   ├── fonts/           # Nunito-ExtraBold.ttf (Phông chữ hệ thống)
│   └── images/          # D1.png...D72.png (72 hình ảnh đặc sản), ban-do-mien-tay.png
├── data/
│   ├── monan.db         # Cơ sở dữ liệu SQLite chứa 72 món ăn
│   └── danh_sach_mon_an.csv # File nguồn tri thức để nạp dữ liệu
├── src/
│   ├── logic/
│   │   ├── knowledge_base.py    # Kết nối DB và ánh xạ MAPPER
│   │   └── inference_engine.py  # Bộ suy diễn logic (xử lý luật & dữ liệu đa trị)
│   └── ui/
│       ├── main_window.py       # Quản lý chuyển trang (Stacked Widget)
│       ├── input_panel.py       # Nhận tiêu chí người dùng
│       ├── map_widget.py        # Widget bản đồ tương tác thời gian thực
│       ├── result_panel.py      # Hiển thị kết quả tư vấn & hình ảnh
│       └── styles.py            # Quản lý giao diện (QSS)
├── tools/
│   └── create_db.py     # Công cụ quản trị: Nạp CSV, Sửa/Xóa món ăn, Tìm kiếm
├── main.py              # File chạy chương trình chính
└── raw_rules.txt        # Tập luật tri thức (72+ luật dạng: T ^ L ^ M ^ N ^ P ^ V => D)

🚀 HƯỚNG DẪN CÀI ĐẶT & VẬN HÀNH
1. Yêu cầu: Cài đặt Python 3.10 trở lên.
2. Cài đặt thư viện: ```bash pip install PySide6 pandas pillow
3. Khởi tạo dữ liệu (Nếu cần): Chạy create_db.py để nạp 72 món ăn từ file CSV vào Database.
4. Chạy ứng dụng: Bash python main.py

💡 TÍNH NĂNG CHÍNH
- Bản đồ tương tác (GIS): Click chọn tỉnh thành trực tiếp trên bản đồ để tự động xác định địa phương tư vấn.
- Suy luận đa điều kiện: Kết hợp 6 tiêu chí (Tỉnh, Loại, Mùa, NL Chính, NL Phụ, Vị) để lọc trong kho tri thức 72 món.
- Xử lý dữ liệu đa trị: Hệ thống thông minh tự động nhận diện các món ăn có nhiều vị (ví dụ: vừa Chua vừa Ngọt).
- Quản trị linh hoạt: Dễ dàng mở rộng thêm món ăn mới chỉ thông qua file CSV mà không cần sửa code logic.

👥 THÀNH VIÊN THỰC HIỆN
1. Lê Thị Thu Nguyệt - Lớp ĐHSTIN23B
2. Nguyễn Tuấn Dinh - Lớp ĐHSTIN23B
GVHD: Thạc sĩ Lê Minh Thư