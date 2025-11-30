import psycopg2
from psycopg2 import Error
from tabulate import tabulate
import os
from datetime import date


def connect_db():
    try:
        connection = psycopg2.connect(
            user = "postgres",
            password = "sabila.19",
            host = "127.0.0.1",
            port = "5432",
            database = "entropin end game"
        )
        return connection
    except Error as error:
        print("Terjadi kesalahan, gagal terkoneksi dengan database", error)

def clear_all():
    os.system('cls')

def next():
    lanjut = input("Silahkan Tekan Enter Untuk Lanjut")
    print(lanjut)
    if lanjut == '':
        clear_all()
    return

def back():
    kembali = input("Silahkan Tekan Enter Untuk Kembali")
    print(kembali)
    if kembali == '':
        clear_all()
    return


def main_menu():
    print(r"""                                                       
 __  __                    _   _ _                        
|  \/  | ___ _ __  _   _  | | | | |_ __ _ _ __ ___   __ _ 
| |\/| |/ _ \ '_ \| | | | | | | | __/ _` | '_ ` _ \ / _` |
| |  | |  __/ | | | |_| | | |_| | || (_| | | | | | | (_| |
|_|  |_|\___|_| |_|\__,_|  \___/ \__\__,_|_| |_| |_|\__,_|
    
1. Register
2. Login
3. Logout Sistem
    """)

    select_menu = input("Pilih Main Menu (1-3) : ")
    if select_menu == "1":
        clear_all()
        register()
    elif select_menu == "2":
        clear_all()
        login()
    elif select_menu == "3":
        clear_all()
        return
    else :
        print("Pilihan Tidak Ditemukan")
        clear_all()
        main_menu()
        

def register():
    print('''=== Silahkan memilih tipe pelaku ===
        1. Penjual
        2. Pembeli
        3. Kembali ke Main Menu
''')
    tipe_pelaku = input("Pilih (1-3) : ")
    while True :
        if tipe_pelaku == "1":
            clear_all()
            register_penjual()
        elif tipe_pelaku == "2":
            clear_all()
            register_pembeli()
        elif tipe_pelaku == "3":
            clear_all()
            main_menu()
        else:
            print("Pilihan tidak tersedia")
            register()
        return

