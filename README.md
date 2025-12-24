🌾 HỆ CHUYÊN GIA TƯ VẤN ẨM THỰC ĐẶC SẢN ĐBSCL
1. Hệ thống ứng dụng trí tuệ nhân tạo (AI) để hỗ trợ du khách lựa chọn món ăn đặc sản phù hợp dựa trên sở thích cá nhân, địa phương và mùa vụ tại vùng Đồng bằng sông Cửu Long
2.📌 GIỚI THIỆU ĐỀ TÀI
- Mục tiêu: Xây dựng hệ chuyên gia bằng ngôn ngữ Python để số hóa tri thức ẩm thực miền Tây
3.Đối tượng: Du khách muốn khám phá văn hóa ẩm thực nhưng gặp khó khăn do thông tin phân tán
4.Công nghệ sử dụng: Python, PySide6 (Giao diện), Lập luận dựa trên luật (Rule-based reasoning)5555.+1📂 

CẤU TRÚC THƯ MỤCPlaintextBTL TRI TUE NHAN TAO/
├── assets/
│   ├── fonts/         # Phông chữ Nunito thiết kế giao diện
│   └── images/        # Kho ảnh đặc sản (D1.png -> D27.png)
├── data/
│   └── mon_an.db      # Cơ sở dữ liệu (tùy chọn mở rộng)
├── src/
│   ├── logic/
│   │   ├── knowledge_base.py    # Cơ sở tri thức (27 món ăn đặc sản)
│   │   └── inference_engine.py  # Bộ suy diễn logic
│   └── ui/
│       ├── main_window.py       # Quản lý chuyển trang (Stack)
│       ├── input_panel.py       # Trang nhập liệu (Sở thích/Mùa/Tỉnh)
│       ├── result_panel.py      # Trang hiển thị kết quả tư vấn
│       └── styles.py            # Quản lý giao diện, màu sắc
├── main.py            # Tệp chạy ứng dụng chính
└── raw_rules.txt      # Tập luật thô của hệ thống

🚀 HƯỚNG DẪN CÀI ĐẶT
- Yêu cầu: Cài đặt Python 3.10 trở lên.
- Cài đặt thư viện:Bashpip install PySide6
- Chạy ứng dụng:Bashpython main.py

👥 THÀNH VIÊN THỰC HIỆN
Lê Thị Thu Nguyệt - Lớp ĐHSTIN23B 
Nguyễn Tuấn Dinh - Lớp ĐHSTIN23B 
GVHD: Thạc sĩ Lê Minh Thư 13