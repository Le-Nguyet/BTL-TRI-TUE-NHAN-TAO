import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd # Đảm bảo đã chạy: pip install pandas
import sqlite3
import os

# --- CẤU HÌNH ĐƯỜNG DẪN ---
DB_PATH = os.path.join("data", "monan.db")
if not os.path.exists("data"): os.makedirs("data")

def get_connection():
    return sqlite3.connect(DB_PATH)

# --- 1. KHỞI TẠO CẤU TRÚC (CHỈ CHẠY LẦN ĐẦU) ---
def init_database():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Tạo bảng nếu chưa có, không dùng DROP để tránh mất dữ liệu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                ten TEXT, loai TEXT, vi TEXT, tinh TEXT, mua TEXT,
                nlc TEXT, nlp TEXT, mo_ta TEXT, image_path TEXT
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Lỗi khởi tạo: {e}")

# --- 2. CHỨC NĂNG NẠP DỮ LIỆU TỪ EXCEL/CSV ---
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        lbl_file_path.config(text=os.path.basename(file_path))
        btn_import.config(state="normal", command=lambda: import_csv(file_path))

def import_csv(file_path):
    try:
        # Đọc dữ liệu
        df = pd.read_csv(file_path, encoding='utf-8')
        
        # Làm sạch dữ liệu: Chỉ lấy ID bắt đầu bằng 'D'
        df['id'] = df['id'].astype(str)
        df_clean = df[df['id'].str.startswith('D', na=False)]
        
        conn = get_connection()
        cursor = conn.cursor()
        success_count = 0

        for _, row in df_clean.iterrows():
            # Sử dụng INSERT OR REPLACE để cập nhật thông tin nếu trùng ID
            cursor.execute("""
                INSERT OR REPLACE INTO products (id, ten, loai, vi, tinh, mua, nlc, nlp, mo_ta, image_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (row['id'], row['ten'], row['loai'], row['vi'], row['tinh'], 
                  row['mua'], row['nlc'], row['nlp'], row['mo_ta'], row['image_path']))
            success_count += 1

        conn.commit()
        conn.close()
        
        # THÔNG BÁO QUAN TRỌNG
        messagebox.showinfo("Thành công", 
            f"✅ Đã nạp/cập nhật {success_count} món ăn vào Database.\n\n"
            "⚠️ LƯU Ý: File này KHÔNG ghi đè luật. \n"
            "Hãy đảm bảo 25 luật của bạn đã được dán vào file 'raw_rules.txt' để bộ suy luận hoạt động.")
            
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xử lý file: {e}")

# --- 3. XÓA MÓN LẺ (GIỮ NGUYÊN TẬP LUẬT) ---
def delete_item():
    id_del = simpledialog.askstring("Xóa món", "Nhập ID món cần xóa (vd: D1):")
    if id_del:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (id_del,))
            if cursor.rowcount > 0:
                conn.commit()
                messagebox.showinfo("Xong", f"Đã xóa dữ liệu món {id_del}.")
            else:
                messagebox.showwarning("Lỗi", "Không tìm thấy ID này.")
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

# --- GIAO DIỆN ---
if __name__ == "__main__":
    init_database()
    root = tk.Tk()
    root.title("Quản lý Cơ sở Tri thức")
    root.geometry("400x350")

    tk.Label(root, text="QUẢN TRỊ DỮ LIỆU HỆ CHUYÊN GIA", font=("Arial", 12, "bold")).pack(pady=20)

    # Khung nạp file
    frame = tk.LabelFrame(root, text="Nạp dữ liệu món ăn (Ảnh/Mô tả)", padx=10, pady=10)
    frame.pack(fill="x", padx=20)
    
    tk.Button(frame, text="📁 Chọn file CSV", command=browse_file).pack()
    lbl_file_path = tk.Label(frame, text="Chưa chọn file", fg="grey")
    lbl_file_path.pack()
    
    btn_import = tk.Button(frame, text="🚀 NẠP VÀO HỆ THỐNG", state="disabled", bg="#27ae60", fg="white")
    btn_import.pack(pady=10)

    # Khung xóa
    tk.Button(root, text="🗑️ Xóa món ăn theo ID", command=delete_item, bg="#e74c3c", fg="white").pack(pady=20)

    root.mainloop()