def register_penjual():
    clear_all()
    connection = connect_db()
    if connection is None:
        print("Koneksi tidak berhasil")
        return
    
    try:
        cursor = connection.cursor()
        
        print("=== REGISTER PENJUAL ===\n")
        print("Ketik 'exit' Untuk kembali ke Main Menu\n")
        
        while True:
            nama = input('Nama Lengkap : ').strip()
            if nama == '':
                print('\nNama tidak boleh kosong')
                next()
                continue
            if nama.isdigit():
                print('\nNama tidak boleh angka')
                next()
                continue
            elif nama == "exit":
                input("\nTekan enter untuk kembali ke menu awal")
                next()
                cursor.close()
                connection.close()
                return main_menu()
            else:
                next()
                break
        while True:
            print(''' ===== DATA NAMA JALAN =====
                1. jalan kalimantan
                2. jalan lumba-lumba
                3. jalan sudirman
                4. jalan gajah mada
                4. jalan sumatra
                5. jalan tidar
                6. jalan mastrip
                7. jalan jawa
                8. jalan brawijaya
                9. jalan P.B soedirman
                10. jalan karimata
                11. jalan kaliurang
                12. jalan kertanegara
                13. jalan prabuwangi
                ''')
            jalan = input('Nama Jalan(ct. jalan jawa) : ').strip()
            if jalan == '':
                print('\nNama jalan tidak boleh kosong')
                next()
                continue
            elif jalan == "exit":
                input("\nTekan enter untuk kembali ke menu awal")
                next()
                cursor.close()
                connection.close()
                return main_menu()
            
            cursor.execute("SELECT id_jalan FROM jalan WHERE nama_jalan = %s", (jalan,))
            data_jalan = cursor.fetchone()
            if data_jalan is None:
                print('\nNama jalan tidak ditemukan. Harap masukkan nama jalan sesuai data')
                next()
                continue
            elif data_jalan is not None:
                id_jalan = data_jalan[0]
                next()
                break
        while True:
            nomor_telepon = input('Nomor Telepon : ').strip()
            if nomor_telepon == '':
                print('\nNomor telepon tidak boleh kosong')
                next()
                continue
            elif nomor_telepon == "exit":
                input("\nTekan enter untuk kembali ke menu awal")
                next()
                cursor.close()
                connection.close()
                return main_menu()
            elif not nomor_telepon.isdigit():
                print('\nNomor telepon harus angka')
                next()
                continue
            elif len(nomor_telepon) < 10 or len(nomor_telepon) > 12:
                print('\nNomor telepon tidak boleh kurang dari 10 atau lebih dari 12')
                next()
                continue 
            else:
                next()
                break
        while True:
            username = input('Username (5-15 karakter) : ').strip()
            if username == '':
                print('\nUsername tidak boleh kosong')
                next()
                continue
            elif username == "exit":
                input("\nTekan enter untuk kembali ke menu awal")
                next()
                cursor.close()
                connection.close()
                return main_menu()
            elif len(username) < 5:
                print('\nUsername terlalu pendek')
                next()
                continue
            elif len(username) > 15:
                print('\nUsername terlalu panjang')
                next()
                continue
            check_query = '''SELECT username_pengguna
                            FROM pengguna 
                            WHERE username_pengguna = %s'''
            cursor.execute(check_query, (username,))
            check_user = cursor.fetchone()
                
            if check_user:
                print("\nUsername sudah digunakan! Silahkan gunakan username lain.")
                next()
                continue
            else:
                next()
                break
        while True:
            password = input('Password (5-15 karakter) : ').strip()
            if password == '':
                print('\nPassword tidak boleh kosong')
                continue
            elif password == "exit":
                input("\nTekan enter untuk kembali ke menu awal")
                next()
                cursor.close()
                connection.close()
                return main_menu()
            elif len(password) < 5:
                print('\nPassword terlalu pendek')
                continue
            elif len(password) > 15:
                print('\nPassword terlalu panjang')
                continue
            check_query = '''SELECT password_pengguna
                            FROM pengguna 
                            WHERE password_pengguna = %s'''
            cursor.execute(check_query, (password,))
            check_pw = cursor.fetchone()

            if check_pw:
                print("\nPassword sudah digunakan! Silahkan gunakan password lain.")
                next()
                continue
            else:
                next()
                break
        role = "penjual" 
        
        insert_query = """
        INSERT INTO pengguna (nama_pengguna, no_telp_pengguna, username_pengguna, password_pengguna, role, id_jalan)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (nama, nomor_telepon, username, password, role, id_jalan))
        connection.commit()

        print("\nRegistrasi Penjual Berhasil!")
        print(f"Selamat datang, {nama}!")
        
        input("\nTekan Enter untuk kembali ke Main Menu...")
        cursor.close()
        connection.close()
        clear_all()
        main_menu()
        return
        
    except Error as error:
        print(f"\nTerjadi kesalahan saat registrasi: {error}")
        input("Tekan Enter untuk melanjutkan...")
        if connection:
            connection.close()
        clear_all()
        register_penjual()
        return

def register_pembeli():
    clear_all()
    connection = connect_db()
    if connection is None:
        print("Koneksi tidak berhasil")
        return
    
    try:
        cursor = connection.cursor()
        
        print("=== REGISTER PEMBELI ===\n")
        print("Ketik 'exit' Untuk kembali ke Main Menu\n")

        while True:
            nama = input('Nama Lengkap : ').strip()
            if nama == '':
                print('\nNama tidak boleh kosong')
                next()
                continue
            if nama.isdigit():
                print('\nNama tidak boleh angka')
                next()
                continue
            elif nama == "exit":
                input("\nTekan enter untuk kembali ke menu awal")
                next()
                cursor.close()
                connection.close()
                return main_menu()
            else:
                next()
                break
        while True:
            print(''' ===== DATA NAMA JALAN =====
                1. jalan kalimantan
                2. jalan lumba-lumba
                3. jalan sudirman
                4. jalan gajah mada
                5. jalan sumatra
                6. jalan tidar
                7. jalan mastrip
                8. jalan jawa
                9. jalan brawijaya
                10. jalan P.B soedirman
                11. jalan karimata
                12. jalan kaliurang
                13. jalan kertanegara
                14. jalan prabuwangi
                ''')
            jalan = input('Nama Jalan(ct. jalan jawa) : ').strip()
            if jalan == '':
                print('\nNama jalan tidak boleh kosong')
                next()
                continue
            elif jalan == "exit":
                input("\nTekan enter untuk kembali ke menu awal")
                clear_all()
                cursor.close()
                connection.close()
                return main_menu()
            
            cursor.execute("SELECT id_jalan FROM jalan WHERE nama_jalan = %s", (jalan,))
            data_jalan = cursor.fetchone()
            if data_jalan is None:
                print('\nNama jalan tidak ditemukan. Harap masukkan nama jalan sesuai data')
                next()
                continue
            elif data_jalan is not None:
                id_jalan = data_jalan[0]
                next()
                break
            else:
                next()
                break
        while True:
            nomor_telepon = input('Nomor Telepon : ').strip()
            if nomor_telepon == '':
                print('\nNomor telepon tidak boleh kosong')
                next()
                continue
            elif nomor_telepon == "exit":
                input("\nTekan enter untuk kembali ke menu awal")
                clear_all()
                cursor.close()
                connection.close()
                return main_menu()
            elif not nomor_telepon.isdigit():
                print('\nNomor telepon harus angka')
                next()
                continue
            elif len(nomor_telepon) < 10 or len(nomor_telepon) > 12:
                print('\nNomor telepon tidak boleh kurang dari 10 atau lebih dari 12')
                next()
                continue 
            else:
                next()
                break
        while True:
            username = input('Username (5-15 karakter) : ').strip()
            if username == '':
                print('\nUsername tidak boleh kosong')
                next()
                continue
            elif username == "exit":
                input("\nTekan enter untuk kembali ke menu awal")
                clear_all()
                cursor.close()
                connection.close()
                return main_menu()
            elif len(username) < 5:
                print('\nUsername terlalu pendek')
                next()
                continue
            elif len(username) > 15:
                print('\nUsername terlalu panjang')
                next()
                continue
            check_query = '''SELECT username_pengguna
                            FROM pengguna 
                            WHERE username_pengguna = %s'''
            cursor.execute(check_query, (username,))
            check_user = cursor.fetchone()
                
            if check_user:
                print("\nUsername sudah digunakan! Silahkan gunakan username lain.")
                next()
                continue
            else:
                next()
                break
        while True:
            password = input('Password (5-15 karakter) : ').strip()
            if password == '':
                print('\nPassword tidak boleh kosong')
                continue
            elif password == "exit":
                input("\nTekan enter untuk kembali ke menu awal")
                clear_all()
                cursor.close()
                connection.close()
                return main_menu()
            elif len(password) < 5:
                print('\nPassword terlalu pendek')
                continue
            elif len(password) > 15:
                print('\nPassword terlalu panjang')
                continue
            check_query = '''SELECT password_pengguna
                            FROM pengguna 
                            WHERE password_pengguna = %s'''
            cursor.execute(check_query, (password,))
            check_pw = cursor.fetchone()

            if check_pw:
                print("\nPassword sudah digunakan! Silahkan gunakan password lain.")
                next()
                continue
            else:
                next()
                break
        role = "pembeli" 
        
        insert_query = """
        INSERT INTO pengguna (nama_pengguna, no_telp_pengguna, username_pengguna, password_pengguna, role, id_jalan)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (nama, nomor_telepon, username, password, role, id_jalan))
        connection.commit()
        
        print("\nRegistrasi Pembeli Berhasil!")
        print(f"Selamat datang, {nama}!")
        
        input("\nTekan Enter untuk kembali ke Main Menu...")
        cursor.close()
        connection.close()
        clear_all()
        main_menu()
        return
        
    except Error as error:
        print(f"\nTerjadi kesalahan saat registrasi: {error}")
        input("Tekan Enter untuk melanjutkan...")
        if connection:
            connection.close()
        clear_all()
        register_pembeli()
        return
    
def login():
    clear_all()
    connection = connect_db()
    if connection is None:
        print("Koneksi tidak berhasil")
        return
    
    try:
        cursor = connection.cursor()

        print("=== LOGIN SISTEM ===\n")
        print("Ketik 0 Untuk kembali ke Main Menu\n")

        while True:
            username = input("Masukkan Username : ")
            if username == "0":
                input("\nTekan enter untuk kembali ke menu awal")
                clear_all()
                cursor.close()
                connection.close()
                return main_menu()
            else:
                break
        while True:
            password = input("Masukkan Password : ")
            if password == "0":
                input("\nTekan enter untuk kembali ke menu awal")
                clear_all()
                cursor.close()
                connection.close()
                return main_menu()
            else:
                break

        check_query = """
        SELECT id_pengguna, nama_pengguna, role 
        FROM pengguna 
        WHERE username_pengguna = %s AND password_pengguna = %s
        """
        cursor.execute(check_query, (username, password))
        check_user = cursor.fetchone()
        
        if check_user:
            id_pengguna = check_user[0]
            nama_pengguna = check_user[1]
            role = check_user[2]
            print(f"\nLogin Berhasil!")
            print(f"Selamat datang {nama_pengguna}")
            print(f"Sebagai {role}")

            next()
            cursor.close()
            connection.close()
            clear_all()

            if role == "admin":
                menu_admin(id_pengguna, username)
            elif role == "penjual":
                menu_penjual(id_pengguna, username)
            elif role == "pembeli":
                menu_pembeli(id_pengguna, username)
            else:
                print("Role tidak dikenali!")
                login()
                return
        else:
            clear_all()
            print("\nUsername atau Password salah!")
            input("Tekan Enter untuk mencoba lagi...")
            cursor.close()
            connection.close()
            clear_all()
            login()
            return
            
    except Error as error:
        print(f"\nTerjadi kesalahan saat login: {error}")
        input("Tekan Enter untuk melanjutkan...")
        if connection:
            connection.close()
        clear_all()
        login()
        return

