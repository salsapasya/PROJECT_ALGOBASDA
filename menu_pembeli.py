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
            database = "entropin coba"
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
    print(r'''                                   _                        
 _ __ ___   ___ _ __  _   _   _   _| |_ __ _ _ __ ___   __ _ 
| '_ ` _ \ / _ \ '_ \| | | | | | | | __/ _` | '_ ` _ \ / _` |
| | | | | |  __/ | | | |_| | | |_| | || (_| | | | | | | (_| |
|_| |_| |_|\___|_| |_|\__,_|  \__,_|\__\__,_|_| |_| |_|\__,_|
    
    1. Register
    2. Login
    3. Logout Sistem
    ''')
    select_menu = input("Pilih Main Menu (1/2) : ")
    while True:
        if select_menu == "1":
            clear_all()
            register()
        elif select_menu == "2":
            clear_all()
            login()
        elif select_menu == "3":
            clear_all()
            break
        else :
            print("Pilihan Tidak Ditemukan")
            clear_all()
            main_menu()
        return

def register():
    print('''=== Silahkan memilih tipe pelaku ===
        1. Penjual
        2. Pembeli
''')
    tipe_pelaku = input("Pilih Tipe Pelaku (1/2) : ")
    while True :
        if tipe_pelaku == "1":
            clear_all()
            register_penjual()
        elif tipe_pelaku == "2":
            clear_all()
            register_pembeli()
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
        
        while True:
            nama = input('Nama Lengkap : ').strip()
            if nama == '':
                print('\nNama tidak boleh kosong')
                next()
                continue
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
        
    except Error as error:
        print(f"\nTerjadi kesalahan saat registrasi: {error}")
        input("Tekan Enter untuk melanjutkan...")
        if connection:
            connection.close()
        clear_all()
        register_penjual()

def register_pembeli():
    clear_all()
    connection = connect_db()
    if connection is None:
        print("Koneksi tidak berhasil")
        return
    
    try:
        cursor = connection.cursor()
        
        print("=== REGISTER PEMBELI ===\n")
        
        while True:
            nama = input('Nama Lengkap : ').strip()
            if nama == '':
                print('\nNama tidak boleh kosong')
                next()
                continue
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
        
    except Error as error:
        print(f"\nTerjadi kesalahan saat registrasi: {error}")
        input("Tekan Enter untuk melanjutkan...")
        if connection:
            connection.close()
        clear_all()
        register_pembeli()
    
def login():
    clear_all()
    connection = connect_db()
    if connection is None:
        print("Koneksi tidak berhasil")
        return
    
    try:
        cursor = connection.cursor()

        print("=== LOGIN SISTEM ===\n")

        username = input("Masukkan Username : ")
        password = input("Masukkan Password : ")

        # if username == "adminentropin" and password == "entropin":
        #     print("\nLogin berhasil sebagai ADMIN!")
        #     input("Tekan Enter...")
        #     cursor.close()
        #     connection.close()
        #     clear_all()
        #     menu_admin(username)
        #     return

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

            # if role == "admin":
            #     menu_admin(username_pengguna)
            # if role == "penjual":
            #     menu_penjual(username_pengguna)
            if role == "pembeli":
                menu_pembeli(id_pengguna, username)
            # else:
            #     print("Role tidak dikenali!")
            #     main_menu()
        else:
            print("\nUsername atau Password salah!")
            input("Tekan Enter untuk mencoba lagi...")
            cursor.close()
            connection.close()
            clear_all()
            login()
            
    except Error as error:
        print(f"\nTerjadi kesalahan saat login: {error}")
        input("Tekan Enter untuk melanjutkan...")
        if connection:
            connection.close()
        clear_all()
        login()

