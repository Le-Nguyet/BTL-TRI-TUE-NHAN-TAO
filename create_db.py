import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import pandas as pd
import sqlite3
import os

DB_PATH = os.path.join("data", "monan.db")

class KnowledgeManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Tri thức Đặc sản Miền Tây")
        self.root.geometry("1000x650")
        self.conn = sqlite3.connect(DB_PATH)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        # --- PHẦN BÊN TRÁI: DANH SÁCH ID ---
        left_frame = tk.Frame(self.root, width=300)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(left_frame, text="DANH SÁCH MÓN ĂN", font=("Arial", 10, "bold")).pack()
        
        # Bảng hiển thị danh sách
        self.tree = ttk.Treeview(left_frame, columns=("ID", "Ten"), show="headings", selectmode="browse")
        self.tree.heading("ID", text="Mã ID")
        self.tree.heading("Ten", text="Tên món")
        self.tree.column("ID", width=50)
        self.tree.column("Ten", width=200)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Nút chức năng bên trái
        btn_box = tk.Frame(left_frame)
        btn_box.pack(fill="x", pady=5)
        tk.Button(btn_box, text="🔄 Làm mới", command=self.load_data).pack(side="left", fill="x", expand=True)
        tk.Button(btn_box, text="🗑️ Xóa món", bg="#e74c3c", fg="white", command=self.delete_item).pack(side="right", fill="x", expand=True)

        # --- PHẦN BÊN PHẢI: CHI TIẾT & CHỈNH SỬA ---
        right_frame = tk.LabelFrame(self.root, text="CHI TIẾT & CHỈNH SỬA", padx=15, pady=15)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Tạo các ô nhập liệu
        self.inputs = {}
        fields = [
            ("id", "Mã ID (Không nên sửa):"), ("ten", "Tên món ăn:"), 
            ("loai", "Loại món:"), ("vi", "Vị (vd: Chua, Ngọt):"), 
            ("tinh", "Tỉnh:"), ("mua", "Mùa:"), 
            ("nlc", "Nguyên liệu chính:"), ("nlp", "Nguyên liệu phụ:"),
            ("image_path", "Tên file ảnh (vd: D1.png):")
        ]

        for i, (key, label) in enumerate(fields):
            tk.Label(right_frame, text=label).grid(row=i, column=0, sticky="w", pady=2)
            entry = tk.Entry(right_frame, width=40)
            entry.grid(row=i, column=1, sticky="ew", pady=2)
            self.inputs[key] = entry

        # Riêng phần mô tả dùng Text Area
        tk.Label(right_frame, text="Mô tả món ăn:").grid(row=len(fields), column=0, sticky="nw")
        self.txt_mo_ta = scrolledtext.ScrolledText(right_frame, width=40, height=8, wrap=tk.WORD)
        self.txt_mo_ta.grid(row=len(fields), column=1, sticky="ew", pady=5)

        # Nút Cập nhật
        tk.Button(right_frame, text="💾 CẬP NHẬT THÔNG TIN", font=("Arial", 10, "bold"),
                  bg="#27ae60", fg="white", pady=10, command=self.update_item).grid(row=len(fields)+1, column=0, columnspan=2, sticky="ew", pady=10)

        # Nút Nạp Excel (Dưới cùng)
        tk.Button(right_frame, text="📁 NẠP MỚI TỪ FILE CSV", command=self.import_csv).grid(row=len(fields)+2, column=0, columnspan=2, sticky="ew")

    def load_data(self):
        """Sắp xếp ID từ nhỏ đến lớn bằng SQL"""
        for item in self.tree.get_children(): self.tree.delete(item)
        try:
            cursor = self.conn.cursor()
            query = "SELECT id, ten FROM products ORDER BY CAST(SUBSTR(id, 2) AS INTEGER) ASC"
            cursor.execute(query)
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)
        except:
            # Nếu có ID lỗi, quay về sắp xếp chuỗi mặc định
            cursor.execute("SELECT id, ten FROM products ORDER BY id ASC")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)

    def on_select(self, event):
        """Khi bấm vào 1 dòng trong bảng, hiển thị chi tiết sang bên phải"""
        selected = self.tree.selection()
        if not selected: return
        item_id = self.tree.item(selected)['values'][0]
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id=?", (item_id,))
        data = cursor.fetchone()
        columns = ["id", "ten", "loai", "vi", "tinh", "mua", "nlc", "nlp", "mo_ta", "image_path"]
        
        if data:
            data_dict = dict(zip(columns, data))
            for key, entry in self.inputs.items():
                entry.delete(0, tk.END)
                entry.insert(0, str(data_dict[key]))
            self.txt_mo_ta.delete("1.0", tk.END)
            self.txt_mo_ta.insert(tk.END, data_dict["mo_ta"])

    def update_item(self):
        """Lấy dữ liệu từ các ô nhập và UPDATE vào Database"""
        try:
            d = {k: e.get() for k, e in self.inputs.items()}
            d['mo_ta'] = self.txt_mo_ta.get("1.0", tk.END).strip()
            
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE products SET 
                ten=?, loai=?, vi=?, tinh=?, mua=?, nlc=?, nlp=?, mo_ta=?, image_path=?
                WHERE id=?
            """, (d['ten'], d['loai'], d['vi'], d['tinh'], d['mua'], d['nlc'], d['nlp'], d['mo_ta'], d['image_path'], d['id']))
            self.conn.commit()
            messagebox.showinfo("Thành công", f"Đã cập nhật món {d['id']}!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def delete_item(self):
        selected = self.tree.selection()
        if not selected: return
        item_id = self.tree.item(selected)['values'][0]
        if messagebox.askyesno("Xác nhận", f"Xóa hoàn toàn món {item_id}?"):
            self.conn.execute("DELETE FROM products WHERE id=?", (item_id,))
            self.conn.commit()
            self.load_data()
            messagebox.showinfo("Xong", "Đã xóa dữ liệu.")

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
                for _, row in df.iterrows():
                    if str(row['id']).startswith('D'):
                        self.conn.execute("INSERT OR REPLACE INTO products VALUES (?,?,?,?,?,?,?,?,?,?)", 
                                        (row['id'], row['ten'], row['loai'], row['vi'], row['tinh'], 
                                         row['mua'], row['nlc'], row['nlp'], row['mo_ta'], row['image_path']))
                self.conn.commit()
                self.load_data()
                messagebox.showinfo("Thành công", "Đã nạp tri thức từ file CSV!")
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = KnowledgeManager(root)
    root.mainloop()