def menu_pembeli(id_pengguna, username):
    clear_all()
    print(f'''
 __  __                    ____                _          _ _ 
|  \/  | ___ _ __  _   _  |  _ \ ___ _ __ ___ | |__   ___| (_)
| |\/| |/ _ \ '_ \| | | | | |_) / _ \ '_ ` _ \| '_ \ / _ \ | |
| |  | |  __/ | | | |_| | |  __/  __/ | | | | | |_) |  __/ | |
|_|  |_|\___|_| |_|\__,_| |_|   \___|_| |_| |_|_.__/ \___|_|_|

Selamat Datang {username} Di Entropin!

1. Daftar Produk Entropin
2. Keranjang dan Checkout
3. Cek Pesanan
4. Riwayat Pesanan
5. Logout
''')
    pilih = input("Pilih Menu (1-5): ")
    
    if pilih == '1':
        clear_all()
        buyproduk_entropin(id_pengguna, username)
    elif pilih == '2':
        clear_all()
        keranjang_pembeli(id_pengguna, username)
    elif pilih == '3':
        clear_all()
        pembeli_cek_pesanan(id_pengguna, username)
    elif pilih == '4':
        clear_all()
        pembeli_riwayat_pesanan(id_pengguna, username)
    elif pilih == '5':
        clear_all()
        main_menu()
        return
    else:
        print('''
            Pilihan Tidak Valid
            Tekan Enter Untuk Kembali Ke Menu''')
        clear_all()
        menu_pembeli(id_pengguna, username)
        return
    
keranjang_entropin = {}