def menu_pembeli(id_pengguna, username):
    clear_all()
    print(f'''
                                                   _          _ _ 
 _ __ ___   ___ _ __  _   _   _ __   ___ _ __ ___ | |__   ___| (_)
| '_ ` _ \ / _ \ '_ \| | | | | '_ \ / _ \ '_ ` _ \| '_ \ / _ \ | |
| | | | | |  __/ | | | |_| | | |_) |  __/ | | | | | |_) |  __/ | |
|_| |_| |_|\___|_| |_|\__,_| | .__/ \___|_| |_| |_|_.__/ \___|_|_|
                             |_|                                  

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
        cek_pesanan(id_pengguna, username)
    elif pilih == '4':
        clear_all()
        riwayat_pesanan_pembeli(id_pengguna, username)
    elif pilih == '5':
        clear_all()
        main_menu()
    else:
        print('''
            Pilihan Tidak Valid
            Tekan Enter Untuk Kembali Ke Menu''')
        clear_all()
        menu_pembeli()
    
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
                    id_produk = int(input('Masukkan ID Produk (0 untuk selesai): '))
                    if id_produk == '':
                        print('ID tidak boleh dikosongi')
                        continue
                    elif id_produk == 0 :
                        input('Tekan Enter Untuk Kembali Ke Menu Pembeli')
                        menu_pembeli(id_pengguna, username)
                        return
                    jumlah_item = int(input('Masukkan Jumlah Yang Ingin Dibeli: '))
                    
                    cursor.execute("""SELECT nama_produk, harga_produk, stok_produk
                                        FROM produk
                                        WHERE id_produk = %s
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
                    else: 
                        print("Stok Tidak Cukup atau Produk Tidak Ada")
            elif pilih == '2':
                clear_all()
                menu_pembeli(id_pengguna, username)     
            else:
                print('Menu Yang Dipilih Tidak Tersedia')
                next()
                cursor.close()
                connection.close()
                clear_all()
                buyproduk_entropin(id_pengguna, username)
                return

    except Error as error:
        print(f"\nTerjadi kesalahan saat membeli produk: {error}")
        input("Tekan Enter untuk melanjutkan...")
        if connection:
            connection.close()
        clear_all()
        buyproduk_entropin()

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
            while True:
                metode_pembayaran = input("Metode Pembayaran (Nama Bank): ").strip()
                if metode_pembayaran == '':
                    print('\nSilahkan masukkan nama bank')
                    next()
                    continue
                else:
                    next()
                    break

            for item in keranjang:
                insert_pesanan = """
                INSERT INTO pesanan (tanggal_pesanan, 
                                    nama_produk,
                                    status_pesanan,
                                    metode_pembayaran,
                                    id_pengguna)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_pesanan
                """
                cursor.execute(insert_pesanan, (date.today(),
                                                item['nama_produk'],
                                                'menunggu pembayaran',
                                                metode_pembayaran,
                                                id_pengguna
                                ))
                id_pesanan = cursor.fetchone()[0]

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
                cursor.execute("""UPDATE produk 
                                    SET stok_produk = stok_produk - %s
                                    WHERE id_produk = %s""",
                                    (item['jumlah_item'], item['id_produk']))
                connection.commit()
        
            while True:
                bayar = input('Apakah anda ingin membayar (iya/tidak)? ').strip()
                if bayar == '':
                    print('\nTidak boleh diisi kosong')
                    next()
                    continue
                elif bayar == 'iya':
                    clear_all()
                    update_status = 'diproses'
                    cursor.execute("""UPDATE pesanan SET status_pesanan = %s
                                        WHERE id_pengguna = %s""",
                                    (update_status, id_pengguna))
                    connection.commit()

                    keranjang_entropin[id_pengguna] = []
                    print(f'\nPesanan {username} sedang diproses')
                    next()
                    menu_pembeli(id_pengguna, username)
                else:
                    menu_pembeli(id_pengguna, username)
                    break
        elif pilih == '2':
            while True:
                hapus_produk = int(input('Nomor Produk yang ingin dihapus : '))
                hapus_produk_fix = hapus_produk - 1
                if hapus_produk == '':
                    print('\nTidak boleh kosong')
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

def cek_pesanan(id_pengguna, username):
    clear_all()
    connection = connect_db()
    if connection is None:
        return
        
    try: 
        cursor = connection.cursor()

        cek_pesanan = """SELECT p.id_pesanan,
                                p.tanggal_pesanan,
                                p.nama_produk,
                                dp.jumlah_pesanan,
                                p.status_pesanan,
                                p.metode_pembayaran
                        FROM pesanan p
                        JOIN detail_pesanan dp ON p.id_pesanan = dp.id_pesanan
                        WHERE id_pengguna = %s"""
        cursor.execute(cek_pesanan, (id_pengguna,))
        pesanan = cursor.fetchall()
        
        if pesanan:
            print(f'\n===== DATA PESANAN {username} =====\n')
            headers = ['ID Pesanan', 'Tanggal Pesanan', 'Nama Produk', 'Banyak Produk', 'Status', 'Metode Bayar']
            print(tabulate(pesanan, headers=headers, tablefmt='fancy_grid'))
            back()
            menu_pembeli(id_pengguna, username)
        else:
            print(f'{username} tidak memiliki pesanan')
            next()
            cursor.close()
            connection.close()
            clear_all()
            menu_pembeli(id_pengguna, username)
            return
        
    except Error as error:
        print(f"\nTerjadi kesalahan saat mengecek pesanan: {error}")
        next()
        if connection:
            connection.close()
        clear_all()
        cek_pesanan(id_pengguna, username)

def riwayat_pesanan_pembeli(id_pengguna, username):
    clear_all()
    connection = connect_db()
    if connection is None:
        return
        
    try: 
        cursor = connection.cursor()

        cek_laporan = """SELECT p.tanggal_pesanan,
                                l.nama_produk,
                                dp.jumlah_pesanan,
                                l.status_pesanan,
                                p.metode_pembayaran
                        FROM pesanan p
                        JOIN laporan l ON p.id_pesanan = l.id_pesanan
                        JOIN detail_pesanan dp ON p.id_pesanan = dp.id_pesanan
                        WHERE id_pengguna = %s"""
        cursor.execute(cek_laporan, (id_pengguna,))
        laporan = cursor.fetchall()

        if laporan:
            print(f'\n===== RIWAYAT PEMBELIAN {username} =====\n')
            headers = ['Tanggal', 'Nama Produk', 'Jumlah Produk', 'Status Pesanan', 'Metode Bayar']
            print(tabulate(laporan, headers=headers, tablefmt='fancy_grid'))
            back()
            menu_pembeli(id_pengguna, username)
        else:
            print(f'{username} tidak memiliki riwayat pesanan')
            next()
            cursor.close()
            connection.close()
            clear_all()
            menu_pembeli(id_pengguna, username)
            return
        
    except Error as error:
        print(f"\nTerjadi kesalahan saat mengecek pesanan: {error}")
        next()
        if connection:
            connection.close()
        clear_all()
        cek_pesanan(id_pengguna, username)















    





clear_all()
print(r'''
          _                                 ____                              
  ()     | |                               (|   \                             
  /\  _  | |  __,   _  _  _    __, _|_      |    | __, _|_  __,   _  _    __, 
 /  \|/  |/  /  |  / |/ |/ |  /  |  |      _|    |/  |  |  /  |  / |/ |  /  | 
/(__/|__/|__/\_/|_/  |  |  |_/\_/|_/|_/   (/\___/ \_/|_/|_/\_/|_/  |  |_/\_/|/
                                                                           /| 
                                                                           \|                              
''')
input("Silahkan Tekan Enter Untuk Melanjutkan Ke Sistem")
clear_all()
main_menu()