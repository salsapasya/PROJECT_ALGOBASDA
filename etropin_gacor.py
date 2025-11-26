
import psycopg2
from psycopg2 import Error
from tabulate import tabulate
import os

def connect_db():
    try:
        connection = psycopg2.connect(
            user = "postgres",
            password = "enikcantik10",
            host = "localhost",
            port = "5432",
            database = "etropin_yg baru"
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
    while True:
        kembali = input("Silahkan Tekan Enter Untuk Kembali")
        if kembali == '':
            clear_all()
            break

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

            if role == "admin":
                menu_admin(id_pengguna, username)
            # if role == "penjual":
            #     menu_penjual(username_pengguna)
            # if role == "pembeli":
            #     menu_pembeli(id_pengguna, username)
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

def menu_admin(id_pengguna, username):
    print('''=== MENU ADMIN ===
          1. Cek Pesanan
          2. Kelola Pasar''')
    
    pilih = input('Pilih Menu (1/2) : ')

    if pilih == '1':
        clear_all()
        cek_pesanan(id_pengguna, username)
        
    elif pilih == '2':
        clear_all()
        kelola_pasar(id_pengguna, username)
    else:
        print("Maaf, pilihan tidak ditemukan")
        input("tekan enter untuk melanjutkan...")

    menu_admin(id_pengguna, username)

def cek_pesanan(id_pengguna, username):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()

        query = """SELECT p.id_pesanan,
                           p.tanggal_pesanan,
                           p.status_pesanan,
                           p.nama_produk,
                           dp.jumlah_pesanan,
                           p.metode_pembayaran,
                           pe.nama_pengguna
                    FROM pesanan p
                    JOIN pengguna pe ON p.id_pengguna = pe.id_pengguna
                    JOIN detail_pesanan dp ON p.id_pesanan = dp.id_pesanan
                    WHERE pe.role = 'pembeli'
                    ORDER BY p.tanggal_pesanan ASC"""
        cursor.execute(query)
        pesanan_list = cursor.fetchall()

        if pesanan_list:
            print("\n === DAFTAR PESANAN ===")

            headers = ["ID", "TANGGAL PESANAN", "STATUS", "PRODUK", "JUMLAH PRODUK", "METODE PEMBAYARAN", "PELANGGAN"]
            print(tabulate(pesanan_list, headers=headers, tablefmt="fancy_grid"))
            
            print("\n === UBAH STATUS PESANAN ===")
            id_pesanan = input("\n Masukkan id pesanan: ")

            print("""\nStatus yang tersedia:
                  1. dikirim
                  2. selesai
                  3. dibatalkan""")

            status_pilihan = input("\nPilih status baru (1-3): ")

            status_map = {
                "1": "dikirim",
                "2": "selesai",
                "3": "dibatalkan"
            }

            if status_pilihan in status_map:
                status_baru = status_map[status_pilihan]
                
                update_query = """UPDATE pesanan
                           SET status_pesanan = %s
                           WHERE id_pesanan = %s
                           """
                cursor.execute(update_query,(status_baru, id_pesanan))
                connection.commit()

                print(f"\n status pesanan dengan ID {id_pesanan} berhasil diubah menjadi {status_baru}")
                next()
                menu_admin(id_pengguna, username)    
            else:
                print("\nPilihan tidak valid")
                next()
                cek_pesanan(id_pengguna, username)
        else:
            print("\nBelum ada pesanan.")

            cursor.close()
        connection.close()
        input("\nTekan Enter...")
        clear_all()
        menu_admin(id_pengguna, username)
        
    except Error as error:
        print(f"\n Error: {error}")
        if connection:
            connection.close()
        input("Tekan Enter...")
        clear_all()
        menu_admin(id_pengguna, username)

def kelola_pasar(id_pengguna, username):
    clear_all()
    connection = connect_db()
    if connection is None:
        print("koneksi tidak berhasil")
        return
    try:
        cursor = connection.cursor()

        print("""===== KELOLA PASAR =====
              1. lihat data pasar
              2. tambah data pasar
              3. update data pasar
              4. hapus data pasar""")

        pilih = input("\n silahkan pilih nomor(1-4):")

        if pilih == '1': #lihat data pasar
            clear_all()
            pasar = """SELECT * FROM kelola_pasar WHERE is_delete = FALSE"""
            cursor.execute(pasar)
            data_pasar = cursor.fetchall()
            headers = ["PRODUK", "HARGA MIN", "HARGA MAX", "HARGA RATA-RATA", "LOKASI"]
            print(tabulate(data_pasar, headers=headers, tablefmt="fancy_grid"))

            back()
            kelola_pasar(id_pengguna, username)

        elif pilih == '2': #tambah data pasar
            clear_all()
            nama_produk = input("Masukan nama produk: ").title()
            harga_minim = input("harga minimal produk: ")
            harga_maksimal = input("harga max produk: ")
            harga_rata_rata = input("harga rata-rata produk: ")
            lokasi_pasar = input("lokasi pasar: ").title()
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
            kelola_pasar(id_pengguna, username)

        elif pilih == "3": #update data pasar
            clear_all()
            query = """SELECT id_kelola_pasar,
                              nama_produk_pasar,
                              harga_min_kelola_pasar,
                              harga_max_kelola_pasar,
                              harga_rata_kelola_pasar,
                              lokasi_pasar
                    FROM kelola_pasar 
                    WHERE is_delete = TRUE"""
            cursor.execute(query)
            data = cursor.fetchall()

            if data:
                headers = ["ID", "NAMA PRODUK", "HARGA MIN", "HARGA MAX", "HARGA RATA-RATA", "LOKASI"]
                print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

                id_pasar = int(input("masukkan id pasar yang ingin diperbarui: "))
                harga_minim = int(input("Masukkan harga minimal: "))
                harga_maksimal = int(input("Masukkan harga maksimal: "))
                harga_rata_rata = int(input("Harga rata-rata: "))

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
                kelola_pasar(id_pengguna, username)
            else:
                print("\nbelum ada data pasar")
                next()
                kelola_pasar(id_pengguna, username)

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

            id_pasar = input("\nMasukkan id pasar yang ingin dihapus: ")

            query ="""UPDATE kelola_pasar 
                      SET is_delete = TRUE 
                      WHERE id_kelola_pasar = %s"""
            cursor.execute(query, (id_pasar,))
            connection.commit()

            print("\nData pasar berhasil dihapus")
            back()
            kelola_pasar(id_pengguna, username)
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