def buyproduk_entropin(id_pengguna, username):
    clear_all()
    connection = connect_db()
    if connection is None:
        print("Koneksi tidak berhasil")
        return
    
    try:
        cursor = connection.cursor()

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
        ORDER BY k.jenis_produk
        """
        cursor.execute(query)
        list_produk = cursor.fetchall()

        if list_produk:
            clear_all()
            print("\n===== PRODUK ENTROPIN =====\n")
            headers = ['ID', 'NAMA PRODUK', 'STOK', 'HARGA', 'KATEGORI', 'DESKRIPSI']
            print(tabulate(list_produk, headers=headers, tablefmt='fancy_grid'))
            
            print('''\n
            1. Tambah Ke Keranjang
            2. Kembali
                ''')
            pilih = input("Pilih (1/2): ")
            if pilih == '1':
                while True:
                    id_produk = input('\nMasukkan ID Produk (0 untuk selesai): ').strip()
                    if id_produk == '':
                        print('\nID tidak boleh dikosongi')
                        next()
                        continue
                    elif id_produk == 0 :
                        input('\nTekan Enter Untuk Kembali Ke Menu Pembeli')
                        clear_all()
                        menu_pembeli(id_pengguna, username)
                        return
                    elif not id_produk.isdigit():
                        print('\nID Produk harus berupa angka')
                        next()
                        continue
                    else:
                        break
                while True:
                    jumlah_item = int(input('Masukkan Jumlah Yang Ingin Dibeli: '))
                    if jumlah_item == '':
                        print('\nJumlah Item tidak boleh dikosongi')
                        next()
                        continue
                    else:
                        break
                    
                cursor.execute("""SELECT nama_produk, harga_produk, stok_produk
                                FROM produk
                                WHERE id_produk = %s AND is_delete = FALSE
                                """, (id_produk,))
                hasil = cursor.fetchone()

                if hasil and hasil[2] >= jumlah_item:
                    if id_pengguna not in keranjang_entropin:
                        keranjang_entropin[id_pengguna] = []
                            
                    keranjang_entropin[id_pengguna].append({
                        'id_produk' : id_produk,
                        'nama_produk' : hasil[0],
                        'harga_produk' : hasil[1],
                        'jumlah_item' : jumlah_item
                        })
                    print(f"\n {hasil[0]} berhasil ditambahkan")
                    next()
                    buyproduk_entropin(id_pengguna, username)
                    return
                else: 
                    print("\nStok Tidak Cukup atau Produk Tidak Ada")
                    next()
            elif pilih == '2':
                cursor.close()
                connection.close()
                clear_all()
                menu_pembeli(id_pengguna, username) 
                return    
            else:
                print('Menu Yang Dipilih Tidak Tersedia')
                next()
                clear_all()
                buyproduk_entropin(id_pengguna, username)
                return

    except Error as error:
        print(f"\nTerjadi kesalahan saat membeli produk: {error}")
        input("Tekan Enter untuk melanjutkan...")
        if connection:
            connection.close()
        clear_all()
        buyproduk_entropin(id_pengguna, username)
        return

def keranjang_pembeli(id_pengguna, username):
    clear_all()
    connection = connect_db()
    if connection is None:
        return
        
    try: 
        cursor = connection.cursor()

        if id_pengguna not in keranjang_entropin or not keranjang_entropin[id_pengguna]:
            print("Keranjang Anda Kosong")
            input("Tekan Enter Untuk Kembali")
            menu_pembeli(id_pengguna, username)
            return
            
        print("\n===== Keranjang Belanja =====\n")
        keranjang = keranjang_entropin[id_pengguna]
        total = 0

        i = 1
        for item in keranjang:
            subtotal = item['harga_produk'] * item['jumlah_item']
            total += subtotal

            print(f''''
            {i}. {item['nama_produk']}
            Rp {item['harga_produk']} x {item['jumlah_item']} = Rp{subtotal}
            ''')
            i += 1

        print(f"\nTotal : Rp{total}")
            
        print('''\n
        1. Checkout
        2. Hapus Item
        3. Tambah Item
        4. Kembali
        ''')
        pilih = input("\nPilih (1-4): ")

        if pilih == '1':
            clear_all()
            while True:
                print('''Daftar Nama Bank
                1. BCA
                2. BRI
                3. MANDIRI
                4. BNI
                ''')
                metode_pembayaran = input("\nMetode Pembayaran (Nama Bank): ").strip()
                if metode_pembayaran == '':
                    print('\nSilahkan masukkan nama bank')
                    next()
                    continue
                elif metode_pembayaran not in ['BCA', 'BRI', 'MANDIRI', 'BNI']:
                    print('\nMetode pembayaran tidak valid. Pilih: BCA, BRI, MANDIRI, atau BNI')
                    next()
                    continue
                else:
                    next()
                    break
            while True:
                bayar = input('\nApakah anda ingin membayar sekarang (iya/tidak)? ').strip().lower()
                if bayar == '':
                    print('\nTidak boleh diisi kosong')
                    next()
                    continue
                elif bayar not in ['iya', 'tidak']:
                    print('\nPilihan tidak valid. Ketik "iya" atau "tidak"')
                    next()
                    continue
                else:
                    break

            if bayar == 'iya':
                status_pesanan = 'diproses'
            else:
                status_pesanan = 'menunggu pembayaran'

            for item in keranjang:
                insert_pesanan = """
                INSERT INTO pesanan (tanggal_pesanan, 
                                    status_pesanan,
                                    metode_pembayaran,
                                    id_pengguna)
                VALUES (%s, %s, %s, %s)
                RETURNING id_pesanan
                """
                cursor.execute(insert_pesanan, (date.today(),
                                                status_pesanan,
                                                metode_pembayaran,
                                                id_pengguna
                                ))
                id_pesanan = cursor.fetchone()[0]

                # insert ke detail pesanan
                insert_detail = """
                INSERT INTO detail_pesanan(jumlah_pesanan, 
                                            id_pesanan,
                                            id_produk)
                VALUES (%s, %s, %s)
                """
                cursor.execute(insert_detail, (item['jumlah_item'],
                                                id_pesanan,
                                                item['id_produk']
                                    ))
                
                # insert ke laporan
                insert_laporan = """
                INSERT INTO laporan (tanggal_laporan, 
                                    status_akhir,
                                    id_pesanan)
                VALUES(%s, %s, %s)
                """
                cursor.execute(insert_laporan, (date.today(),
                                                status_pesanan,
                                                id_pesanan
                                    ))

                cursor.execute("""UPDATE produk 
                                    SET stok_produk = stok_produk - %s
                                    WHERE id_produk = %s""",
                                    (item['jumlah_item'], item['id_produk']))
                connection.commit()

            keranjang_entropin[id_pengguna] = []
            
            if bayar == 'iya':
                print(f'\nPesanan {username} sedang diproses')
            else:
                print(f'\nPesanan {username} disimpan. Status: Menunggu Pembayaran')
            
            back()
            menu_pembeli(id_pengguna, username)
            return
        elif pilih == '2':
            while True:
                hapus_produk = input('Nomor Produk yang ingin dihapus : ').strip()
                hapus_produk_fix = hapus_produk - 1
                if hapus_produk == '':
                    print('\nTidak boleh kosong')
                    next()
                    continue
                elif not hapus_produk.isdigit():
                    print('\nNomor harus berupa angka')
                    next()
                    continue
                elif hapus_produk_fix >= 0 and hapus_produk_fix < len(keranjang):
                    hapus = keranjang.pop(hapus_produk_fix)
                    print(f'\n{hapus['nama_produk']} dihapus dari keranjang')
                    next()
                    menu_pembeli(id_pengguna, username)
                else:
                    print('\nNomor tidak valid')
        elif pilih == '3':
            clear_all()
            buyproduk_entropin(id_pengguna, username)
        elif pilih == '4':
            clear_all()
            menu_pembeli(id_pengguna, username)
        else:
            print('\nPilihan tidak tersedia')
            next()
            cursor.close()
            connection.close()
            clear_all()
            keranjang_pembeli(id_pengguna, username)
            return
            
    except Error as error:
        print(f"\nTerjadi kesalahan saat membeli produk: {error}")
        input("Tekan Enter untuk melanjutkan...")
        if connection:
            connection.close()
        clear_all()
        keranjang_pembeli(id_pengguna, username)
        return

def pembeli_cek_pesanan(id_pengguna, username):
    clear_all()
    connection = connect_db()
    if connection is None:
        return
        
    try: 
        cursor = connection.cursor()

        cek_pesanan = """SELECT p.id_pesanan,
                                p.tanggal_pesanan,
                                pr.nama_produk,
                                dp.jumlah_pesanan,
                                p.status_pesanan,
                                p.metode_pembayaran,
                                CONCAT(j.nama_jalan, ', ', d.nama_desa, ', ', k.nama_kecamatan, ', ', kb.nama_kabupaten) AS alamat
                        FROM pesanan p
                        JOIN detail_pesanan dp ON p.id_pesanan = dp.id_pesanan
                        JOIN produk pr ON dp.id_produk = pr.id_produk
                        JOIN pengguna pg ON pr.id_pengguna = pg.id_pengguna
                        JOIN jalan j ON pg.id_jalan = j.id_jalan
                        JOIN desa d ON j.id_desa = d.id_desa
                        JOIN kecamatan k ON d.id_kecamatan = k.id_kecamatan
                        JOIN kabupaten kb ON k.id_kabupaten = kb.id_kabupaten
                        WHERE p.id_pengguna = %s
                            AND p.status_pesanan IN ('diproses','dikirim','menunggu pembayaran')
                        ORDER BY p.tanggal_pesanan DESC"""
        cursor.execute(cek_pesanan, (id_pengguna,))
        pesanan = cursor.fetchall()
        
        if pesanan:
            print(f'\n===== DATA PESANAN {username} =====\n')
            headers = ['ID', 'Tgl Pesanan', 'Nama Produk', 'Banyak Produk', 'Status', 'Metode Bayar', 'Alamat']
            print(tabulate(pesanan, headers=headers, tablefmt='fancy_grid'))
            print('''\n
            1. Bayar Pesanan (Ubah Status)
            2. Kembali ke Menu Pembeli
            ''')
            pilih = input("\nPilih (1/2): ").strip()
            
            if pilih == '1':
                # FITUR BAYAR PESANAN
                while True:
                    id_pesanan_bayar = input("\nMasukkan ID Pesanan yang ingin dibayar (0 untuk kembali): ").strip()
                    if id_pesanan_bayar == '0':
                        clear_all()
                        menu_pembeli(id_pengguna, username)
                        return
                    elif id_pesanan_bayar == '':
                        print("\nID pesanan tidak boleh kosong")
                        next()
                        continue
                    elif not id_pesanan_bayar.isdigit():
                        print("\nID pesanan harus berupa angka")
                        next()
                        continue
                    
                    # Cek apakah pesanan ada dan milik user ini
                    cursor.execute("""
                    SELECT p.id_pesanan, p.status_pesanan 
                    FROM pesanan p 
                    WHERE p.id_pesanan = %s AND p.id_pengguna = %s
                    """, (id_pesanan_bayar, id_pengguna))
                    
                    check_pesanan = cursor.fetchone()
                    
                    if check_pesanan is None:
                        print("\nPesanan tidak ditemukan atau bukan milik Anda")
                        next()
                        continue                 
                    if check_pesanan[1] != 'menunggu pembayaran':
                        print(f"\nPesanan ini sudah berstatus '{check_pesanan[1]}', tidak bisa diubah")
                        next()
                        continue
                    
                    # UPDATE status pesanan menjadi diproses
                    cursor.execute("""
                    UPDATE pesanan 
                    SET status_pesanan = %s 
                    WHERE id_pesanan = %s
                    """, ('diproses', id_pesanan_bayar))
                    
                    cursor.execute("""
                    UPDATE laporan 
                    SET status_akhir = %s 
                    WHERE id_pesanan = %s
                    """, ('diproses', id_pesanan_bayar))
                    
                    connection.commit()
                    
                    print(f"\nPesanan ID {id_pesanan_bayar} berhasil dibayar!")
                    next()
                    pembeli_cek_pesanan(id_pengguna, username)
                    return                  
            elif pilih == '2':
                clear_all()
                menu_pembeli(id_pengguna, username)
                return
            else:
                print("\nPilihan tidak valid")
                next()
                clear_all()
                menu_pembeli(id_pengguna, username)
                return
        else:
            print(f'{username} tidak memiliki pesanan')
            next()
            cursor.close()
            connection.close()
            menu_pembeli(id_pengguna, username)
            return
        
    except Error as error:
        print(f"\nTerjadi kesalahan saat mengecek pesanan: {error}")
        next()
        if connection:
            connection.close()
        menu_pembeli(id_pengguna, username)
        return

def pembeli_riwayat_pesanan(id_pengguna, username):
    clear_all()
    connection = connect_db()
    if connection is None:
        return
        
    try: 
        cursor = connection.cursor()

        cek_laporan =  """SELECT l.tanggal_laporan,
                                pr.nama_produk,
                                dp.jumlah_pesanan,
                                l.status_akhir,
                                p.metode_pembayaran,
                                CONCAT(j.nama_jalan, ', ', d.nama_desa, ', ', k.nama_kecamatan, ', ', kb.nama_kabupaten) AS alamat
                        FROM laporan l
                        JOIN pesanan p ON p.id_pesanan = l.id_pesanan
                        JOIN detail_pesanan dp ON p.id_pesanan = dp.id_pesanan
                        JOIN produk pr ON dp.id_produk = pr.id_produk
                        JOIN pengguna pg ON p.id_pengguna = pg.id_pengguna
                        JOIN jalan j ON pg.id_jalan = j.id_jalan
                        JOIN desa d ON j.id_desa = d.id_desa
                        JOIN kecamatan k ON d.id_kecamatan = k.id_kecamatan
                        JOIN kabupaten kb ON k.id_kabupaten = kb.id_kabupaten
                        WHERE p.id_pengguna = %s AND l.status_akhir IN ('selesai', 'dibatalkan')
                        ORDER BY l.tanggal_laporan DESC"""
        cursor.execute(cek_laporan, (id_pengguna,))
        laporan = cursor.fetchall()

        if laporan:
            print(f'\n===== RIWAYAT PEMBELIAN {username} =====\n')
            headers = ['Tanggal', 'Nama Produk', 'Jumlah Produk', 'Status Pesanan', 'Metode Bayar', 'Alamat']
            print(tabulate(laporan, headers=headers, tablefmt='fancy_grid'))
            back()
            menu_pembeli(id_pengguna, username)
        else:
            print(f'{username} tidak memiliki riwayat pesanan')
            next()
            cursor.close()
            connection.close()
            menu_pembeli(id_pengguna, username)
            return
        
    except Error as error:
        print(f"\nTerjadi kesalahan saat meihat riwayat pesanan: {error}")
        next()
        if connection:
            connection.close()
        clear_all()
        menu_pembeli(id_pengguna, username)

def menu_penjual(id_pengguna, username):
    clear_all()
    print(f'''
 __  __                    ____             _             _ 
|  \/  | ___ _ __  _   _  |  _ \ ___ _ __  (_)_   _  __ _| |
| |\/| |/ _ \ '_ \| | | | | |_) / _ \ '_ \ | | | | |/ _` | |
| |  | |  __/ | | | |_| | |  __/  __/ | | || | |_| | (_| | |
|_|  |_|\___|_| |_|\__,_| |_|   \___|_| |_|/ |\__,_|\__,_|_|
                                         |__/               

Selamat Datang {username} Di Entropin!

1. Kelola Produk
2. Lihat Riwayat Penjualan
3. Lihat harga Pasar
4. Logout
''')
    pilihan = input("Pilih Menu(1-4): ")
    if pilihan == "1":
        clear_all()
        penjual_kelola_produk(id_pengguna, username)
    elif pilihan == "2":
        clear_all()
        penjual_riwayat_penjualan(id_pengguna, username)
    elif pilihan == "3":
        clear_all()
        penjual_lihat_pasar(id_pengguna, username)
    elif pilihan == "4":
        clear_all()
        main_menu()
    else:
        print("Pilihan tidak valid")
        back()
        menu_penjual(id_pengguna, username)


def penjual_kelola_produk(id_pengguna, username):
    clear_all()
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        
        print('''
    ===== KELOLA PRODUK ENTROPIN =====

    1. Lihat Produk
    2. Tambah Produk 
    3. Update Produk
    4. Hapus Produk
    5. Kembali
    ''')
        
        pilihan = input("Pilih(1-5): ")
        
        if pilihan == "1": #penjual lihat produk entropin
            clear_all()
            query = """
            SELECT 
                p.id_produk, 
                p.nama_produk, 
                p.stok_produk, 
                p.harga_produk, 
                k.jenis_produk, 
                k.deskripsi_produk,
                p.id_pengguna 
            FROM
                produk p
            JOIN kategori_produk k ON p.id_kategori_produk = k.id_kategori_produk
            WHERE is_delete = FALSE AND stok_produk > 0
            """
        
            cursor.execute(query)
            produk = cursor.fetchall()
            
            if produk:
                print("\n===== PRODUK ENTROPIN =====\n")
                headers = ["ID", "NAMA PRODUK", "STOK", "HARGA", "KATEGORI", "DESKRIPSI", "ID PENGGUNA"]
                print(tabulate(produk, headers=headers, tablefmt="fancy_grid"))
                input("\nTekan enter untuk kembali ke menu penjual")
                clear_all()
                penjual_kelola_produk(id_pengguna, username)
            else:
                print("\nBelum ada produk.")
                next()
                penjual_kelola_produk(id_pengguna, username)
        
        elif pilihan == "2": #penjual menambahkan produk
            clear_all()
            while True:
                nama_produk = input("Nama Produk (0 untuk selesai): ").strip()
                if nama_produk == '':
                    print('\nNama produk tidak boleh kosong')
                    next()
                    continue
                elif nama_produk == "0":
                    input("\nTekan enter untuk kembali ke menu penjual")
                    next()
                    cursor.close()
                    connection.close()
                    return menu_penjual(id_pengguna, username)
                while True:
                    harga_produk = int(input("Harga Produk: "))
                    if harga_produk == '':
                        print('\nHarga tidak boleh kosong')
                        next()
                        continue
                    else:
                        break
                while True:
                    stok_produk = int(input("Stok Produk: "))
                    if stok_produk == '':
                        print('\nStok produk tidak boleh kosong')
                        next()
                        continue
                    else:
                        break
                while True:
                    print('''\n===== NAMA KATEGORI =====\n
                            1. Hasil Panen
                            2. Olahan Pertanian
                            3. Bibit dan Benih
                            4. Pupuk dan Nutrisi Tanaman
                        ''')
                    kategori = input("Kategori Produk: ").strip()
                    if kategori == '':
                        print('Kategori tidak boleh kosong')
                        next()
                        continue
                    
                    cursor.execute("SELECT id_kategori_produk FROM kategori_produk WHERE jenis_produk = %s ", (kategori,))
                    nama_kategori = cursor.fetchone()

                    if nama_kategori is None:
                        print('\nNama kategori tidak ada. Silahkan masukkan nama kategori dengan benar')
                        next()
                        continue
                    elif nama_kategori is not None:
                        id_kategori_produk = nama_kategori[0]
                        next()
                        break

                tambah_produk = """
                INSERT INTO produk (nama_produk, harga_produk, stok_produk, id_kategori_produk, is_delete, id_pengguna)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(tambah_produk, (nama_produk, harga_produk, stok_produk, id_kategori_produk, False, id_pengguna))
                connection.commit()
                print(f"Produk {nama_produk} berhasil ditambahkan")
                next()
                penjual_kelola_produk(id_pengguna, username)
        
        elif pilihan == "3": #penjual update produk
            clear_all()
            pilih_produk = "SELECT id_produk, nama_produk, harga_produk, stok_produk FROM produk WHERE is_delete = FALSE AND id_pengguna = %s"
            cursor.execute(pilih_produk, (id_pengguna,))
            produk = cursor.fetchall()
            
            if produk:
                header = ["ID", "Nama", "Harga", "Stok"]
                print(tabulate(produk, headers=header, tablefmt="fancy_grid"))
                
                while True:
                    id_produk = int(input("ID Produk yang akan diupdate (0 untuk kembali): "))
                    if id_produk == "":
                        print("ID tidak boleh kosong")
                        next()
                        continue
                    elif id_produk == "0":
                        input("\nTekan enter untuk kembali ke menu penjual")
                        next()
                        cursor.close()
                        connection.close()
                        return menu_penjual(id_pengguna, username)
                    else:
                        break
                while True:
                    harga = int(input("Harga baru: "))
                    if harga == "":
                        print("Harga tidak boleh kosong")
                        next()
                        continue
                    else:
                        break
                while True:
                    stok = int(input("Stok baru: "))
                    if stok == "":
                        print("Stok tidak boleh kosong")
                        next()
                        continue
                    else:
                        break
                
                query = "UPDATE produk SET harga_produk = %s, stok_produk = %s WHERE id_produk = %s"
                cursor.execute(query, (harga, stok, id_produk))
                connection.commit()
                print(f"\nUpdate produk dengan ID {id_produk} berhasil")
                next()
                penjual_kelola_produk(id_pengguna, username)
            else:
                print("\nBelum ada produk")
                next()
                penjual_kelola_produk(id_pengguna, username)
        
        elif pilihan == "4": #penjual menghapus produk
            clear_all()
            hapus_produk = "SELECT id_produk, nama_produk, harga_produk, stok_produk FROM produk WHERE is_delete = FALSE AND id_pengguna = %s"
            cursor.execute(hapus_produk, (id_pengguna,))
            produk = cursor.fetchall()
            
            if produk:
                headers = ["ID", "Nama", "Harga", "Stok", ]
                print(tabulate(produk, headers=headers, tablefmt="fancy_grid"))
                
                while True:
                    id_produk = int(input("ID Produk yang akan dihapus (0 untuk kembali): "))
                    if id_produk == "":
                        print("ID tidak boleh kosong")
                        next()
                        continue
                    elif id_produk == "0":
                        input("\nTekan enter untuk kembali ke menu penjual")
                        next()
                        cursor.close()
                        connection.close()
                        return menu_penjual(id_pengguna, username)
                    else:
                        break

                query = "UPDATE produk SET is_delete = TRUE WHERE id_produk = %s"
                cursor.execute(query, (id_produk,))
                connection.commit()
                print("\nProduk berhasil dihapus")
                next()
                penjual_kelola_produk(id_pengguna, username)
            else:
                print("\nBelum ada produk")
                next()
                penjual_kelola_produk(id_pengguna, username)
        elif pilihan == "5": #menu kembali
            input("\nTekan enter untuk kembali ke menu penjual")
            clear_all()
            menu_penjual(id_pengguna, username)
        else:
            print('Menu Yang Dipilih Tidak Tersedia')
            next()
            cursor.close()
            connection.close()
            clear_all()
            penjual_kelola_produk(id_pengguna, username)
            return

    except Error as error:
        print(f"\nTerjadi kesalahan saat mengelola produk: {error}")
        input("Tekan Enter untuk melanjutkan...")
        if connection:
            connection.close()
        clear_all()
        penjual_kelola_produk(id_pengguna, username)

