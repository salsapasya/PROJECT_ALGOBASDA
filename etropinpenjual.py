import psycopg2
from psycopg2 import Error
from tabulate import tabulate
import os
from datetime import datetime

def connect_db():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="Zalfa123",
            host="localhost",
            port="1986",
            database="etropin4"
        )
        return connection
    except Error as error:
        print("Terjadi kesalahan, gagal terkoneksi dengan database", error)
        return

def clear_all():
    os.system('cls')

# ===========================
# MAIN MENU & LOGIN/REGISTER
# ===========================

def main_menu():
    print('''
==========================================          
    SISTEM MARKETPLACE PRODUK PERTANIAN  
==========================================

        1. Register
        2. Login
        3. Keluar
        ''')
    select_menu = input("Pilih Menu (1-3): ")
    
    if select_menu == "1":
        clear_all()
        register()
    elif select_menu == "2":
        clear_all()
        login()
    elif select_menu == "3":
        print("Terima kasih! Sampai jumpa.")
        exit()
    else:
        print("Pilihan tidak valid!")
        input("Tekan Enter...")
        clear_all()
        main_menu()

def register():
    print('''=== PILIH TIPE AKUN ===
    1. Penjual (Petani)
    2. Pembeli
''')
    tipe = input("Pilih (1/2): ")
    
    if tipe == "1":
        clear_all()
        register_user("penjual")
    elif tipe == "2":
        clear_all()
        register_user("pembeli")
    else:
        print("Pilihan tidak valid!")
        input("Tekan Enter...")
        clear_all()
        register()

