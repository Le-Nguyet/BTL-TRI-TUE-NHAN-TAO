import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import pandas as pd
import sqlite3
import os
import re

# Import MAPPER từ file knowledge_base để giải mã các ký hiệu T, L, M, N, P, V
# Đảm bảo cấu trúc thư mục của bạn cho phép import này
try:
    from src.logic.knowledge_base import MAPPER
except ImportError:
    # Nếu chưa có file knowledge_base, bạn có thể định nghĩa tạm MAPPER ở đây
    MAPPER = {}

# --- CẤU HÌNH ĐƯỜNG DẪN ---
DB_PATH = os.path.join("data", "monan.db")
RULES_FILE = "raw_rules.txt"
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
        self.ent_search.bind("<KeyRelease>", self.on_search_change) 

        # Bảng hiển thị
        self.tree = ttk.Treeview(left_frame, columns=("ID", "Ten"), show="headings", selectmode="browse")
        self.tree.heading("ID", text="Mã ID")
        self.tree.heading("Ten", text="Tên món")
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Ten", width=220)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Cụm nút công cụ bên trái
        tk.Button(left_frame, text="🗑️ XÓA MÓN ĐANG CHỌN", bg="#e74c3c", fg="white", font=("Arial", 9, "bold"), command=self.delete_item).pack(fill="x", padx=10, pady=5)
        
        # --- NÚT ĐỒNG BỘ TRI THỨC ---
        tk.Button(left_frame, text="🔄 ĐỒNG BỘ TỪ LUẬT", bg="#e67e22", fg="white", font=("Arial", 9, "bold"), command=self.sync_from_rules).pack(fill="x", padx=10, pady=5)

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
        for item in self.tree.get_children(): self.tree.delete(item)
        cursor = self.conn.cursor()
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
                entry.insert(0, str(row_dict[k]) if row_dict[k] is not None else "")
            self.txt_mo_ta.delete("1.0", tk.END)
            self.txt_mo_ta.insert(tk.END, str(row_dict["mo_ta"]) if row_dict["mo_ta"] is not None else "")

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

    def sync_from_rules(self):
        if not os.path.exists(RULES_FILE):
            return messagebox.showerror("Lỗi", "Không tìm thấy file raw_rules.txt")

        try:
            from src.logic.knowledge_base import MAPPER
            data_map = {}
            # Regex linh hoạt hơn để tránh lỗi dấu cách
            pattern = r"(T\d+).*?(L\d+).*?(M\d+).*?(N\d+).*?(P\d+).*?(V\d+).*?=>\s*(D\d+)"
            
            with open(RULES_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    match = re.search(pattern, line)
                    if match:
                        t, l, m, n, p, v, d_id = match.groups()
                        if d_id not in data_map:
                            data_map[d_id] = {k: set() for k in ['tinh','loai','mua','nlc','nlp','vi']}
                        
                        for code, key in zip([t,l,m,n,p,v], ['tinh','loai','mua','nlc','nlp','vi']):
                            if code in MAPPER: 
                                data_map[d_id][key].add(MAPPER[code])

            cursor = self.conn.cursor()
            update_count = 0
            for d_id, fields in data_map.items():
                vals = {k: ", ".join(sorted(list(v))) for k, v in fields.items()}
                
                # SỬ DỤNG LỆNH CẬP NHẬT THÔNG MINH:
                # Nếu món chưa có (ID mới), nó sẽ tạo dòng mới với tên "Món mới (Chờ cập nhật)"
                cursor.execute("SELECT ten FROM products WHERE id=?", (d_id,))
                exists = cursor.fetchone()
                
                if exists:
                    cursor.execute("""
                        UPDATE products SET tinh=?, loai=?, mua=?, nlc=?, nlp=?, vi=? WHERE id=?
                    """, (vals['tinh'], vals['loai'], vals['mua'], vals['nlc'], vals['nlp'], vals['vi'], d_id))
                else:
                    # Tự động thêm món mới nếu trong luật có mà DB chưa có
                    cursor.execute("""
                        INSERT INTO products (id, ten, tinh, loai, mua, nlc, nlp, vi, mo_ta) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (d_id, f"Món mới {d_id}", vals['tinh'], vals['loai'], vals['mua'], vals['nlc'], vals['nlp'], vals['vi'], "Chưa có mô tả"))
                
                update_count += 1
            
            self.conn.commit()
            self.load_data()
            messagebox.showinfo("Thành công", f"Đã đồng bộ toàn bộ {update_count} món ăn từ tập luật!")
            
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Lỗi: {str(e)}")

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