def penjual_riwayat_penjualan(id_pengguna, username):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        riwayat = """SELECT pr.nama_produk,
                            kat.jenis_produk,
                            SUM(dp.jumlah_pesanan) AS total_terjual,
                            COUNT(dp.id_pesanan) AS banyak_dibeli,
                            SUM(dp.jumlah_pesanan * pr.harga_produk) AS total_pendapatan,
                            pr.stok_produk AS sisa_stok
                    FROM produk pr
                    JOIN detail_pesanan dp ON pr.id_produk = dp.id_produk
                    JOIN kategori_produk kat ON pr.id_kategori_produk = kat.id_kategori_produk
                    WHERE pr.id_pengguna = %s
                    GROUP BY pr.id_produk, pr.nama_produk, kat.jenis_produk, pr.stok_produk
                    ORDER BY total_pendapatan DESC"""
        cursor.execute(riwayat, (id_pengguna,))
        data_riwayat = cursor.fetchall()
        
        if data_riwayat:
            print(f"\n===== RIWAYAT PENJUALAN {username} =====\n")
            headers = ["NAMA PRODUK", "TERJUAL", "BANYAK DIBELI", "PENDAPATAN", "SISA STOK"]
            print(tabulate(data_riwayat, headers=headers, tablefmt="fancy_grid"))
            
            grand_total = sum(row[4] for row in data_riwayat)
            print(f"\nTotal Omset Keseluruhan: Rp {grand_total}")
            back()
            menu_penjual(id_pengguna, username)
        else:
            print("\nBelum ada riwayat penjualan")
            next()
            cursor.close()
            connection.close()
            clear_all()
            menu_penjual(id_pengguna, username)
            return

    except Error as error:
        print(f"\nTerjadi kesalahan saat melihat riwayat: {error}")
        input("Tekan Enter untuk melanjutkan...")
        if connection:
            connection.close()
        clear_all()
        menu_penjual(id_pengguna, username)