def register_user(role):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        
        print(f"=== REGISTER {role.upper()} ===\n")
        
        nama = input("Nama Lengkap: ")
        alamat = input("Alamat: ")
        nomor_telepon = input("Nomor Telepon: ")
        username = input("Username: ")
        password = input("Password: ")
        
        cursor.execute("SELECT username_pengguna FROM pengguna WHERE username_pengguna = %s", (username,))
        if cursor.fetchone():
            print("\n❌ Username sudah terdaftar!")
            input("Tekan Enter...")
            cursor.close()
            connection.close()
            clear_all()
            register_user(role)
            return
        
        query = """
        INSERT INTO pengguna (nama_pengguna, alamat_pengguna, no_telp_pengguna, username_pengguna, password_pengguna, role)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nama, alamat, nomor_telepon, username, password, role))
        connection.commit()
        
        print(f"\n✅ Registrasi {role} berhasil!")
        print(f"Selamat datang, {nama}!")
        
        cursor.close()
        connection.close()
        input("\nTekan Enter kembali ke menu...")
        clear_all()
        main_menu()
        
    except Error as error:
        print(f"\n❌ Error: {error}")
        if connection:
            connection.rollback()
            connection.close()
        input("Tekan Enter...")
        clear_all()
        main_menu()

def login():
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        
        print("=== LOGIN ===\n")
        
        username = input("Username: ")
        password = input("Password: ")
        
        if username == "admin" and password == "admin123":
            print("\n✅ Login berhasil sebagai ADMIN!")
            input("Tekan Enter...")
            cursor.close()
            connection.close()
            clear_all()
            menu_admin(0, "Administrator")
            return
        
        query = """
        SELECT id_pengguna, nama_pengguna, role 
        FROM pengguna 
        WHERE username_pengguna = %s AND password_pengguna = %s
        """
        cursor.execute(query, (username, password))
        user_data = cursor.fetchone()
        
        if user_data:
            id_pengguna = user_data[0]
            nama_pengguna = user_data[1]
            role = user_data[2]
            
            print(f"\n✅ Login berhasil!")
            print(f"Selamat datang, {nama_pengguna}!")
            
            cursor.close()
            connection.close()
            input("\nTekan Enter...")
            clear_all()
            
            if role == "penjual":
                menu_penjual(id_pengguna, nama_pengguna)
            elif role == "pembeli":
                menu_pembeli(id_pengguna, nama_pengguna)
        else:
            print("\n❌ Username atau Password salah!")
            cursor.close()
            connection.close()
            input("Tekan Enter...")
            clear_all()
            login()
            
    except Error as error:
        print(f"\n❌ Error: {error}")
        if connection:
            connection.close()
        input("Tekan Enter...")
        clear_all()
        main_menu()

# ===========================
# MENU ADMIN
# ===========================

def menu_admin(id_pengguna, nama_pengguna):
    print(f'''
=== MENU ADMIN ===
Halo, {nama_pengguna}!

1. Cek Pesanan (Ubah Status)
2. Kelola Pasar (Ubah Data)
3. Lihat Semua Pengguna
4. Logout
''')
    pilihan = input("Pilih Menu (1-4): ")
    
    if pilihan == "1":
        clear_all()
        admin_cek_pesanan(id_pengguna, nama_pengguna)
    elif pilihan == "2":
        clear_all()
        admin_kelola_pasar(id_pengguna, nama_pengguna)
    elif pilihan == "3":
        clear_all()
        admin_lihat_pengguna(id_pengguna, nama_pengguna)
    elif pilihan == "4":
        clear_all()
        print("Logout berhasil!")
        main_menu()
    else:
        print("Pilihan tidak valid!")
        input("Tekan Enter...")
        clear_all()
        menu_admin(id_pengguna, nama_pengguna)

def admin_cek_pesanan(id_pengguna, nama_pengguna):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        
        # Tampilkan semua pesanan
        query = """
        SELECT p.id_pesanan, p.tanggal_pesanan, u.nama_pengguna, p.nama_produk, 
               p.status_pesanan, p.total_harga
        FROM pesanan p
        JOIN pengguna u ON p.id_pengguna = u.id_pengguna
        ORDER BY p.tanggal_pesanan DESC
        """
        cursor.execute(query)
        pesanan_list = cursor.fetchall()
        
        if pesanan_list:
            print("\n=== DAFTAR PESANAN ===\n")
            headers = ["ID", "Tanggal", "Pembeli", "Produk", "Status", "Total"]
            print(tabulate(pesanan_list, headers=headers, tablefmt="grid"))
            
            print("\n=== UBAH STATUS PESANAN ===")
            id_pesanan = input("\nMasukkan ID Pesanan (atau 0 untuk kembali): ")
            
            if id_pesanan == "0":
                clear_all()
                menu_admin(id_pengguna, nama_pengguna)
                return
            
            print("\nStatus yang tersedia:")
            print("1. menunggu_pembayaran")
            print("2. diproses")
            print("3. dikirim")
            print("4. selesai")
            print("5. dibatalkan")
            
            status_pilihan = input("\nPilih status baru (1-5): ")
            status_map = {
                "1": "menunggu_pembayaran",
                "2": "diproses",
                "3": "dikirim",
                "4": "selesai",
                "5": "dibatalkan"
            }
            
            if status_pilihan in status_map:
                new_status = status_map[status_pilihan]
                update_query = "UPDATE pesanan SET status_pesanan = %s WHERE id_pesanan = %s"
                cursor.execute(update_query, (new_status, id_pesanan))
                connection.commit()
                print(f"\n✅ Status pesanan berhasil diubah menjadi '{new_status}'")
            else:
                print("\n❌ Pilihan tidak valid!")
        else:
            print("\nBelum ada pesanan.")
        
        cursor.close()
        connection.close()
        input("\nTekan Enter...")
        clear_all()
        menu_admin(id_pengguna, nama_pengguna)
        
    except Error as error:
        print(f"\n❌ Error: {error}")
        if connection:
            connection.close()
        input("Tekan Enter...")
        clear_all()
        menu_admin(id_pengguna, nama_pengguna)

def admin_kelola_pasar(id_pengguna, nama_pengguna):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        
        print("\n=== KELOLA PASAR ===")
        print("1. Lihat Data Pasar")
        print("2. Tambah Data Pasar")
        print("3. Update Data Pasar")
        print("4. Hapus Data Pasar")
        
        pilihan = input("\nPilih (1-4): ")
        
        if pilihan == "1":
            query = "SELECT * FROM kelola_pasar WHERE is_delete = FALSE"
            cursor.execute(query)
            data = cursor.fetchall()
            
            if data:
                headers = ["ID", "Produk", "Harga Min", "Harga Max", "Harga Rata-rata", "Lokasi", "ID Pengguna"]
                print(tabulate(data, headers=headers, tablefmt="grid"))
            else:
                print("\nBelum ada data pasar.")
        
        elif pilihan == "2":
            nama_produk = input("Nama Produk: ")
            harga_min = input("Harga Minimum: ")
            harga_max = input("Harga Maximum: ")
            harga_rata = input("Harga Rata-rata: ")
            lokasi = input("Lokasi Pasar: ")
            
            query = """
            INSERT INTO kelola_pasar (nama_produk_pasar, harga_min_kelola_pasar, 
                                      harga_max_kelola_pasar, harga_rata_kelola_pasar, 
                                      lokasi_pasar, id_pengguna)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nama_produk, harga_min, harga_max, harga_rata, lokasi, id_pengguna))
            connection.commit()
            print("\n✅ Data pasar berhasil ditambahkan!")
        
        elif pilihan == "3":
            query = "SELECT * FROM kelola_pasar WHERE is_delete = FALSE"
            cursor.execute(query)
            data = cursor.fetchall()
            
            if data:
                headers = ["ID", "Produk", "Harga Min", "Harga Max", "Harga Rata-rata", "Lokasi", "ID Pengguna"]
                print(tabulate(data, headers=headers, tablefmt="grid"))
                
                id_pasar = input("\nMasukkan ID yang akan diupdate: ")
                harga_min = input("Harga Minimum baru: ")
                harga_max = input("Harga Maximum baru: ")
                harga_rata = input("Harga Rata-rata baru: ")
                
                query = """
                UPDATE kelola_pasar 
                SET harga_min_kelola_pasar = %s, harga_max_kelola_pasar = %s, 
                    harga_rata_kelola_pasar = %s
                WHERE id_kelola_pasar = %s
                """
                cursor.execute(query, (harga_min, harga_max, harga_rata, id_pasar))
                connection.commit()
                print("\n✅ Data pasar berhasil diupdate!")
            else:
                print("\nBelum ada data pasar.")
        
        elif pilihan == "4":
            query = "SELECT * FROM kelola_pasar WHERE is_delete = FALSE"
            cursor.execute(query)
            data = cursor.fetchall()
            
            if data:
                headers = ["ID", "Produk", "Harga Min", "Harga Max", "Harga Rata-rata", "Lokasi"]
                print(tabulate(data, headers=headers, tablefmt="grid"))
                
                id_pasar = input("\nMasukkan ID yang akan dihapus: ")
                query = "UPDATE kelola_pasar SET is_delete = TRUE WHERE id_kelola_pasar = %s"
                cursor.execute(query, (id_pasar,))
                connection.commit()
                print("\n✅ Data pasar berhasil dihapus!")
            else:
                print("\nBelum ada data pasar.")
        
        cursor.close()
        connection.close()
        input("\nTekan Enter...")
        clear_all()
        menu_admin(id_pengguna, nama_pengguna)
        
    except Error as error:
        print(f"\n❌ Error: {error}")
        if connection:
            connection.close()
        input("Tekan Enter...")
        clear_all()
        menu_admin(id_pengguna, nama_pengguna)

