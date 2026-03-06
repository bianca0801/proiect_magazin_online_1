import customtkinter as ctk
import tkinter.messagebox as mb
from tkinter import ttk
import mysql.connector
from PIL import Image
import os
from config import DB_CONFIG


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


COLOR_BG = "#121212"
COLOR_CARD = "#1E1E1E"
COLOR_ACCENT = "#621bc4"
COLOR_ACCENT_HOVER = "#7C4DFF"
COLOR_TEXT = "#FFFFFF"
COLOR_TEXT_DIM = "#B0BEC5"
COLOR_INPUT_BG = "#2C2C2C"
COLOR_DELETE = "#C62828"



def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        mb.showerror("Eroare Baza de Date", f"Nu m-am putut conecta: {err}")
        return None



def apply_treeview_style():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
                    background=COLOR_CARD,
                    foreground="white",
                    fieldbackground=COLOR_CARD,
                    borderwidth=1,
                    relief="solid",
                    rowheight=40,
                    font=("Segoe UI", 12))

    style.configure("Treeview.Heading",
                    background="#252525",
                    foreground="#BB86FC",
                    relief="solid",
                    borderwidth=1,
                    font=("Segoe UI", 13, "bold"))

    style.map("Treeview.Heading", background=[('active', '#333333')])

    style.map("Treeview",
              background=[('selected', COLOR_ACCENT)],
              foreground=[('selected', 'white')])


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Manager Magazin")
        self.geometry("1100x750")
        self.configure(fg_color=COLOR_BG)

        apply_treeview_style()

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame_classes = (FirstFrame, SelectionFrame, AddClientFrame,
                         AddProductFrame, AddOrderFrame, LoginFrame, AdminDashboardFrame)

        for F in frame_classes:
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FirstFrame)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
        if hasattr(frame, 'refresh_data'):
            frame.refresh_data()

class ModernCard(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=COLOR_CARD, corner_radius=20, border_width=0, **kwargs)

class FirstFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        if os.path.exists("background.jpg"):
            try:
                img = ctk.CTkImage(Image.open("background.jpg"), size=(1100, 750))
                ctk.CTkLabel(self, image=img, text="").place(x=0, y=0, relwidth=1, relheight=1)
            except:
                pass

        self.place_content()

    def place_content(self):
        card = ModernCard(self)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="BINE AI VENIT", font=("Segoe UI", 36, "bold"), text_color="white").pack(padx=60,
                                                                                                         pady=(40, 10))
        ctk.CTkLabel(card, text="Sistem de Gestiune Integrat", font=("Segoe UI", 16), text_color=COLOR_TEXT_DIM).pack(
            pady=(0, 40))

        ctk.CTkButton(card, text="ADAUGA DATE",
                      font=("Segoe UI", 15, "bold"), width=220, height=55,
                      fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, corner_radius=25,
                      command=lambda: self.controller.show_frame(SelectionFrame)).pack(pady=10)

        ctk.CTkButton(card, text="PANOU ADMIN",
                      font=("Segoe UI", 15, "bold"), width=220, height=55,
                      fg_color="#37474F", hover_color="#455A64", corner_radius=25,
                      command=lambda: self.controller.show_frame(LoginFrame)).pack(pady=(10, 40))


class SelectionFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        card = ModernCard(self)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="MENIU ADAUGARE", font=("Segoe UI", 28, "bold"), text_color="white").pack(padx=50,
                                                                                                          pady=40)

        grid_frame = ctk.CTkFrame(card, fg_color="transparent")
        grid_frame.pack(padx=40, pady=10)

        self.create_btn(grid_frame, "CLIENT", AddClientFrame, 0)
        self.create_btn(grid_frame, "PRODUS", AddProductFrame, 1)
        self.create_btn(grid_frame, "COMANDA", AddOrderFrame, 2)

        ctk.CTkButton(card, text="← Inapoi", fg_color="transparent", text_color="gray", hover=False,
                      command=lambda: controller.show_frame(FirstFrame)).pack(pady=20)

    def create_btn(self, parent, text, frame_target, col):
        ctk.CTkButton(parent, text=text, font=("Segoe UI", 16, "bold"),
                      width=160, height=120, corner_radius=15,
                      fg_color="#2D2D2D", hover_color="#3D3D3D", border_width=1, border_color="#333",
                      command=lambda: self.controller.show_frame(frame_target)).grid(row=0, column=col, padx=10)


class AddClientFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        card = ModernCard(self)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="CLIENT NOU", font=("Segoe UI", 20, "bold")).pack(pady=(30, 20))

        self.ent_nume = self.create_input(card, "Nume")
        self.ent_prenume = self.create_input(card, "Prenume")
        self.ent_email = self.create_input(card, "Email")

        ctk.CTkButton(card, text="SALVEAZA", fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER,
                      width=200, height=50, corner_radius=25, font=("Segoe UI", 13, "bold"),
                      command=self.save).pack(pady=25)

        ctk.CTkButton(card, text="Inapoi", fg_color="transparent", text_color="gray", hover=False,
                      command=lambda: controller.show_frame(SelectionFrame)).pack(pady=(0, 20))

    def create_input(self, parent, ph):
        entry = ctk.CTkEntry(parent, placeholder_text=ph, width=290, height=38,
                             fg_color=COLOR_INPUT_BG, border_width=0, corner_radius=10)
        entry.pack(pady=8, padx=20)
        return entry

    def save(self):
        nume = self.ent_nume.get()
        prenume = self.ent_prenume.get()
        email = self.ent_email.get()
        if not nume or not prenume: mb.showwarning("Eroare", "Date incomplete!"); return
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("INSERT INTO clienti (Nume, Prenume, Email) VALUES (%s, %s, %s)", (nume, prenume, email))
                conn.commit()
                conn.close()
                mb.showinfo("Succes", "Client Salvat!")
                self.clear_inputs()
            except Exception as e:
                mb.showerror("Err", str(e))

    def clear_inputs(self):
        self.ent_nume.delete(0, 'end')
        self.ent_prenume.delete(0, 'end')
        self.ent_email.delete(0, 'end')


class AddProductFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        card = ModernCard(self)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="PRODUS NOU", font=("Segoe UI", 24, "bold")).pack(pady=(30, 20))

        self.ent_nume = self.create_input(card, "Nume Produs")

        row_frame = ctk.CTkFrame(card, fg_color="transparent")
        row_frame.pack(pady=10)
        self.ent_pret = self.create_small_input(row_frame, "Pret (RON)")
        self.ent_pret.pack(side="left", padx=5)
        self.ent_stoc = self.create_small_input(row_frame, "Stoc")
        self.ent_stoc.pack(side="left", padx=5)

        self.ent_desc = self.create_input(card, "Descriere scurta")

        ctk.CTkButton(card, text="SALVEAZA", fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER,
                      width=250, height=50, corner_radius=25, font=("Segoe UI", 14, "bold"),
                      command=self.save).pack(pady=30)

        ctk.CTkButton(card, text="Inapoi", fg_color="transparent", text_color="gray", hover=False,
                      command=lambda: controller.show_frame(SelectionFrame)).pack(pady=(0, 20))

    def create_input(self, parent, ph):
        entry = ctk.CTkEntry(parent, placeholder_text=ph, width=300, height=45, fg_color=COLOR_INPUT_BG, border_width=0,
                             corner_radius=10)
        entry.pack(pady=10)
        return entry

    def create_small_input(self, parent, ph):
        return ctk.CTkEntry(parent, placeholder_text=ph, width=145, height=45, fg_color=COLOR_INPUT_BG, border_width=0,
                            corner_radius=10)

    def save(self):
        try:
            conn = get_db_connection()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO produse (Nume, Pret, Descriere, Stoc) VALUES (%s, %s, %s, %s)",
                            (self.ent_nume.get(), int(self.ent_pret.get()), self.ent_desc.get(),
                             int(self.ent_stoc.get())))
                conn.commit()
                conn.close()
                mb.showinfo("Succes", "Produs Salvat!")
                self.ent_nume.delete(0, 'end')
                self.ent_pret.delete(0, 'end')
                self.ent_desc.delete(0, 'end')
                self.ent_stoc.delete(0, 'end')
        except Exception as e:
            mb.showerror("Err", str(e))


class AddOrderFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.map_clienti = {}
        self.map_produse = {}
        self.stocuri_produse = {}
        self.cos_cumparaturi = []

        card = ModernCard(self)
        card.pack(fill="both", expand=True, padx=40, pady=40)

        ctk.CTkLabel(card, text="PLASARE COMANDA", font=("Segoe UI", 24, "bold"), text_color="white").pack(
            pady=(30, 20))

        sel_frame = ctk.CTkFrame(card, fg_color="transparent")
        sel_frame.pack(fill="x", padx=40)

        self.combo_client = ctk.CTkComboBox(sel_frame, width=250, height=40, fg_color=COLOR_INPUT_BG, border_width=0)
        self.combo_client.pack(side="left", padx=5)

        self.combo_produs = ctk.CTkComboBox(sel_frame, width=250, height=40, fg_color=COLOR_INPUT_BG, border_width=0)
        self.combo_produs.pack(side="left", padx=5)

        self.ent_cant = ctk.CTkEntry(sel_frame, width=80, height=40, placeholder_text="1", fg_color=COLOR_INPUT_BG,border_width=0)
        self.ent_cant.pack(side="left", padx=5)

        ctk.CTkButton(sel_frame, text="+", width=50, height=40, fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER,
                      corner_radius=10, command=self.add_to_cart).pack(side="left", padx=10)

        table_frame = ctk.CTkFrame(card, fg_color=COLOR_INPUT_BG, corner_radius=15)
        table_frame.pack(fill="both", expand=True, padx=40, pady=20)

        cols = ("Produs", "Cantitate", "Stoc Ramas")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=8)
        self.tree.heading("Produs", text="Produs")
        self.tree.column("Produs", width=250)
        self.tree.heading("Cantitate", text="Cantitate")
        self.tree.column("Cantitate", width=80, anchor="center")
        self.tree.heading("Stoc Ramas", text="Stoc")
        self.tree.column("Stoc Ramas", width=80, anchor="center")

        self.tree.tag_configure('odd', background='#252525')
        self.tree.tag_configure('even', background='#1E1E1E')

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=40, pady=20)

        ctk.CTkButton(btn_frame, text="Sterge Selectia", fg_color="transparent", text_color="#EF5350", hover=False,
                      command=self.remove_from_cart).pack(side="left")

        ctk.CTkButton(btn_frame, text="FINALIZEAZA", fg_color="#00C853", hover_color="#00E676", width=200, height=45,
                      corner_radius=22, font=("Segoe UI", 13, "bold"), command=self.finalize_order).pack(side="right")
        ctk.CTkButton(btn_frame, text="Inapoi", fg_color="transparent", text_color="gray", hover=False, width=80,
                      command=self.go_back).pack(side="right", padx=10)

    def go_back(self):
        self.cos_cumparaturi = []
        self.refresh_cart_visuals()
        self.controller.show_frame(SelectionFrame)

    def refresh_data(self):
        self.cos_cumparaturi = []
        self.refresh_cart_visuals()
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT idClient, CONCAT(Nume, ' ', Prenume) FROM clienti")
            self.map_clienti = {name: uid for uid, name in cursor.fetchall()}
            self.combo_client.configure(values=list(self.map_clienti.keys()))
            self.combo_client.set("Selecteaza Client")

            cursor.execute("SELECT idProdus, Nume, Stoc FROM produse WHERE Stoc > 0")
            produse_data = cursor.fetchall()
            self.map_produse = {}
            self.stocuri_produse = {}
            nume_produse = []
            for pid, nume, stoc in produse_data:
                n = f"{nume}"
                self.map_produse[n] = pid
                self.stocuri_produse[pid] = stoc
                nume_produse.append(n)
            self.combo_produs.configure(values=nume_produse)
            self.combo_produs.set("Selecteaza Produs")
            conn.close()

    def add_to_cart(self):
        pk = self.combo_produs.get()
        pid = self.map_produse.get(pk)
        cs = self.ent_cant.get()
        if not pid or not cs.isdigit() or int(cs) <= 0: mb.showerror("Err", "Produs/Cantitate invalida!"); return
        req = int(cs)
        st = self.stocuri_produse.get(pid)
        in_c = sum(i['cantitate'] for i in self.cos_cumparaturi if i['pid'] == pid)
        if req + in_c > st: mb.showerror("Stoc", f"Indisponibil! Stoc: {st}"); return
        self.cos_cumparaturi.append({'pid': pid, 'nume': pk, 'cantitate': req, 'stoc_ramas_dupa': st - (req + in_c)})
        self.refresh_cart_visuals()
        self.ent_cant.delete(0, 'end')
        self.ent_cant.insert(0, "1")

    def remove_from_cart(self):
        sel = self.tree.selection()
        if sel: del self.cos_cumparaturi[self.tree.index(sel)]; self.refresh_cart_visuals()

    def refresh_cart_visuals(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for idx, i in enumerate(self.cos_cumparaturi):
            tag = 'even' if idx % 2 == 0 else 'odd'
            self.tree.insert("", "end", values=(i['nume'], i['cantitate'], i['stoc_ramas_dupa']), tags=(tag,))

    def finalize_order(self):
        uid = self.map_clienti.get(self.combo_client.get())
        if not uid or not self.cos_cumparaturi: mb.showerror("Err", "Date lipsa!"); return
        if mb.askyesno("Confirmare", "Finalizezi?"):
            conn = get_db_connection()
            if conn:
                try:
                    c = conn.cursor()
                    for i in self.cos_cumparaturi:
                        c.execute(
                            "INSERT INTO comenzi (idClient, idProdus, Cantitate, dataAchizitie) VALUES (%s, %s, %s, CURDATE())",
                            (uid, i['pid'], i['cantitate']))
                        c.execute("UPDATE produse SET Stoc = Stoc - %s WHERE idProdus = %s", (i['cantitate'], i['pid']))
                    conn.commit()
                    mb.showinfo("Ok", "Finalizat!")
                    self.cos_cumparaturi = []
                    self.refresh_cart_visuals()
                    self.refresh_data()
                except Exception as e:
                    conn.rollback(); mb.showerror("Err", str(e))
                finally:
                    conn.close()


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        card = ModernCard(self)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="LOGIN", font=("Segoe UI", 24, "bold")).pack(pady=30)

        self.user = ctk.CTkEntry(card, placeholder_text="User", width=250, height=45, fg_color=COLOR_INPUT_BG,
                                 border_width=0, corner_radius=10)
        self.user.pack(pady=8, padx=20)
        self.pas = ctk.CTkEntry(card, placeholder_text="Parola", show="*", width=250, height=45,
                                fg_color=COLOR_INPUT_BG, border_width=0, corner_radius=10)
        self.pas.pack(pady=8, padx=20)

        ctk.CTkButton(card, text="INTRĂ", fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, width=250, height=50,
                      corner_radius=25, command=self.check).pack(pady=30)
        ctk.CTkButton(card, text="Inapoi", fg_color="transparent", text_color="gray", hover=False,
                      command=lambda: controller.show_frame(FirstFrame)).pack(pady=(0, 20))

    def check(self):
        if self.user.get() == "admin" and self.pas.get() == "admin":
            self.controller.show_frame(AdminDashboardFrame)
        else:
            mb.showerror("Err", "Gresit!")


class AdminDashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        head = ctk.CTkFrame(self, fg_color="transparent")
        head.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(head, text="ADMIN DASHBOARD", font=("Segoe UI", 22, "bold"), text_color="white").pack(side="left")
        ctk.CTkButton(head, text="Log Out", fg_color="#D32F2F", width=100, corner_radius=15,
                      command=lambda: controller.show_frame(FirstFrame)).pack(side="right")

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=30, pady=10)
        self.tabview._segmented_button.configure(selected_color=COLOR_ACCENT, selected_hover_color=COLOR_ACCENT_HOVER,
                                                 corner_radius=15)

        self.tab_c = self.tabview.add("Clienti")
        self.tab_p = self.tabview.add("Produse")
        self.tab_o = self.tabview.add("Comenzi")

        self.setup_admin_tabs()

    def refresh_data(self):
        self.refresh_c()
        self.refresh_p()
        self.refresh_o()

    def setup_admin_tabs(self):

        self.tree_c = self.create_table(self.tab_c, ("id", "Nume", "Prenume", "Email"))
        self.tree_c.bind("<<TreeviewSelect>>", self.sel_c)
        f_c = ctk.CTkFrame(self.tab_c, fg_color="transparent")
        f_c.pack(fill="x", pady=10)
        self.in_c = [ctk.CTkEntry(f_c, placeholder_text=t, width=120) for t in ["ID", "Nume", "Pren", "Email"]]
        for e in self.in_c: e.pack(side="left", padx=5)
        ctk.CTkButton(f_c, text="Update", fg_color="#F57C00", width=80, command=self.up_c).pack(side="right", padx=5)
        ctk.CTkButton(f_c, text="Del", fg_color=COLOR_DELETE, width=60, command=self.del_c).pack(side="right")

        self.tree_p = self.create_table(self.tab_p, ("id", "Nume", "Pret", "Descriere", "Stoc"))
        self.tree_p.bind("<<TreeviewSelect>>", self.sel_p)
        f_p = ctk.CTkFrame(self.tab_p, fg_color="transparent")
        f_p.pack(fill="x", pady=10)
        self.in_p = [ctk.CTkEntry(f_p, placeholder_text=t, width=100) for t in ["ID", "Nume", "Pret", "Descriere", "Stoc"]]
        for e in self.in_p: e.pack(side="left", padx=5)
        ctk.CTkButton(f_p, text="Update", fg_color="#F57C00", width=80, command=self.up_p).pack(side="right", padx=5)
        ctk.CTkButton(f_p, text="Del", fg_color=COLOR_DELETE, width=60, command=self.del_p).pack(side="right")

        self.tree_o = self.create_table(self.tab_o, ("Client", "Produs", "Data", "Cantitate", "Total"))
        ctk.CTkButton(self.tab_o, text="STERGE COMANDA", fg_color=COLOR_DELETE, command=self.del_o).pack(pady=10)

    def create_table(self, parent, cols):
        f = ctk.CTkFrame(parent, fg_color=COLOR_INPUT_BG, corner_radius=10)
        f.pack(fill="both", expand=True, padx=5, pady=5)
        t = ttk.Treeview(f, columns=cols, show="headings", height=10)
        for c in cols: t.heading(c, text=c); t.column(c, width=100)

        t.tag_configure('odd', background='#252525')
        t.tag_configure('even', background='#1E1E1E')

        t.pack(fill="both", expand=True, padx=2, pady=2)
        return t

    def fill_tree(self, tree, query):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(query)
        for idx, r in enumerate(c.fetchall()):
            tag = 'even' if idx % 2 == 0 else 'odd'
            tree.insert("", "end", values=r, tags=(tag,))
        conn.close()

    def refresh_c(self):
        for i in self.tree_c.get_children(): self.tree_c.delete(i)
        self.fill_tree(self.tree_c, "SELECT * FROM clienti")

    def refresh_p(self):
        for i in self.tree_p.get_children(): self.tree_p.delete(i)
        self.fill_tree(self.tree_p, "SELECT * FROM produse")

    def refresh_o(self):
        for i in self.tree_o.get_children(): self.tree_o.delete(i)
        q = "SELECT CONCAT(c.Nume, ' ', c.Prenume), p.Nume, co.dataAchizitie, co.Cantitate, (co.Cantitate * p.Pret), c.idClient, p.idProdus FROM comenzi co JOIN clienti c ON co.idClient = c.idClient JOIN produse p ON co.idProdus = p.idProdus ORDER BY co.dataAchizitie DESC"
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(q)
        for idx, r in enumerate(c.fetchall()):
            tag = 'even' if idx % 2 == 0 else 'odd'
            self.tree_o.insert("", "end", values=r, tags=(tag,))
        conn.close()

    def sel_c(self, e):
        self.fill_inputs(self.tree_c, self.in_c)

    def sel_p(self, e):
        self.fill_inputs(self.tree_p, self.in_p)

    def fill_inputs(self, tree, inputs):
        s = tree.selection()
        if s:
            v = tree.item(s)['values']
            for i, val in enumerate(v): inputs[i].delete(0, 'end'); inputs[i].insert(0, val)

    def up_c(self):
        self.run_q("UPDATE clienti SET Nume=%s, Prenume=%s, Email=%s WHERE idClient=%s",
                   (self.in_c[1].get(), self.in_c[2].get(), self.in_c[3].get(), self.in_c[0].get()), self.refresh_c)

    def del_c(self):
        self.run_q("DELETE FROM clienti WHERE idClient=%s", (self.in_c[0].get(),), self.refresh_c)

    def up_p(self):
        self.run_q("UPDATE produse SET Nume=%s, Pret=%s, Descriere=%s, Stoc=%s WHERE idProdus=%s",
                   (self.in_p[1].get(), self.in_p[2].get(), self.in_p[3].get(), self.in_p[4].get(), self.in_p[0].get()),
                   self.refresh_p)

    def del_p(self):
        self.run_q("DELETE FROM produse WHERE idProdus=%s", (self.in_p[0].get(),), self.refresh_p)

    def del_o(self):
        s = self.tree_o.selection()
        if s:
            v = self.tree_o.item(s)['values']
            self.run_q("DELETE FROM comenzi WHERE idClient=%s AND idProdus=%s AND dataAchizitie=%s LIMIT 1",
                       (v[5], v[6], v[2]), self.refresh_o)

    def run_q(self, q, p, cb):
        if mb.askyesno("?", "Sigur?"):
            conn = get_db_connection()
            c = conn.cursor()
            c.execute(q, p)
            conn.commit()
            conn.close()
            cb()
            mb.showinfo("Ok", "Done!")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()