def penjual_lihat_pasar(id_pengguna, username):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        
        cek_pasar = """SELECT nama_produk_pasar, 
                        harga_min_kelola_pasar, 
                        harga_max_kelola_pasar, 
                        harga_rata_kelola_pasar, 
                        lokasi_pasar
                    FROM kelola_pasar
                    WHERE is_delete = FALSE
                    ORDER BY nama_produk_pasar"""
        
        cursor.execute(cek_pasar)
        data_pasar = cursor.fetchall()
        if data_pasar:
            print("\n===== DAFTAR HARGA PASAR =====\n")

            headers = ["PRODUK", "HARGA MIN", "HARGA MAX", "HARGA RATA-RATA", "LOKASI"]
            print(tabulate(data_pasar, headers=headers, tablefmt="fancy_grid"))

            print("\nGunakan data ini sebagai referensi harga jual produk Anda!")
            next()
            menu_penjual(id_pengguna, username)
        else:
            print("\nBelum ada data harga pasar")
            next()
            cursor.close()
            connection.close()
            clear_all()
            menu_pembeli(id_pengguna, username)
            return

    except Error as error:
        print(f"\nTerjadi kesalahan saat melihat harga pasar: {error}")
        input("Tekan Enter untuk melanjutkan...")
        if connection:
            connection.close()
        clear_all()
        penjual_lihat_pasar(id_pengguna, username)