def admin_lihat_pengguna(id_pengguna, nama_pengguna):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        
        query = "SELECT id_pengguna, nama_pengguna, username_pengguna, role, no_telp_pengguna FROM pengguna"
        cursor.execute(query)
        users = cursor.fetchall()
        
        if users:
            print("\n=== DAFTAR PENGGUNA ===\n")
            headers = ["ID", "Nama", "Username", "Role", "No. Telp"]
            print(tabulate(users, headers=headers, tablefmt="grid"))
        else:
            print("\nBelum ada pengguna.")
        
        cursor.close()
        connection.close()
        input("\nTekan Enter...")
        clear_all()
        menu_admin(id_pengguna, nama_pengguna)
        
    except Error as error:
        print(f"\n❌ Error: {error}")
        if connection:
            connection.close()
        input("Tekan Enter...")
        clear_all()
        menu_admin(id_pengguna, nama_pengguna)

# ===========================
# MENU PEMBELI
# ===========================

def menu_pembeli(id_pengguna, nama_pengguna):
    print(f'''
=== MENU PEMBELI ===
Halo, {nama_pengguna}!

1. Tampilan Produk
2. Keranjang & Checkout
3. Cek Pesanan
4. Riwayat Pesanan
5. Logout
''')
    pilihan = input("Pilih Menu (1-5): ")
    
    if pilihan == "1":
        clear_all()
        pembeli_lihat_produk(id_pengguna, nama_pengguna)
    elif pilihan == "2":
        clear_all()
        pembeli_keranjang(id_pengguna, nama_pengguna)
    elif pilihan == "3":
        clear_all()
        pembeli_cek_pesanan(id_pengguna, nama_pengguna)
    elif pilihan == "4":
        clear_all()
        pembeli_riwayat_pesanan(id_pengguna, nama_pengguna)
    elif pilihan == "5":
        clear_all()
        print("Logout berhasil!")
        main_menu()
    else:
        print("Pilihan tidak valid!")
        input("Tekan Enter...")
        clear_all()
        menu_pembeli(id_pengguna, nama_pengguna)

