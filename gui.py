from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import sqlite3
import re



# Buat Database

try:
    conn = sqlite3.connect('kontak.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE kontak (tipe text, nama text, telp text, identitas text, email text,
                perusahaan text, handphone text, fax text, npwp text, alamat_kirim text, alamat_bayar text)""")

    conn.commit()
    conn.close()
except:
    pass


try:
    conn = sqlite3.connect('produk.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE produk (nama text, SKU text, kategori text, unit text, deskripsi text,
                stok int, batas_minimum int, harga_jual text, harga_beli text, harga_beli_terakhir text)""")

    conn.commit()
    conn.close()
except:
    pass



# Query Database

def query_kontak():
    conn = sqlite3.connect('kontak.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM kontak")
    contacts = c.fetchall()

    for contact in contacts:
        tree_kontak.insert("", END, text=contact[1] + ' ' + contact[2], values=(contact[6], contact[10], contact[5], contact[3], contact[5]))
        tree_kontak.bind('<Double-Button-1>', tab_kontak_tersebut)
        tree_kontak.pack()
        
    conn.commit()
    conn.close()

def query_produk():
    conn = sqlite3.connect('produk.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM produk")
    products = c.fetchall()

    for product in products:
        tree_produk.insert("", END, text=product[0], values=(product[1], product[5], product[6], product[3], product[7], product[8], product[9], product[2]))
        tree_produk.bind('<Double-Button-1>', tab_produk_tersebut)
        tree_produk.pack()

    conn.commit()
    conn.close()





































# Function Kontak

def reset_tambah_kontak():
    e_nama_awal.delete(0, END)
    e_nama_akhir.delete(0, END)
    e_telp.delete(0, END)
    e_identitas.delete(0, END)
    e_email.delete(0, END)
    e_perusahaan.delete(0, END)
    e_handphone.delete(0, END)
    e_fax.delete(0, END)
    e_npwp.delete(0, END)
    e_alamat_kirim.delete(0, END)
    e_alamat_bayar.delete(0, END)


def hapus_kontak():
    conn = sqlite3.connect('kontak.db')
    c = conn.cursor()
    contacts = tree_kontak.selection()

    for contact in contacts:
        value = tree_kontak.item(contact)['values'][0]
        c.execute("DELETE from kontak WHERE email=?", (value,))  
        conn.commit()

    conn.close()

    tree_kontak.delete(*tree_kontak.get_children())
    query_kontak()


def tambah_kontak():
    
    conn = sqlite3.connect('kontak.db')
    c = conn.cursor()

    c.execute("""INSERT INTO kontak VALUES (
                :tipe,
                :nama,
                :telp,
                :identitas,
                :email,
                :perusahaan,
                :handphone,
                :fax,
                :npwp,
                :alamat_kirim,
                :alamat_bayar
                )""",
                {
                    'tipe': tipe_kontak.get(),
                    'nama': e_nama_awal.get() + ' ' + e_nama_akhir.get(),
                    'telp': e_telp.get(),
                    'identitas': e_identitas.get(),
                    'email': e_email.get(),
                    'perusahaan': e_perusahaan.get(),
                    'handphone': e_handphone.get(),
                    'fax': e_fax.get(),
                    'npwp': e_npwp.get(),
                    'alamat_kirim': e_alamat_kirim.get(),
                    'alamat_bayar': e_alamat_bayar.get()
                }
                )

    conn.commit()
    conn.close()

    tree_kontak.delete(*tree_kontak.get_children())
    query_kontak()
    reset_tambah_kontak()


def batal_tambah_kontak():
    notebook.hide(frame_tambah_kontak)
    notebook.select(frame_kontak)


def search_kontak():
    tree_kontak.delete(*tree_kontak.get_children())

    conn = sqlite3.connect('kontak.db')
    c = conn.cursor()

    c.execute("SELECT nama FROM kontak")
    contacts = list(c.fetchall())


    string = ''
    value = e_search_ktk.get()
    if value == '':
        query_kontak()

    for contact in contacts:
        for word in contact:
            string += word + '\n'


    with open('temp.txt', 'w') as f:
        f.write(string)


    with open('temp.txt', 'r') as f:
        for line in f:
            matched = re.match(rf'\d*\w*{value}\d*\w*', line, re.IGNORECASE)
            if matched:
                c.execute("SELECT *,oid FROM kontak WHERE nama=?", (line.replace('\n', ''),))
                matches = c.fetchall()
                for match in matches:
                    tree_kontak.insert("", END, text=match[1] + ' ' + match[2], values=(match[6], match[10], match[5], match[3], match[5]))
                    tree_kontak.bind('<Double-Button-1>', tab_kontak_tersebut)
                    tree_kontak.pack()


    conn.commit()
    conn.close()






































# Function Gambar Produk

def cari_gambar():
    global file_gambar
    file_gambar = filedialog.askopenfilename(initialdir =  "/", title = "Select A File", filetype =(("jpeg files","*.jpg"),("all files","*.*")))

    img = Image.open(file_gambar).resize((180, 180))
    photo = ImageTk.PhotoImage(img)

    btn_gambar.grid_forget()
    global gambar
    gambar = Label(frame_tambah_produk, image=photo)
    gambar.image = photo
    gambar.grid(column=2, row=2, sticky=W+E)


def save_gambar():
    with open(file_gambar, 'rb') as rf:
        with open('img/pdk/' + nama_produk + '.png', 'wb') as wf:
            chunk_size = 4096
            rf_chunk = rf.read(chunk_size)
            while len(rf_chunk) > 0:
                wf.write(rf_chunk)
                rf_chunk = rf.read(chunk_size)



# Function Produk

def reset_tambah_produk():
    e_nama_pdk.delete(0, END)
    e_sku.delete(0, END)
    e_kategori_pdk.delete(0, END)
    e_stok.delete(0, END)
    e_unit.delete(0, END)
    e_deskripsi.delete(0, END)
    e_batas_minimum.delete(0, END)
    e_harga_jual.delete(0, END)
    e_harga_beli.delete(0, END)


def hapus_produk():
    conn = sqlite3.connect('produk.db')
    c = conn.cursor()
    products = tree_produk.selection()

    for product in products:
        value = tree_produk.item(product)['values'][0]
        c.execute("DELETE from produk WHERE SKU=?", (value,))  
        conn.commit()

    conn.close()

    tree_produk.delete(*tree_produk.get_children())
    query_produk()



def tambah_produk():
    
    conn = sqlite3.connect('produk.db')
    c = conn.cursor()

    c.execute("""INSERT INTO produk VALUES (
                :nama,
                :SKU,
                :kategori,
                :unit,
                :deskripsi,
                :stok,
                :batas_minimum,
                :harga_jual,
                :harga_beli,
                :harga_beli_terakhir
                )""",
                {
                    'nama': e_nama_pdk.get(),
                    'SKU': e_sku.get(),
                    'kategori': e_kategori_pdk.get(),
                    'unit': e_unit.get(),
                    'deskripsi': e_deskripsi.get(),
                    'stok': e_stok.get(),
                    'batas_minimum': e_batas_minimum.get() or 1,
                    'harga_jual': e_harga_jual.get(),
                    'harga_beli': e_harga_beli.get(),
                    'harga_beli_terakhir': '-'
                }
                )

    conn.commit()
    conn.close()

    global nama_produk
    nama_produk = e_nama_pdk.get()
    save_gambar()

    gambar.grid_forget()
    btn_gambar.grid(columnspan=4, column=2, row=2, pady=(20,130), sticky=W+E)

    tree_produk.delete(*tree_produk.get_children())
    query_produk()
    reset_tambah_produk()



def batal_tambah_produk():
    notebook.hide(frame_tambah_produk)
    notebook.select(frame_produk)


def search_produk():
    tree_produk.delete(*tree_produk.get_children())

    conn = sqlite3.connect('produk.db')
    c = conn.cursor()

    c.execute("SELECT nama FROM produk")
    products = list(c.fetchall())


    string = ''
    value = e_search_pdk.get()
    if value == '':
        query_produk()

    for product in products:
        for word in product:
            string += word + '\n'


    with open('temp.txt', 'w') as f:
        f.write(string)


    with open('temp.txt', 'r') as f:
        for line in f:
            matched = re.match(rf'\d*\w*{value}\d*\w*', line, re.IGNORECASE)
            if matched:
                c.execute("SELECT *,oid FROM produk WHERE nama=?", (line.replace('\n', ''),))
                matches = c.fetchall()
                for match in matches:
                    tree_produk.insert("", END, text=match[0], values=(match[1], match[5], match[6], match[3], match[7], match[8], match[9], match[2]))
                    tree_produk.bind('<Double-Button-1>', tab_produk_tersebut)
                    tree_produk.pack()


    conn.commit()
    conn.close()





































# Buat Window
root = Tk()
root.title('PDF Generator')
root.geometry('1275x725')



# Buat Tab

ttk.Style().configure('Custom.TNotebook.Tab', padding=[7, 7], font=('Helvetica', 10))

notebook = ttk.Notebook(root, style='Custom.TNotebook')
notebook.pack(pady=5)


# Tab Luar
frame_penjualan = Frame(notebook, width=750, height=600)
frame_pembelian = Frame(notebook, width=750, height=600)
frame_kontak = Frame(notebook, width=750, height=600)
frame_produk = Frame(notebook, width=750, height=600)

frame_penjualan.pack(fill='both', expand=1)
frame_pembelian.pack(fill='both', expand=1)
frame_kontak.pack(fill='both', expand=1)
frame_produk.pack(fill='both', expand=1)

notebook.add(frame_kontak, text='Kontak')
notebook.add(frame_produk, text='Produk')
notebook.add(frame_penjualan, text='Penjualan')
notebook.add(frame_pembelian, text='Pembelian')


# Frame Dalam
frame_dalam_kontak = Frame(frame_kontak, width=750, height=400)
frame_dalam_produk = Frame(frame_produk, width=750, height=450)

frame_dalam_kontak.grid(row=6, columnspan=7)
frame_dalam_produk.grid(row=7, columnspan=3)


# Tab Tambah Kontak
frame_tambah_kontak = Frame(notebook, width=750, height=600)

def tab_tambah_kontak():
    frame_tambah_kontak.pack(fill='both', expand=1)
    notebook.add(frame_tambah_kontak, text='Tambah Kontak')
    notebook.select(frame_tambah_kontak)


# Tab Tambah Produk
frame_tambah_produk = Frame(notebook, width=750, height=600)

def tab_tambah_produk():
    frame_tambah_produk.pack(fill='both', expand=1)
    notebook.add(frame_tambah_produk, text='Tambah Produk')
    notebook.select(frame_tambah_produk)






































# Tab Kontak Tersebut
def tab_kontak_tersebut(event):

    def tutup_kontak():
        notebook.hide(frame_kontak_tersebut)
        notebook.select(frame_kontak)


    contact = tree_kontak.selection()
    conn = sqlite3.connect('kontak.db')
    c = conn.cursor()
    
    value = tree_kontak.item(contact)['values'][2]
    c.execute("SELECT * FROM kontak WHERE email=?", (value,))
    contact_data = c.fetchone()


    frame_kontak_tersebut = Frame(notebook, width=750, height=600)
    frame_kontak_tersebut.pack(fill='both', expand=1)
    notebook.add(frame_kontak_tersebut, text=contact_data[1] + ' ' + contact_data[2])
    notebook.select(frame_kontak_tersebut)


    lb_kontak_tersebut = Label(frame_kontak_tersebut,  text='Info Kontak', font=("Helvetica", 20))
    btn_tutup_kontak = Button(frame_kontak_tersebut,  text='Tutup', bg='tomato', font=("Helvetica", 12), command=tutup_kontak)

    lb_tipe = Label(frame_kontak_tersebut, text='Tipe Kontak', font=("Times New Roman", 12))
    lb_nama_awal = Label(frame_kontak_tersebut, text='Nama Awal', font=("Times New Roman", 12))
    lb_nama_akhir = Label(frame_kontak_tersebut, text='Nama Akhir', font=("Times New Roman", 12))
    lb_telp = Label(frame_kontak_tersebut, text='No. Telphone', font=("Times New Roman", 12))
    lb_identitas = Label(frame_kontak_tersebut, text='No. Identitas', font=("Times New Roman", 12))
    lb_email = Label(frame_kontak_tersebut, text='Email', font=("Times New Roman", 12))
    lb_perusahaan = Label(frame_kontak_tersebut, text='Nama Perusahaan', font=("Times New Roman", 12))
    lb_handphone = Label(frame_kontak_tersebut, text='No. Handphone', font=("Times New Roman", 12))
    lb_fax = Label(frame_kontak_tersebut, text='Fax', font=("Times New Roman", 12))
    lb_npwp = Label(frame_kontak_tersebut, text='No. NPWP', font=("Times New Roman", 12))
    lb_alamat_kirim = Label(frame_kontak_tersebut, text='Alamat Pengiriman', font=("Times New Roman", 12))
    lb_alamat_bayar = Label(frame_kontak_tersebut, text='Alamat Pembayaran', font=("Times New Roman", 12))


    lbl_tipe = Label(frame_kontak_tersebut, text=contact_data[0], font=("Times New Roman", 12))
    lbl_nama_awal = Label(frame_kontak_tersebut, text=contact_data[1], font=("Times New Roman", 12))
    lbl_nama_akhir = Label(frame_kontak_tersebut, text=contact_data[2], font=("Times New Roman", 12))
    lbl_telp = Label(frame_kontak_tersebut, text=contact_data[3], font=("Times New Roman", 12))
    lbl_identitas = Label(frame_kontak_tersebut, text=contact_data[4], font=("Times New Roman", 12))
    lbl_email = Label(frame_kontak_tersebut, text=contact_data[5], font=("Times New Roman", 12))
    lbl_perusahaan = Label(frame_kontak_tersebut, text=contact_data[6], font=("Times New Roman", 12))
    lbl_handphone = Label(frame_kontak_tersebut, text=contact_data[7], font=("Times New Roman", 12))
    lbl_fax = Label(frame_kontak_tersebut, text=contact_data[8], font=("Times New Roman", 12))
    lbl_npwp = Label(frame_kontak_tersebut, text=contact_data[9], font=("Times New Roman", 12))
    lbl_alamat_kirim = Label(frame_kontak_tersebut, text=contact_data[10], font=("Times New Roman", 12))
    lbl_alamat_bayar = Label(frame_kontak_tersebut, text=contact_data[11], font=("Times New Roman", 12))


    # Grid
    lb_kontak_tersebut.grid(sticky=W, row=1, padx=40, pady=20)
    btn_tutup_kontak.grid(sticky=E, column=5, pady=20, row=1)

    lb_tipe.grid(columnspan=2, row=2, pady=(20,0), sticky=W)
    lb_nama_awal.grid(columnspan=2, row=3, pady=(20,0), sticky=W)
    lb_nama_akhir.grid(columnspan=2, row=4, pady=(20,0), sticky=W)
    lb_telp.grid(columnspan=2, row=5, pady=(20,0), sticky=W)
    lb_identitas .grid(columnspan=2, row=6, pady=(20,0), sticky=W)
    lb_email .grid(columnspan=2, row=7, pady=(20,0), sticky=W)
    lb_perusahaan.grid(columnspan=2, row=8, pady=(20,0), sticky=W)
    lb_handphone.grid(columnspan=2, row=9, pady=(20,0), sticky=W)
    lb_fax.grid(columnspan=2, row=10, pady=(20,0), sticky=W)
    lb_npwp.grid(columnspan=2, row=11, pady=(20,0), sticky=W)
    lb_alamat_kirim.grid(columnspan=2, row=12, pady=(20,0), sticky=W)
    lb_alamat_bayar.grid(columnspan=2, row=13, pady=(20,0), sticky=W)


    lbl_tipe.grid(columnspan=4, column=2, row=2, pady=(20,0), sticky=W)
    lbl_nama_awal.grid(columnspan=4, column=2, row=3, pady=(20,0), sticky=W)
    lbl_nama_akhir.grid(columnspan=4, column=2, row=4, pady=(20,0), sticky=W)
    lbl_telp.grid(columnspan=4, column=2, row=5, pady=(20,0), sticky=W)
    lbl_identitas.grid(columnspan=4, column=2, row=6, pady=(20,0), sticky=W)
    lbl_email.grid(columnspan=4, column=2, row=7, pady=(20,0), sticky=W)
    lbl_perusahaan.grid(columnspan=4, column=2, row=8, pady=(20,0), sticky=W)
    lbl_handphone.grid(columnspan=4, column=2, row=9, pady=(20,0), sticky=W)
    lbl_fax.grid(columnspan=4, column=2, row=10, pady=(20,0), sticky=W)
    lbl_npwp.grid(columnspan=4, column=2, row=11, pady=(20,0), sticky=W)
    lbl_alamat_kirim.grid(columnspan=4, column=2, row=12, pady=(20,0), sticky=W)
    lbl_alamat_bayar.grid(columnspan=4, column=2, row=13, pady=(20,0), sticky=W)

        
    conn.close()

















# Tab Kontak

lb_kontak = Label(frame_kontak,  text='Kontak', font=("Helvetica", 20))
btn_tambah_kontak = Button(frame_kontak, text='Kontak Baru', font=("Times New Roman", 12), command=tab_tambah_kontak)

btn_semua_tipe = Button(frame_kontak, text='Semua Tipe', font=("Times New Roman", 12))
btn_pembeli = Button(frame_kontak, text='Pembeli', font=("Times New Roman", 12))
btn_supplier = Button(frame_kontak, text='Supplier', font=("Times New Roman", 12))
btn_karyawan = Button(frame_kontak, text='Karyawan', font=("Times New Roman", 12))
btn_lainnya = Button(frame_kontak, text='Lainnya', font=("Times New Roman", 12))

btn_hapus_kontak = Button(frame_kontak, bg='lightgray', text='Hapus', font=("Times New Roman", 12), command=hapus_kontak)
e_search_ktk = Entry(frame_kontak)
btn_search_ktk = Button(frame_kontak, bg='lightgray', text='Search', font=("Times New Roman", 12), command=search_kontak)


# Grid Kontak
lb_kontak.grid(columnspan=2, row=1, sticky=W, padx=40, pady=20)
btn_tambah_kontak.grid(column= 6, row=1, padx=10, pady=20)

btn_pembeli.grid(column=0, row=3, padx=10, pady=20, sticky=W+E)
btn_supplier.grid(column=1, row=3, padx=10, pady=20, sticky=W+E)
btn_karyawan.grid(column=2, row=3, padx=10, pady=20, sticky=W+E)
btn_lainnya.grid(column=3, row=3, padx=10, pady=20, sticky=W+E)
btn_semua_tipe.grid(column=4, row=3, padx=10, pady=20, sticky=W+E)

btn_hapus_kontak.grid(column=4, row=8, padx=(0, 40), pady=20, sticky=E)
e_search_ktk.grid(column=5, row=8, pady=20, sticky=W+E)
btn_search_ktk.grid(column=6, row=8, padx=(10, 40), pady=20, sticky=W)

e_search_ktk.focus()


# Treeview Kontak

tree_kontak = ttk.Treeview(frame_dalam_kontak)

scrlbar_ktk = ttk.Scrollbar(frame_dalam_kontak, orient ="vertical", command = tree_kontak.yview)
scrlbar_ktk.pack(side='right', fill=Y)
tree_kontak.configure(yscrollcommand = scrlbar_ktk.set, height=20)

tree_kontak["columns"]=("one", "two", "three", "four", "five")
tree_kontak.column("#0", width=200, minwidth=100, stretch=NO)
tree_kontak.column("one", width=200, minwidth=100, stretch=NO)
tree_kontak.column("two", width=400, minwidth=100, stretch=NO)
tree_kontak.column("three", width=150, minwidth=100, stretch=NO)
tree_kontak.column("four", width=150, minwidth=100, stretch=NO)
tree_kontak.column("five", width=150, minwidth=100, stretch=NO)

tree_kontak.heading("#0", text="     Nama", anchor=W)
tree_kontak.heading("one", text="Nama Perusahaan", anchor=W)
tree_kontak.heading("two", text="Alamat", anchor=W)
tree_kontak.heading("three", text="Email", anchor=W)
tree_kontak.heading("four", text="No. Telp", anchor=W)
tree_kontak.heading("five", text="Saldo", anchor=W)

query_kontak()
tree_kontak.pack()



















# Tab Tambah Kontak

lb_tambah_kontak = Label(frame_tambah_kontak,  text='Info Kontak', font=("Helvetica", 20))

lb_tipe = Label(frame_tambah_kontak, text='Tipe Kontak', font=("Times New Roman", 12))
lb_nama_awal = Label(frame_tambah_kontak, text='Nama Awal', font=("Times New Roman", 12))
lb_nama_akhir = Label(frame_tambah_kontak, text='Nama Akhir', font=("Times New Roman", 12))
lb_telp = Label(frame_tambah_kontak, text='No. Telphone', font=("Times New Roman", 12))
lb_identitas = Label(frame_tambah_kontak, text='No. Identitas', font=("Times New Roman", 12))
lb_email = Label(frame_tambah_kontak, text='Email', font=("Times New Roman", 12))
lb_perusahaan = Label(frame_tambah_kontak, text='Nama Perusahaan', font=("Times New Roman", 12))
lb_handphone = Label(frame_tambah_kontak, text='No. Handphone', font=("Times New Roman", 12))
lb_fax = Label(frame_tambah_kontak, text='Fax', font=("Times New Roman", 12))
lb_npwp = Label(frame_tambah_kontak, text='No. NPWP', font=("Times New Roman", 12))
lb_alamat_kirim = Label(frame_tambah_kontak, text='Alamat Pengiriman', font=("Times New Roman", 12))
lb_alamat_bayar = Label(frame_tambah_kontak, text='Alamat Pembayaran', font=("Times New Roman", 12))

tipe_kontak = StringVar()
tipe_kontak.set('Pembeli')
rd_pembeli = Radiobutton(frame_tambah_kontak, text='Pembeli', variable=tipe_kontak, value='Pembeli')
rd_supplier = Radiobutton(frame_tambah_kontak, text='Supplier', variable=tipe_kontak, value='Supplier')
rd_karyawan = Radiobutton(frame_tambah_kontak, text='Karyawan', variable=tipe_kontak, value='Karyawan')
rd_lainnya = Radiobutton(frame_tambah_kontak, text='Lainnya', variable=tipe_kontak, value='Lainnya')

e_nama_awal = Entry(frame_tambah_kontak, width=70)
e_nama_akhir = Entry(frame_tambah_kontak)
e_telp = Entry(frame_tambah_kontak)
e_identitas = Entry(frame_tambah_kontak)
e_email = Entry(frame_tambah_kontak)
e_perusahaan = Entry(frame_tambah_kontak)
e_handphone = Entry(frame_tambah_kontak)
e_fax = Entry(frame_tambah_kontak)
e_npwp = Entry(frame_tambah_kontak)
e_alamat_kirim = Entry(frame_tambah_kontak)
e_alamat_bayar = Entry(frame_tambah_kontak)

btn_batal_tambah_kontak = Button(frame_tambah_kontak, text='Batal', font=("Times New Roman", 12), bg='red', command=batal_tambah_kontak)
btn_reset_tambah_kontak = Button(frame_tambah_kontak, text='Reset', font=("Times New Roman", 12), bg='silver', command=reset_tambah_kontak)
btn_tambah_kontak = Button(frame_tambah_kontak, text='Tambah', font=("Times New Roman", 12), bg='lightgreen', command=tambah_kontak)


# Grid
lb_tambah_kontak.grid(sticky=W, padx=40, pady=20)

lb_tipe.grid(columnspan=2, row=1, pady=(20,0), sticky=W)
lb_nama_awal.grid(columnspan=2, row=3, pady=(20,0), sticky=W)
lb_nama_akhir.grid(columnspan=2, row=4, pady=(20,0), sticky=W)
lb_telp.grid(columnspan=2, row=5, pady=(20,0), sticky=W)
lb_identitas .grid(columnspan=2, row=6, pady=(20,0), sticky=W)
lb_email .grid(columnspan=2, row=7, pady=(20,0), sticky=W)
lb_perusahaan.grid(columnspan=2, row=8, pady=(20,0), sticky=W)
lb_handphone.grid(columnspan=2, row=9, pady=(20,0), sticky=W)
lb_fax.grid(columnspan=2, row=10, pady=(20,0), sticky=W)
lb_npwp.grid(columnspan=2, row=11, pady=(20,0), sticky=W)
lb_alamat_kirim.grid(columnspan=2, row=12, pady=(20,0), sticky=W)
lb_alamat_bayar.grid(columnspan=2, row=13, pady=(20,0), sticky=W)

rd_pembeli.grid(column=2, row=1, pady=(20,0))
rd_supplier.grid(column=3, row=1, pady=(20,0))
rd_karyawan.grid(column=4, row=1, pady=(20,0))
rd_lainnya.grid(column=5, row=1, pady=(20,0))

e_nama_awal.grid(columnspan=4, column=2, row=3, pady=(20,0), sticky=W+E)
e_nama_akhir.grid(columnspan=4, column=2, row=4, pady=(20,0), sticky=W+E)
e_telp.grid(columnspan=4, column=2, row=5, pady=(20,0), sticky=W+E)
e_identitas .grid(columnspan=4, column=2, row=6, pady=(20,0), sticky=W+E)
e_email .grid(columnspan=4, column=2, row=7, pady=(20,0), sticky=W+E)
e_perusahaan.grid(columnspan=4, column=2, row=8, pady=(20,0), sticky=W+E)
e_handphone.grid(columnspan=4, column=2, row=9, pady=(20,0), sticky=W+E)
e_fax.grid(columnspan=4, column=2, row=10, pady=(20,0), sticky=W+E)
e_npwp.grid(columnspan=4, column=2, row=11, pady=(20,0), sticky=W+E)
e_alamat_kirim.grid(columnspan=4, column=2, row=12, pady=(20,0), sticky=W+E)
e_alamat_bayar.grid(columnspan=4, column=2, row=13, pady=(20,0), sticky=W+E)

btn_batal_tambah_kontak.grid(column=3, row=15, pady=(20,0), sticky=W+E)
btn_reset_tambah_kontak.grid(column=4, row=15, pady=(20,0), sticky=W+E)
btn_tambah_kontak.grid(column=5, row=15, pady=(20,0), sticky=W+E)















































# Tab Produk Tersebut
def tab_produk_tersebut(event):

    def tutup_produk():
        notebook.hide(frame_produk_tersebut)
        notebook.select(frame_produk)


    product = tree_produk.selection()
    conn = sqlite3.connect('produk.db')
    c = conn.cursor()
    
    value = tree_produk.item(product)['values'][0]
    c.execute("SELECT * FROM produk WHERE sku=?", (value,))
    product_data = c.fetchone()


    frame_produk_tersebut = Frame(notebook, width=750, height=600)
    frame_produk_tersebut.pack(fill='both', expand=1)
    notebook.add(frame_produk_tersebut, text=product_data[0])
    notebook.select(frame_produk_tersebut)


    lb_produk_tersebut = Label(frame_produk_tersebut,  text='Info Produk', font=("Helvetica", 20))
    btn_tutup_produk = Button(frame_produk_tersebut,  text='Tutup', bg='tomato', font=("Helvetica", 12), command=tutup_produk)

    img = Image.open('img/pdk/' + product_data[0] + '.png').resize((180, 180))
    photo = ImageTk.PhotoImage(img)
    gambar = Label(frame_produk_tersebut, image=photo)

    lb_nama_pdk = Label(frame_produk_tersebut, text='Nama Produk', font=("Times New Roman", 12))
    lb_sku = Label(frame_produk_tersebut, text='Kode SKU', font=("Times New Roman", 12))
    lb_kategori_pdk = Label(frame_produk_tersebut, text='Kategori', font=("Times New Roman", 12))
    lb_stok = Label(frame_produk_tersebut, text='Stok', font=("Times New Roman", 12))
    lb_unit = Label(frame_produk_tersebut, text='Unit', font=("Times New Roman", 12))
    lb_deskripsi = Label(frame_produk_tersebut, text='Deskripsi', font=("Times New Roman", 12))
    lb_batas_minimum = Label(frame_produk_tersebut, text='Batas Minimum', font=("Times New Roman", 12))
    lb_harga_beli = Label(frame_produk_tersebut, text='Harga Beli', font=("Times New Roman", 12))
    lb_harga_jual = Label(frame_produk_tersebut, text='Harga Jual', font=("Times New Roman", 12))
    lb_harga_beli_terakhir = Label(frame_produk_tersebut, text='Harga Beli Terakhir', font=("Times New Roman", 12))

    
    lbl_nama_pdk = Label(frame_produk_tersebut, text=product_data[0], font=("Times New Roman", 12))
    lbl_sku = Label(frame_produk_tersebut, text=product_data[1], font=("Times New Roman", 12))
    lbl_kategori_pdk = Label(frame_produk_tersebut, text=product_data[2], font=("Times New Roman", 12))
    lbl_stok = Label(frame_produk_tersebut, text=product_data[5], font=("Times New Roman", 12))
    lbl_unit = Label(frame_produk_tersebut, text=product_data[3], font=("Times New Roman", 12))
    lbl_deskripsi = Label(frame_produk_tersebut, text=product_data[4], font=("Times New Roman", 12))
    lbl_batas_minimum = Label(frame_produk_tersebut, text=product_data[6], font=("Times New Roman", 12))
    lbl_harga_beli = Label(frame_produk_tersebut, text=product_data[8], font=("Times New Roman", 12))
    lbl_harga_jual = Label(frame_produk_tersebut, text=product_data[7], font=("Times New Roman", 12))
    lbl_harga_beli_terakhir = Label(frame_produk_tersebut, text=product_data[9], font=("Times New Roman", 12))


    # Grid
    lb_produk_tersebut.grid(sticky=W, row=1, padx=40, pady=20)
    btn_tutup_produk.grid(sticky=E, column=5, pady=20, row=1)

    gambar.image = photo
    gambar.grid(column=0, row=2, sticky=W+E)

    lb_nama_pdk.grid(columnspan=2, row=3, pady=(20,0), sticky=W)
    lb_sku.grid(columnspan=2, row=4, pady=(20,0), sticky=W)
    lb_kategori_pdk.grid(columnspan=2, row=5, pady=(20,0), sticky=W)
    lb_stok.grid(columnspan=2, row=6, pady=(20,0), sticky=W)
    lb_unit.grid(column=4, row=6, pady=(20,0))
    lb_deskripsi.grid(columnspan=2, row=7, pady=(20,0), sticky=W)
    lb_batas_minimum.grid(columnspan=2, row=8, pady=(20,0), sticky=W)
    lb_harga_beli.grid(columnspan=2, row=9, pady=(20,0), sticky=W)
    lb_harga_jual.grid(columnspan=2, row=10, pady=(20,0), sticky=W)
    lb_harga_beli_terakhir.grid(columnspan=2, row=11, pady=(20,0), sticky=W)


    lbl_nama_pdk.grid(columnspan=4, column=2, row=3, pady=(20,0), sticky=W)
    lbl_sku.grid(columnspan=4, column=2, row=4, pady=(20,0), sticky=W)
    lbl_kategori_pdk.grid(columnspan=4, column=2, row=5, pady=(20,0), sticky=W)
    lbl_stok.grid(columnspan=2, column=2, row=6, pady=(20,0), sticky=W)
    lbl_unit.grid(column=5, row=6, pady=(20,0), sticky=W)
    lbl_deskripsi.grid(columnspan=4, column=2, row=7, pady=(20,0), sticky=W)
    lbl_batas_minimum.grid(columnspan=4, column=2, row=8, pady=(20,0), sticky=W)
    lbl_harga_beli.grid(columnspan=4, column=2, row=9, pady=(20,0), sticky=W)
    lbl_harga_jual.grid(columnspan=4, column=2, row=10, pady=(20,0), sticky=W)
    lbl_harga_beli_terakhir.grid(columnspan=4, column=2, row=11, pady=(20,0), sticky=W)

        
    conn.close()























# Tab Produk

lb_produk = Label(frame_produk,  text='Produk', font=("Helvetica", 20))
btn_tambah_produk = Button(frame_produk, text='Produk Baru', font=("Times New Roman", 12), command=tab_tambah_produk)

lb_tersedia = Label(frame_produk, bg='cyan', text='Produk Tersedia', font=("Times New Roman", 12))
lb_rendah = Label(frame_produk, bg='cyan', text='Produk Rendah', font=("Times New  Roman", 12))
lb_habis = Label(frame_produk, bg='cyan', text='Produk Habis', font=("Times New Roman", 12))

btn_hapus_produk = Button(frame_produk, bg='lightgray', text='Hapus', font=("Times New Roman", 12), command=hapus_produk)
e_search_pdk = Entry(frame_produk)
btn_search_pdk = Button(frame_produk, bg='lightgray', text='Search', font=("Times New Roman", 12), command=search_produk)


# Grid Produk
lb_produk.grid(columnspan=2, row=1, sticky=W, padx=40, pady=20)
btn_tambah_produk.grid(column= 2, row=1, padx=10, pady=20, sticky=E)

lb_tersedia.grid(column=0, row=6, pady=20, padx=30, sticky=W+E)
lb_rendah.grid(column=1, row=6, pady=20, padx=30, sticky=W+E)
lb_habis.grid(column=2, row=6, pady=20, padx=30, sticky=W+E)

btn_hapus_produk.grid(column=1, row=8, padx=(0, 40), pady=20, sticky=E)
e_search_pdk.grid(column=2, row=8, padx=(120, 0), ipadx=50, pady=20, sticky=W)
btn_search_pdk.grid(column=2, row=8, padx=(0, 40), pady=20, sticky=E)

e_search_pdk.focus()


# Treeview Produk
tree_produk = ttk.Treeview(frame_dalam_produk)

scrlbar_pdk = ttk.Scrollbar(frame_dalam_produk, orient ="vertical", command = tree_produk.yview)
scrlbar_pdk.pack(side=RIGHT, fill=Y)
tree_produk.configure(yscrollcommand = scrlbar_pdk.set, height=20)

tree_produk["columns"]=("one", "two", "three", "four", "five", "six", "seven", "eight")
tree_produk.column("#0", width=200, minwidth=100, stretch=NO)
tree_produk.column("one", width=150, minwidth=80, stretch=NO)
tree_produk.column("two", width=50, minwidth=50, stretch=NO)
tree_produk.column("three", width=40, minwidth=30, stretch=NO)
tree_produk.column("four", width=70, minwidth=50, stretch=NO)
tree_produk.column("five", width=150, minwidth=100, stretch=NO)
tree_produk.column("six", width=150, minwidth=100, stretch=NO)
tree_produk.column("seven", width=150, minwidth=100, stretch=NO)
tree_produk.column("eight", width=120, minwidth=80, stretch=NO)

tree_produk.heading("#0", text="     Nama Produk", anchor=W)
tree_produk.heading("one", text="Kode Produk", anchor=W)
tree_produk.heading("two", text="Qty", anchor=W)
tree_produk.heading("three", text="Min", anchor=W)
tree_produk.heading("four", text="Unit", anchor=W)
tree_produk.heading("five", text="Harga Jual", anchor=W)
tree_produk.heading("six", text="Harga Beli", anchor=W)
tree_produk.heading("seven", text="Harga Terakhir Beli", anchor=W)
tree_produk.heading("eight", text="Kategori", anchor=W)

query_produk()
tree_produk.pack(side=LEFT)

















# Tab Tambah Produk
lb_tambah_produk = Label(frame_tambah_produk,  text='Info Produk', font=("Helvetica", 20))

lb_gambar = Label(frame_tambah_produk, text='Gambar Produk', font=("Times New Roman", 12))
lb_nama_pdk = Label(frame_tambah_produk, text='Nama Produk', font=("Times New Roman", 12))
lb_sku = Label(frame_tambah_produk, text='Kode SKU', font=("Times New Roman", 12))
lb_kategori_pdk = Label(frame_tambah_produk, text='Kategori', font=("Times New Roman", 12))
lb_stok = Label(frame_tambah_produk, text='Stok', font=("Times New Roman", 12))
lb_unit = Label(frame_tambah_produk, text='Unit', font=("Times New Roman", 12))
lb_deskripsi = Label(frame_tambah_produk, text='Deskripsi', font=("Times New Roman", 12))
lb_batas_minimum = Label(frame_tambah_produk, text='Batas Minimum', font=("Times New Roman", 12))
lb_harga_beli = Label(frame_tambah_produk, text='Harga Beli', font=("Times New Roman", 12))
lb_harga_jual = Label(frame_tambah_produk, text='Harga Jual', font=("Times New Roman", 12))

btn_gambar = Button(frame_tambah_produk, text = "Browse Image", command=cari_gambar)

e_nama_pdk = Entry(frame_tambah_produk)
e_sku = Entry(frame_tambah_produk)
e_kategori_pdk = Entry(frame_tambah_produk)
e_stok = Entry(frame_tambah_produk)
e_unit = Entry(frame_tambah_produk)
e_deskripsi = Entry(frame_tambah_produk)
e_batas_minimum = Entry(frame_tambah_produk)
e_harga_jual = Entry(frame_tambah_produk)
e_harga_beli = Entry(frame_tambah_produk)

btn_batal_tambah_produk = Button(frame_tambah_produk, text='Batal', font=("Times New Roman", 12), bg='red', command=batal_tambah_produk)
btn_reset_tambah_produk = Button(frame_tambah_produk, text='Reset', font=("Times New Roman", 12), bg='silver', command=reset_tambah_produk)
btn_tambah_produk = Button(frame_tambah_produk, text='Tambah', font=("Times New Roman", 12), bg='lightgreen', command=tambah_produk)


# Grid
lb_tambah_produk.grid(sticky=W, padx=40, pady=20)

lb_gambar.grid(columnspan=2, row=2, pady=(20,130), sticky=W)
lb_nama_pdk.grid(columnspan=2, row=3, pady=(20,0), sticky=W)
lb_sku.grid(columnspan=2, row=4, pady=(20,0), sticky=W)
lb_kategori_pdk.grid(columnspan=2, row=5, pady=(20,0), sticky=W)
lb_stok.grid(columnspan=2, row=6, pady=(20,0), sticky=W)
lb_unit.grid(column=4, row=6, pady=(20,0))
lb_deskripsi.grid(columnspan=2, row=7, pady=(20,0), sticky=W)
lb_batas_minimum.grid(columnspan=2, row=8, pady=(20,0), sticky=W)
lb_harga_beli.grid(columnspan=2, row=9, pady=(20,0), sticky=W)
lb_harga_jual.grid(columnspan=2, row=10, pady=(20,0), sticky=W)

btn_gambar.grid(columnspan=4, column=2, row=2, pady=(20,130), sticky=W+E)

e_nama_pdk.grid(columnspan=4, column=2, row=3, pady=(20,0), sticky=W+E)
e_sku.grid(columnspan=4, column=2, row=4, pady=(20,0), sticky=W+E)
e_kategori_pdk.grid(columnspan=4, column=2, row=5, pady=(20,0), sticky=W+E)
e_stok.grid(columnspan=2, column=2, row=6, pady=(20,0), sticky=W+E)
e_unit.grid(column=5, row=6, pady=(20,0), sticky=W+E)
e_deskripsi.grid(columnspan=4, column=2, row=7, pady=(20,0), sticky=W+E)
e_batas_minimum.grid(columnspan=4, column=2, row=8, pady=(20,0), sticky=W+E)
e_harga_beli.grid(columnspan=4, column=2, row=9, pady=(20,0), sticky=W+E)
e_harga_jual.grid(columnspan=4, column=2, row=10, pady=(20,0), sticky=W+E)

btn_batal_tambah_produk.grid(column=3, row=15, pady=(20,0), sticky=W+E)
btn_reset_tambah_produk.grid(column=4, row=15, pady=(20,0), sticky=W+E)
btn_tambah_produk.grid(column=5, row=15, pady=(20,0), sticky=W+E)



root.mainloop()