def menu_admin(id_pengguna, username):
    clear_all()
    print(f"""
 __  __                       _       _           _       
|  \/  | ___ _ __  _   _     / \   __| |_ __ ___ (_)_ __  
| |\/| |/ _ \ '_ \| | | |   / _ \ / _` | '_ ` _ \| | '_ \ 
| |  | |  __/ | | | |_| |  / ___ \ (_| | | | | | | | | | |
|_|  |_|\___|_| |_|\__,_| /_/   \_\__,_|_| |_| |_|_|_| |_|

Selamat Datang {username} Di Entropin!

1. Cek Pesanan
2. Kelola Pasar
3. Logout
""")
    
    pilih = input('Pilih Menu (1-3) : ')

    if pilih == '1':
        clear_all()
        admin_cek_pesanan(id_pengguna, username)       
    elif pilih == '2':
        clear_all()
        admin_kelola_pasar(id_pengguna, username)
    elif pilih == "3":
        clear_all()
        main_menu()
    else:
        print("Pilihan tidak ditemukan")
        next()
        menu_admin(id_pengguna, username)
        return

def admin_cek_pesanan(id_pengguna, username):
    while True:
        clear_all()
        connection = connect_db()
        if connection is None:
            return
        
        try:
            cursor = connection.cursor()

            query = """SELECT p.id_pesanan,
                            p.tanggal_pesanan,
                            p.status_pesanan,
                            pr.nama_produk,
                            dp.jumlah_pesanan,
                            p.metode_pembayaran,
                            pe.nama_pengguna,
                            CONCAT(j.nama_jalan, ', ', d.nama_desa, ', ', k.nama_kecamatan, ', ', kb.nama_kabupaten) AS alamat
                        FROM pesanan p
                        JOIN detail_pesanan dp ON p.id_pesanan = dp.id_pesanan
                        JOIN produk pr ON dp.id_produk = pr.id_produk
                        JOIN pengguna pe ON p.id_pengguna = pe.id_pengguna
                        JOIN jalan j ON pe.id_jalan = j.id_jalan
                        JOIN desa d ON j.id_desa = d.id_desa
                        JOIN kecamatan k ON d.id_kecamatan = k.id_kecamatan
                        JOIN kabupaten kb ON k.id_kabupaten = kb.id_kabupaten
                        WHERE pe.role = 'pembeli'
                        ORDER BY p.tanggal_pesanan ASC"""
            cursor.execute(query)
            pesanan_list = cursor.fetchall()

            if pesanan_list:
                clear_all()
                print("\n === DAFTAR PESANAN ===")

                headers = ["ID", "TGL PESANAN", "STATUS", "PRODUK", "QUANTITY", "METODE BAYAR", "PELANGGAN", "ALAMAT"]
                print(tabulate(pesanan_list, headers=headers, tablefmt="fancy_grid"))
            
            else:
                print("\nBelum ada pesanan.")
                next()
                cursor.close()
                connection.close()
                return menu_admin(id_pengguna, username)

            print("\n === UBAH STATUS PESANAN ===")
            print("(Masukkan '0' untuk kembali ke menu admin)")
            id_pesanan = input("\n Masukkan id pesanan: ").strip()
            
            if id_pesanan == '':
                print("\nID pesanan tidak boleh kosong")
                next()
                continue
            elif not id_pesanan.isdigit():
                print("\nID pesanan harus berupa angka")
                next()
                continue
            elif id_pesanan == '0':
                next()
                cursor.close()
                connection.close()
                return menu_admin(id_pengguna, username)

            print("""\nStatus yang tersedia:
                1. dikirim
                2. selesai
                3. dibatalkan""")

            status_pilihan = input("\nPilih status baru (1-3): ").strip()
            
            status_map = {
                "1": "dikirim",
                "2": "selesai",
                "3": "dibatalkan"}

            if status_pilihan in status_map:
                status_baru = status_map[status_pilihan]
                    
                update_pesanan = """UPDATE pesanan
                                SET status_pesanan = %s
                                WHERE id_pesanan = %s
                                """
                cursor.execute(update_pesanan, (status_baru, id_pesanan))
                connection.commit()

                update_laporan = """UPDATE laporan
                                SET status_akhir = %s
                                WHERE id_pesanan = %s
                                """
                cursor.execute(update_laporan, (status_baru, id_pesanan))
                connection.commit()
                    
                print(f"\n Status pesanan dengan ID {id_pesanan} berhasil diubah menjadi {status_baru}")
                next()
                continue   
            else:
                print("\nPilihan tidak valid")
                next()
                continue
                
        
        except Error as error:
            print(f"\n Error: {error}")
            if connection:
                connection.close()
            next()
            return menu_admin(id_pengguna, username)
        