# Simpan keranjang sementara di memori (bisa diganti dengan tabel database)
keranjang_global = {}

def pembeli_lihat_produk(id_pengguna, nama_pengguna):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT id_produk, nama_produk, harga_produk, stok_produk, kategori_produk
        FROM produk
        WHERE is_delete = FALSE AND stok_produk > 0
        """
        cursor.execute(query)
        produk_list = cursor.fetchall()
        
        if produk_list:
            print("\n=== DAFTAR PRODUK ===\n")
            headers = ["ID", "Nama Produk", "Harga", "Stok", "Kategori"]
            print(tabulate(produk_list, headers=headers, tablefmt="grid"))
            
            print("\n1. Tambah ke Keranjang")
            print("2. Kembali")
            pilihan = input("\nPilih (1/2): ")
            
            if pilihan == "1":
                id_produk = input("Masukkan ID Produk: ")
                jumlah = int(input("Jumlah: "))
                
                # Cek stok
                cursor.execute("SELECT stok_produk, harga_produk, nama_produk FROM produk WHERE id_produk = %s", (id_produk,))
                result = cursor.fetchone()
                
                if result and result[0] >= jumlah:
                    if id_pengguna not in keranjang_global:
                        keranjang_global[id_pengguna] = []
                    
                    keranjang_global[id_pengguna].append({
                        'id_produk': id_produk,
                        'nama_produk': result[2],
                        'harga': result[1],
                        'jumlah': jumlah
                    })
                    print(f"\n✅ {result[2]} berhasil ditambahkan ke keranjang!")
                else:
                    print("\n❌ Stok tidak cukup atau produk tidak ditemukan!")
        else:
            print("\nBelum ada produk tersedia.")
        
        cursor.close()
        connection.close()
        input("\nTekan Enter...")
        clear_all()
        menu_pembeli(id_pengguna, nama_pengguna)
        
    except Error as error:
        print(f"\n❌ Error: {error}")
        if connection:
            connection.close()
        input("Tekan Enter...")
        clear_all()
        menu_pembeli(id_pengguna, nama_pengguna)

def pembeli_keranjang(id_pengguna, nama_pengguna):
    if id_pengguna not in keranjang_global or not keranjang_global[id_pengguna]:
        print("\n🛒 Keranjang Anda kosong!")
        input("Tekan Enter...")
        clear_all()
        menu_pembeli(id_pengguna, nama_pengguna)
        return
    
    print("\n=== KERANJANG BELANJA ===\n")
    keranjang = keranjang_global[id_pengguna]
    total = 0
    
    for idx, item in enumerate(keranjang, 1):
        subtotal = item['harga'] * item['jumlah']
        total += subtotal
        print(f"{idx}. {item['nama_produk']} - Rp{item['harga']:,} x {item['jumlah']} = Rp{subtotal:,}")
    
    print(f"\nTotal: Rp{total:,}")
    
    print("\n1. Checkout")
    print("2. Hapus Item")
    print("3. Kembali")
    
    pilihan = input("\nPilih (1-3): ")
    
    if pilihan == "1":
        connection = connect_db()
        if connection is None:
            return
        
        try:
            cursor = connection.cursor()
            
            metode_bayar = input("Metode Pembayaran (COD/Transfer): ")
            
            for item in keranjang:
                # Insert pesanan
                query = """
                INSERT INTO pesanan (tanggal_pesanan, nama_produk, status_pesanan, 
                                   metode_pembayaran, total_harga, id_pengguna)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_pesanan
                """
                cursor.execute(query, (
                    datetime.now().date(),
                    item['nama_produk'],
                    'menunggu_pembayaran',
                    metode_bayar,
                    item['harga'] * item['jumlah'],
                    id_pengguna
                ))
                id_pesanan = cursor.fetchone()[0]
                
                # Insert detail pesanan
                detail_query = """
                INSERT INTO detail_pesanan (jumlah_pesanan, subtotal, id_pesanan, id_produk)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(detail_query, (
                    item['jumlah'],
                    item['harga'] * item['jumlah'],
                    id_pesanan,
                    item['id_produk']
                ))
                
                # Update stok
                cursor.execute(
                    "UPDATE produk SET stok_produk = stok_produk - %s WHERE id_produk = %s",
                    (item['jumlah'], item['id_produk'])
                )
            
            connection.commit()
            keranjang_global[id_pengguna] = []
            
            print("\n✅ Checkout berhasil! Pesanan Anda sedang diproses.")
            
            cursor.close()
            connection.close()
            
        except Error as error:
            print(f"\n❌ Error: {error}")
            if connection:
                connection.rollback()
                connection.close()
    
    elif pilihan == "2":
        idx = int(input("Nomor item yang akan dihapus: ")) - 1
        if 0 <= idx < len(keranjang):
            removed = keranjang.pop(idx)
            print(f"\n✅ {removed['nama_produk']} dihapus dari keranjang!")
        else:
            print("\n❌ Nomor tidak valid!")
    
    input("\nTekan Enter...")
    clear_all()
    menu_pembeli(id_pengguna, nama_pengguna)

