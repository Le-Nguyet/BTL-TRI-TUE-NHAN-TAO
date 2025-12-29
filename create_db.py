import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd
import sqlite3
import os

# --- CẤU HÌNH ĐƯỜNG DẪN ---
DB_PATH = os.path.join("data", "monan.db")

# --- 1. CHỨC NĂNG DỌN DẸP DATABASE (CLEAN UP) ---
def clean_database():
    """Xóa các dòng rác không đúng định dạng ID (bắt đầu bằng D) trong database"""
    try:
        if not os.path.exists(DB_PATH):
            return
            
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Lệnh SQL: Xóa những dòng mà ID không bắt đầu bằng chữ 'D'
        cursor.execute("DELETE FROM products WHERE id NOT LIKE 'D%'")
        
        so_luong_xoa = cursor.rowcount
        conn.commit()
        conn.close()
        if so_luong_xoa > 0:
            print(f"✅ Đã dọn dẹp hệ thống! Đã xóa {so_luong_xoa} dòng dữ liệu rác hiện có.")
    except Exception as e:
        print(f"❌ Lỗi khi dọn dẹp database: {e}")

# --- 2. CHỨC NĂNG XÓA MỘT MÓN CỤ THỂ THEO ID ---
def delete_specific_item():
    """Cho phép người dùng nhập ID để xóa thủ công một món lỗi"""
    id_to_delete = simpledialog.askstring("Xóa món ăn", "Nhập mã ID cần xóa (ví dụ: D11):")
    
    if id_to_delete:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Kiểm tra xem ID có tồn tại không
            cursor.execute("SELECT ten FROM products WHERE id = ?", (id_to_delete,))
            result = cursor.fetchone()
            
            if result:
                confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa món '{result[0]}' (ID: {id_to_delete})?")
                if confirm:
                    cursor.execute("DELETE FROM products WHERE id = ?", (id_to_delete,))
                    conn.commit()
                    messagebox.showinfo("Thành công", f"Đã xóa món {id_to_delete} khỏi hệ thống.")
            else:
                messagebox.showwarning("Thông báo", f"Không tìm thấy món nào có ID: {id_to_delete}")
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa: {e}")

# --- 3. CHỨC NĂNG NẠP FILE CSV HÀNG LOẠT ---
def browse_file():
    """Mở cửa sổ chọn file từ máy tính"""
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        lbl_file_path.config(text=os.path.basename(file_path))
        btn_import.config(state="normal", command=lambda: import_csv(file_path))

def import_csv(file_path):
    """Đọc và nạp dữ liệu từ file CSV vào Database"""
    try:
        # Đọc file CSV bằng pandas với encoding utf-8
        df = pd.read_csv(file_path, encoding='utf-8')
        
        # TỰ ĐỘNG LỌC DỮ LIỆU LỖI TRONG FILE TRƯỚC KHI NẠP
        df['id'] = df['id'].astype(str)
        df_clean = df[df['id'].str.startswith('D', na=False)]
        
        trash_count = len(df) - len(df_clean)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        success_count = 0
        duplicate_count = 0

        for _, row in df_clean.iterrows():
            # Kiểm tra trùng ID trước khi nạp
            cursor.execute("SELECT id FROM products WHERE id = ?", (row['id'],))
            if cursor.fetchone():
                duplicate_count += 1
                continue
            
            # Nạp dữ liệu vào database (Khớp với các trường bạn đã tạo)
            cursor.execute("""
                INSERT INTO products (id, ten, loai, vi, tinh, mua, nlc, nlp, mo_ta, image_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (row['id'], row['ten'], row['loai'], row['vi'], row['tinh'], 
                  row['mua'], row['nlc'], row['nlp'], row['mo_ta'], row['image_path']))
            success_count += 1

        conn.commit()
        conn.close()
        
        # Thông báo kết quả
        msg = f"✅ Nạp thành công: {success_count} món\n"
        msg += f"⚠️ Bỏ qua (trùng ID): {duplicate_count} dòng\n"
        if trash_count > 0:
            msg += f"🧹 Đã lọc bỏ {trash_count} dòng rác từ file CSV."
            
        messagebox.showinfo("Kết quả nạp dữ liệu", msg)
        
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xử lý dữ liệu: {e}")

# --- 4. GIAO DIỆN CHÍNH (GUI) ---
if __name__ == "__main__":
    # Tự động dọn dẹp các dòng rác trong database ngay khi mở ứng dụng
    clean_database()

    root = tk.Tk()
    root.title("Quản lý tri thức Hệ chuyên gia")
    root.geometry("450x400")
    root.configure(bg="#f0f0f0")

    # Tiêu đề
    tk.Label(root, text="HỆ THỐNG QUẢN TRỊ TRI THỨC", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=20)

    # --- Khu vực nạp file ---
    frame_import = tk.LabelFrame(root, text="Nạp dữ liệu hàng loạt", padx=10, pady=10)
    frame_import.pack(fill="x", padx=20, pady=5)

    btn_browse = tk.Button(frame_import, text="📁 Chọn file CSV", command=browse_file, width=15)
    btn_browse.pack(pady=5)

    lbl_file_path = tk.Label(frame_import, text="Chưa chọn file", fg="grey", font=("Arial", 9, "italic"))
    lbl_file_path.pack()

    btn_import = tk.Button(frame_import, text="🚀 BẮT ĐẦU NẠP", state="disabled", 
                           bg="#27ae60", fg="white", font=("Arial", 10, "bold"))
    btn_import.pack(pady=10)

    # --- Khu vực quản lý món lẻ ---
    frame_manage = tk.LabelFrame(root, text="Quản lý món lẻ", padx=10, pady=10)
    frame_manage.pack(fill="x", padx=20, pady=15)

    tk.Label(frame_manage, text="Xóa món sai lỗi bằng cách nhập mã ID:").pack()
    btn_delete = tk.Button(frame_manage, text="🗑️ Xóa món theo ID", command=delete_specific_item, 
                           bg="#e74c3c", fg="white", width=20)
    btn_delete.pack(pady=10)

    root.mainloop()