def admin_kelola_pasar(id_pengguna, username):
    clear_all()
    connection = connect_db()
    if connection is None:
        print("koneksi tidak berhasil")
        return
    try:
        cursor = connection.cursor()

        print("""\n===== KELOLA PASAR =====\n
        1. lihat data pasar
        2. tambah data pasar
        3. update data pasar
        4. hapus data pasar
        5. kembali
        """)

        pilih = input("\n silahkan pilih nomor(1-5): ")

        if pilih == '1': #lihat data pasar
            clear_all()
            pasar = """SELECT id_kelola_pasar,
                            nama_produk_pasar,
                            harga_min_kelola_pasar,
                            harga_max_kelola_pasar,
                            harga_rata_kelola_pasar,
                            lokasi_pasar
                    FROM kelola_pasar 
                    WHERE is_delete = FALSE"""
            cursor.execute(pasar)
            data_pasar = cursor.fetchall()

            headers = ["ID", "NAMA PRODUK", "HARGA MIN", "HARGA MAX", "HARGA RATA-RATA", "LOKASI"]
            print(tabulate(data_pasar, headers=headers, tablefmt="fancy_grid"))

            back()
            admin_kelola_pasar(id_pengguna, username)

        elif pilih == '2': #tambah data pasar
            clear_all()
            print("ketik 0 untuk kembali ke menu sebelumnya")
            while True:
                nama_produk = input("Masukan nama produk: ").title()
                if nama_produk == '':
                    print('\nNama produk tidak boleh kosong')
                    next()
                    continue
                elif nama_produk == "0":
                    next()
                    cursor.close()
                    connection.close()
                    return admin_kelola_pasar(id_pengguna, username)
                else:
                    break
            while True:
                harga_minim = input("harga minimal produk: ")
                if harga_minim == '':
                    print('\nHarga minimal tidak boleh kosong')
                    next()
                    continue
                elif harga_minim == "0":
                    next()
                    cursor.close()
                    connection.close()
                    return admin_kelola_pasar(id_pengguna, username)
                elif not harga_minim.isdigit():
                    print('\nHarga minimal harus berupa angka')
                    next()
                    continue
                else:
                    break
            while True:
                harga_maksimal = input("harga max produk: ")
                if harga_maksimal == '':
                    print('\nHarga maksimal tidak boleh kosong')
                    next()
                    continue
                elif harga_maksimal == "0":
                    next()
                    cursor.close()
                    connection.close()
                    return admin_kelola_pasar(id_pengguna, username)
                elif not harga_maksimal.isdigit():
                    print('\nHarga maksimal harus berupa angka')
                    next()
                    continue
                else:
                    break
            while True:
                harga_rata_rata = input("harga rata-rata produk: ")
                if harga_rata_rata == '':
                    print('\nHarga rata-rata tidak boleh kosong')
                    next()
                    continue
                elif harga_rata_rata == "0":
                    next()
                    cursor.close()
                    connection.close()
                    return admin_kelola_pasar(id_pengguna, username)
                elif not harga_rata_rata.isdigit():
                    print('\nHarga rata-rata harus berupa angka')
                    next()
                    continue
                else:
                    break
            while True:
                lokasi_pasar = input("lokasi pasar: ").title()
                if lokasi_pasar == '':
                    print('\nLokasi pasar tidak boleh kosong')
                    next()
                    continue
                elif lokasi_pasar == "0":
                    next()
                    cursor.close()
                    connection.close()
                    return admin_kelola_pasar(id_pengguna, username)
                else:
                    break
            query = """
            INSERT INTO kelola_pasar(nama_produk_pasar,
                        harga_min_kelola_pasar, 
                        harga_max_kelola_pasar, 
                        harga_rata_kelola_pasar, 
                        lokasi_pasar, 
                        is_delete, 
                        id_pengguna)
            VALUES  (%s, %s, %s, %s, %s, %s, %s)"""

            cursor.execute(query, (nama_produk, harga_minim, harga_maksimal, harga_rata_rata, lokasi_pasar, 'FALSE', id_pengguna ))
            connection.commit()

            print("\nPRODUK BERHASIL DITAMBAHKAN!")
            back()
            admin_kelola_pasar(id_pengguna, username)

        elif pilih == "3": #update data pasar
            clear_all()
            query = """SELECT id_kelola_pasar,
                            nama_produk_pasar,
                            harga_min_kelola_pasar,
                            harga_max_kelola_pasar,
                            harga_rata_kelola_pasar,
                            lokasi_pasar
                    FROM kelola_pasar 
                    WHERE is_delete = FALSE"""
            cursor.execute(query)
            data = cursor.fetchall()

            if data:
                headers = ["ID", "NAMA PRODUK", "HARGA MIN", "HARGA MAX", "HARGA RATA-RATA", "LOKASI"]
                print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

                print("Ketik 0 untuk kembali ke menu sebelumnya")
                while True:
                    id_pasar = int(input("masukkan id pasar yang ingin diperbarui: "))
                    if id_pasar == "":
                        print("\nID pasar tidak boleh kosong")
                        next()
                        continue
                    elif id_pasar == 0:
                        back()
                        cursor.close()
                        connection.close()
                        return admin_kelola_pasar(id_pengguna, username)
                    else:
                        break
                while True:
                    harga_minim = int(input("Masukkan harga minimal: "))
                    if harga_minim == "":
                        print('\nHarga minimal tidak boleh kosong')
                        next()
                        continue
                    elif harga_minim == 0:
                        back()
                        cursor.close()
                        connection.close()
                        return admin_kelola_pasar(id_pengguna, username)
                    else:
                        break  
                while True:
                    harga_maksimal = int(input("Masukkan harga maksimal: "))
                    if harga_maksimal == "":
                        print('\nHarga maksimal tidak boleh kosong')
                        next()
                        continue
                    elif harga_maksimal == 0:
                        back()
                        cursor.close()
                        connection.close()
                        return admin_kelola_pasar(id_pengguna, username)
                    else:
                        break
                while True:
                    harga_rata_rata = int(input("Masukkan harga rata-rata: "))
                    if harga_rata_rata == "":
                        print('\nHarga rata-rata tidak boleh kosong')
                        next()
                        continue
                    elif harga_rata_rata == 0:
                        back()
                        cursor.close()
                        connection.close()
                        return admin_kelola_pasar(id_pengguna, username)
                    else:
                        break
                query = """ UPDATE kelola_pasar
                            SET harga_min_kelola_pasar = %s, 
                                harga_max_kelola_pasar = %s,
                                harga_rata_kelola_pasar = %s 
                            WHERE id_kelola_pasar = %s
                            ORDER BY id_kelola_pasar"""
                cursor.execute(query,(harga_minim, harga_maksimal, harga_rata_rata, id_pasar))
                connection.commit()

                print("\nDATA BERHASIL DIUBAH...")
                back()
                admin_kelola_pasar(id_pengguna, username)
            else:
                print("\nbelum ada data pasar")
                next()
                admin_kelola_pasar(id_pengguna, username)

        elif pilih == "4": #hapus data pasar
            clear_all()
            query ="""SELECT id_kelola_pasar,
                            nama_produk_pasar,
                            harga_min_kelola_pasar,
                            harga_max_kelola_pasar,
                            harga_rata_kelola_pasar,
                            lokasi_pasar
                    FROM kelola_pasar 
                    WHERE is_delete = FALSE"""
            cursor.execute(query)
            data = cursor.fetchall()

            if data:
                headers = ["ID", "PRODUK", "HARGA MINIM", "HARGA MAX", "HARGA RATA-RATA", "LOKASI"]
                print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

                while True:
                    id_pasar = input("\nMasukkan id pasar yang ingin dihapus (0 untuk kembali): ")
                    if id_pasar == '':
                        print("\nID pasar tidak boleh kosong")
                        next()
                        cursor.close()
                        connection.close()
                        return admin_kelola_pasar(id_pengguna, username)
                    elif id_pasar == "0":
                        back()
                        cursor.close()
                        connection.close()
                        return admin_kelola_pasar(id_pengguna, username)
                    else:
                        break

                query ="""UPDATE kelola_pasar 
                        SET is_delete = TRUE 
                        WHERE id_kelola_pasar = %s"""
                cursor.execute(query, (id_pasar,))
                connection.commit()

                print("\nData pasar berhasil dihapus")
                back()
                admin_kelola_pasar(id_pengguna, username)
        elif pilih == "5": #kembali
            back()
            menu_admin(id_pengguna, username)
        else:
            print("\nData pasar tidak ditemukan")
            next()
            cursor.close()
            connection.close()
            clear_all()
            menu_admin(id_pengguna, username)
            return

    except Error as error:
        print(f"\nTerjadi kesalahan saat registrasi: {error}")
        input("Tekan Enter untuk melanjutkan...")
        if connection:
            connection.close()
        clear_all()
        menu_admin()

clear_all()
print(r"""
          _                                 ____                              
  ()     | |                               (|   \                             
  /\  _  | |  __,   _  _  _    __, _|_      |    | __, _|_  __,   _  _    __, 
 /  \|/  |/  /  |  / |/ |/ |  /  |  |      _|    |/  |  |  /  |  / |/ |  /  | 
/(__/|__/|__/\_/|_/  |  |  |_/\_/|_/|_/   (/\___/ \_/|_/|_/\_/|_/  |  |_/\_/|/
                                                                           /| 
                                                                           \|                              
""")
input("Silahkan Tekan Enter Untuk Melanjutkan Ke Sistem ENTROPIN!")
clear_all()
main_menu()