def pembeli_cek_pesanan(id_pengguna, nama_pengguna):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT id_pesanan, tanggal_pesanan, nama_produk, status_pesanan, total_harga
        FROM pesanan
        WHERE id_pengguna = %s AND status_pesanan != 'selesai' AND status_pesanan != 'dibatalkan'
        ORDER BY tanggal_pesanan DESC
        """
        cursor.execute(query, (id_pengguna,))
        pesanan = cursor.fetchall()
        
        if pesanan:
            print("\n=== PESANAN AKTIF ===\n")
            headers = ["ID", "Tanggal", "Produk", "Status", "Total"]
            print(tabulate(pesanan, headers=headers, tablefmt="grid"))
        else:
            print("\nTidak ada pesanan aktif.")
        
        cursor.close()
        connection.close()
        input("\nTekan Enter...")
        clear_all()
        menu_pembeli(id_pengguna, nama_pengguna)
        
    except Error as error:
        print(f"\n❌ Error: {error}")
        if connection:
            connection.close()
        input("Tekan Enter...")
        clear_all()
        menu_pembeli(id_pengguna, nama_pengguna)

def pembeli_riwayat_pesanan(id_pengguna, nama_pengguna):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT id_pesanan, tanggal_pesanan, nama_produk, status_pesanan, total_harga
        FROM pesanan
        WHERE id_pengguna = %s
        ORDER BY tanggal_pesanan DESC
        """
        cursor.execute(query, (id_pengguna,))
        riwayat = cursor.fetchall()
        
        if riwayat:
            print("\n=== RIWAYAT PESANAN ===\n")
            headers = ["ID", "Tanggal", "Produk", "Status", "Total"]
            print(tabulate(riwayat, headers=headers, tablefmt="grid"))
        else:
            print("\nBelum ada riwayat pesanan.")
        
        cursor.close()
        connection.close()
        input("\nTekan Enter...")
        clear_all()
        menu_pembeli(id_pengguna, nama_pengguna)
        
    except Error as error:
        print(f"\n❌ Error: {error}")
        if connection:
            connection.close()
        input("Tekan Enter...")
        clear_all()
        menu_pembeli(id_pengguna, nama_pengguna)

