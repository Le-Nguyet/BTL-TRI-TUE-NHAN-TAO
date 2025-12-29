import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import pandas as pd
import sqlite3
import os

# --- CẤU HÌNH ĐƯỜNG DẪN ---
DB_PATH = os.path.join("data", "monan.db")
if not os.path.exists("data"): os.makedirs("data")

class KnowledgeManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ Thống Quản Trị Tri Thức Đặc Sản Miền Tây")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f4f7f6")
        
        self.conn = sqlite3.connect(DB_PATH)
        self.init_db_structure()
        self.init_ui()
        self.load_data()

    def init_db_structure(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY, ten TEXT, loai TEXT, vi TEXT, tinh TEXT, 
                mua TEXT, nlc TEXT, nlp TEXT, mo_ta TEXT, image_path TEXT)
        """)
        self.conn.commit()

    def init_ui(self):
        # --- TIÊU ĐỀ ---
        header = tk.Frame(self.root, bg="#2c3e50", height=50)
        header.pack(side="top", fill="x")
        tk.Label(header, text="BẢNG ĐIỀU KHIỂN QUẢN TRỊ TRI THỨC", fg="white", bg="#2c3e50", font=("Arial", 14, "bold")).pack(pady=10)

        # --- PHẦN BÊN TRÁI: TÌM KIẾM & DANH SÁCH ---
        left_frame = tk.Frame(self.root, width=350, bg="white", bd=1, relief="flat")
        left_frame.pack(side="left", fill="y", padx=15, pady=15)

        tk.Label(left_frame, text="🔍 TÌM KIẾM MÓN ĂN:", font=("Arial", 10, "bold"), bg="white").pack(pady=(10, 0), anchor="w", padx=10)
        
        # Ô nhập tìm kiếm
        self.ent_search = tk.Entry(left_frame, font=("Arial", 11), bd=1, relief="solid")
        self.ent_search.pack(fill="x", padx=10, pady=5)
        self.ent_search.bind("<KeyRelease>", self.on_search_change) # Tự động lọc khi gõ chữ

        # Bảng hiển thị
        self.tree = ttk.Treeview(left_frame, columns=("ID", "Ten"), show="headings", selectmode="browse")
        self.tree.heading("ID", text="Mã ID")
        self.tree.heading("Ten", text="Tên món")
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Ten", width=220)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Nút xóa
        tk.Button(left_frame, text="🗑️ XÓA MÓN ĐANG CHỌN", bg="#e74c3c", fg="white", font=("Arial", 9, "bold"), command=self.delete_item).pack(fill="x", padx=10, pady=10)

        # --- PHẦN BÊN PHẢI: CHI TIẾT & CHỈNH SỬA ---
        right_frame = tk.LabelFrame(self.root, text=" THÔNG TIN CHI TIẾT MÓN ĂN ", bg="white", padx=20, pady=10, font=("Arial", 11, "bold"))
        right_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        self.inputs = {}
        fields = [
            ("id", "Mã ID (vd: D1):"), ("ten", "Tên món ăn:"), ("loai", "Loại món:"),
            ("vi", "Vị (vd: Chua):"), ("tinh", "Tỉnh:"), ("mua", "Mùa:"),
            ("nlc", "NL Chính:"), ("nlp", "NL Phụ:"), ("image_path", "Tên file ảnh:")
        ]

        for i, (key, label) in enumerate(fields):
            tk.Label(right_frame, text=label, bg="white").grid(row=i, column=0, sticky="w", pady=3)
            entry = tk.Entry(right_frame, font=("Arial", 10), bd=1, relief="solid")
            entry.grid(row=i, column=1, sticky="ew", pady=3)
            self.inputs[key] = entry

        tk.Label(right_frame, text="Mô tả món ăn:", bg="white").grid(row=len(fields), column=0, sticky="nw", pady=5)
        self.txt_mo_ta = scrolledtext.ScrolledText(right_frame, font=("Arial", 10), width=40, height=10, wrap=tk.WORD, bd=1, relief="solid")
        self.txt_mo_ta.grid(row=len(fields), column=1, sticky="ew", pady=5)

        # Cụm nút lưu/nạp
        btn_box = tk.Frame(right_frame, bg="white")
        btn_box.grid(row=len(fields)+1, column=0, columnspan=2, pady=15, sticky="ew")

        tk.Button(btn_box, text="💾 CẬP NHẬT THÔNG TIN", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), command=self.update_item, height=2).pack(fill="x", pady=2)
        tk.Button(btn_box, text="📁 NẠP TỪ FILE CSV", bg="#34495e", fg="white", command=self.import_csv).pack(fill="x", pady=2)

        right_frame.columnconfigure(1, weight=1)

    def load_data(self, filter_text=""):
        """Tải dữ liệu có lọc và sắp xếp theo ID số"""
        for item in self.tree.get_children(): self.tree.delete(item)
        cursor = self.conn.cursor()
        
        # SQL sắp xếp số: cắt chữ 'D' và chuyển sang Integer
        base_query = "SELECT id, ten FROM products"
        if filter_text:
            query = f"{base_query} WHERE ten LIKE ? OR id LIKE ? ORDER BY CAST(SUBSTR(id, 2) AS INTEGER) ASC"
            cursor.execute(query, (f'%{filter_text}%', f'%{filter_text}%'))
        else:
            query = f"{base_query} ORDER BY CAST(SUBSTR(id, 2) AS INTEGER) ASC"
            cursor.execute(query)
            
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def on_search_change(self, event):
        """Hàm xử lý khi người dùng gõ vào ô tìm kiếm"""
        self.load_data(self.ent_search.get())

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected: return
        item_id = self.tree.item(selected)['values'][0]
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id=?", (item_id,))
        data = cursor.fetchone()
        if data:
            cols = ["id", "ten", "loai", "vi", "tinh", "mua", "nlc", "nlp", "mo_ta", "image_path"]
            row_dict = dict(zip(cols, data))
            for k, entry in self.inputs.items():
                entry.delete(0, tk.END)
                entry.insert(0, str(row_dict[k]))
            self.txt_mo_ta.delete("1.0", tk.END)
            self.txt_mo_ta.insert(tk.END, row_dict["mo_ta"])

    def update_item(self):
        try:
            d = {k: e.get() for k, e in self.inputs.items()}
            d['mo_ta'] = self.txt_mo_ta.get("1.0", tk.END).strip()
            if not d['id']: return messagebox.showwarning("Lỗi", "Vui lòng nhập ID!")
            
            cursor = self.conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO products VALUES (?,?,?,?,?,?,?,?,?,?)", list(d.values()))
            self.conn.commit()
            messagebox.showinfo("Xong", f"Đã cập nhật món {d['id']}!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def delete_item(self):
        selected = self.tree.selection()
        if not selected: return
        item_id = self.tree.item(selected)['values'][0]
        if messagebox.askyesno("Xác nhận", f"Xóa vĩnh viễn món {item_id}?"):
            self.conn.execute("DELETE FROM products WHERE id=?", (item_id,))
            self.conn.commit()
            self.load_data(); self.ent_search.delete(0, tk.END)

    def import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if path:
            try:
                df = pd.read_csv(path, encoding='utf-8')
                for _, r in df.iterrows():
                    self.conn.execute("INSERT OR REPLACE INTO products VALUES (?,?,?,?,?,?,?,?,?,?)", list(r))
                self.conn.commit(); self.load_data()
                messagebox.showinfo("Thành công", "Đã nạp tri thức từ CSV!")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = KnowledgeManager(root)
    root.mainloop()