# ===========================
# MENU PENJUAL (PETANI)
# ===========================

def menu_penjual(id_pengguna, nama_pengguna):
    print('''
=== MENU PENJUAL ===

1. Kelola Produk
2. Lihat Riwayat Penjualan
3. Lihat harga Pasar
4. Logout
''')
    pilihan = input("Pilih Menu(1-4): ")
    if pilihan == "1":
        clear_all()
        penjual_kelola_produk(id_pengguna, nama_pengguna)
    elif pilihan == "2":
        clear_all()
        penjual_riwayat_penjualan(id_pengguna, nama_pengguna)
    elif pilihan == "3":
        clear_all()
        penjual_lihat_pasar(id_pengguna, nama_pengguna)
    elif pilihan == "4":
        clear_all()
        print("Logout berhasil")
        main_menu()
    else:
        print("Pilihan tidak valid")
        input("Tekan enter untuk kembali ke menu penjual: ")
        clear_all()
        menu_penjual(id_pengguna, nama_pengguna)


def penjual_kelola_produk(id_pengguna, nama_pengguna):
    clear_all
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        print('''
    === KELOLA PRODUK ===

     1. Lihat Produk
     2. Tambah Produk 
     3. Update Produk
     4. Hapus Produk
    ''')
        
        pilihan = input("Pilih(1-4): ")
        if pilihan == "1":
            query = """
            SELECT 
                p.id_produk, 
                p.nama_produk, 
                p.stok_produk, 
                p.harga_produk, 
                k.jenis_produk, 
                k.deskripsi_produk 
            FROM
                produk p
            JOIN kategori_produk k ON p.id_kategori_produk = k.id_kategori_produk
            WHERE is_delete = FALSE AND stok_produk > 0
            """
        
            cursor.execute(query)
            produk = cursor.fetchall()
            
            if produk:
                print("=== PRODUK ENTROPIN ===")
                headers = ["ID", "NAMA PRODUK", "STOK", "HARGA", "KATEGORI", "DESKRIPSI"]
                print(tabulate(produk, headers=headers, tablefmt="grid"))
            else:
                print("\nBelum ada produk.")
        
        elif pilihan == "2":
            nama = input("Nama Produk: ")
            harga = input("Harga Produk: ")
            stok = input("Stok Produk: ")
            kategori = input("Kategori Produk: ")
            
            query = """
            INSERT INTO produk (nama_produk, harga_produk, stok_produk, kategori_produk)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (nama, harga, stok, kategori))
            connection.commit()
            print("Produk berhasil ditambahkan")
        
        elif pilihan == "3":
            query = "SELECT id_produk, nama_produk, harga_produk, stok_produk FROM produk WHERE is_delete = FALSE"
            cursor.execute(query)
            produk = cursor.fetchall()
            
            if produk:
                header = ["ID", "Nama", "Harga", "Stok", "Kategori", "ID Penjual"]
                print(tabulate(produk, headers=header, tablefmt="grid"))
                
                id_produk = input("ID Produk yang akan diupdate: ")
                harga = input("Harga baru: ")
                stok = input("Stok baru: ")
                
                query = "UPDATE produk SET harga_produk = %s, stok_produk = %s WHERE id_produk = %s"
                cursor.execute(query, (harga, stok, id_produk))
                connection.commit()
                print("Update produk berhasil")
            else:
                print("Belum ada produk")
        
        elif pilihan == "4":
            query = "SELECT id_produk, nama_produk, harga_produk, stok_produk FROM produk WHERE is_delete = FALSE"
            cursor.execute(query)
            produk = cursor.fetchall()
            
            if produk:
                headers = ["ID", "Nama", "Harga", "Stok", ]
                print(tabulate(produk, headers=headers, tablefmt="grid"))
                
                id_produk = input("\nID Produk yang akan dihapus: ")
                query = "UPDATE produk SET is_delete = TRUE WHERE id_produk = %s"
                cursor.execute(query, (id_produk,))
                connection.commit()
                print(" Produk berhasil dihapus")
            else:
                print("Belum ada produk")
        
        cursor.close()
        connection.close()
        input("Tekan enter untuk kembali ke menu penjual: ")
        clear_all()
        menu_penjual(id_pengguna, nama_pengguna)
        
    except Error as error:
        print(f"Error: {error}")
        if connection:
            connection.close()
        input("Tekan enter untuk kembali ke menu penjual: ")
        clear_all()
        menu_penjual(id_pengguna, nama_pengguna)

def penjual_riwayat_penjualan(id_pengguna, nama_pengguna):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        query = """
        SELECT p.id_pesanan, p.tanggal_pesanan, u.nama_pengguna AS pembeli, 
               p.nama_produk, dp.jumlah_pesanan, p.total_harga, p.status_pesanan
        FROM pesanan p
        JOIN detail_pesanan dp ON p.id_pesanan = dp.id_pesanan
        JOIN produk pr ON dp.id_produk = pr.id_produk
        JOIN pengguna u ON p.id_pengguna = u.id_pengguna
        ORDER BY p.tanggal_pesanan DESC
        """
        cursor.execute(query)
        riwayat = cursor.fetchall()
        
        if riwayat:
            print("=== RIWAYAT PENJUALAN ===")
            headers = ["ID Pesanan", "Tanggal", "Pembeli", "Produk", "Jumlah", "Total", "Status"]
            print(tabulate(riwayat, headers=headers, tablefmt="grid"))
            
            total_penjualan = sum(row[5] for row in riwayat if row[6] == 'selesai')
            print(f"Total Penjualan (Selesai): Rp{total_penjualan:,}")
        else:
            print("Belum ada riwayat penjualan")
        
        cursor.close()
        connection.close()
        input("Tekan enter untuk kembali ke menu penjual: ")
        clear_all()
        menu_penjual(id_pengguna, nama_pengguna)
        
    except Error as error:
        print(f"Error: {error}")
        if connection:
            connection.close()
        input("Tekan enter untuk kembali ke menu penjual: ")
        clear_all()
        menu_penjual(id_pengguna, nama_pengguna)

def penjual_lihat_pasar(id_pengguna, nama_pengguna):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT nama_produk_pasar, harga_min_kelola_pasar, harga_max_kelola_pasar, 
               harga_rata_kelola_pasar, lokasi_pasar
        FROM kelola_pasar
        WHERE is_delete = FALSE
        ORDER BY nama_produk_pasar
        """
        cursor.execute(query)
        data_pasar = cursor.fetchall()
        if data_pasar:
            print("\n=== DAFTAR HARGA PASAR ===\n")
            headers = ["Produk", "Harga Min", "Harga Max", "Harga Rata-rata", "Lokasi"]
            print(tabulate(data_pasar, headers=headers, tablefmt="grid"))
            print("Gunakan data ini sebagai referensi harga jual produk Anda!")
        else:
            print("Belum ada data harga pasar")
        
        cursor.close()
        connection.close()
        input("Tekan enter untuk kembali ke menu penjual: ")
        clear_all()
        menu_penjual(id_pengguna, nama_pengguna)
        
    except Error as error:
        print(f"Error: {error}")
        if connection:
            connection.close()
        input("Tekan enter untuk kembali ke menu penjual: ")
        clear_all()
        menu_penjual(id_pengguna, nama_pengguna)

# ===========================
# JALANKAN PROGRAM
# ===========================
input("Tekan Enter untuk melanjutkan...")
clear_all()
main_menu()