import psycopg2
from psycopg2 import Error
from tabulate import tabulate
import os

def connect_db():
    try:
        connection = psycopg2.connect(
            user = "postgres",
            password = "sabila.19",
            host = "127.0.0.1",
            port = "5432",
            database = "entropin"
        )
        return connection
    except Error as error:
        print("Terjadi kesalahan, gagal terkoneksi dengan database", error)

def clear_all():
    os.system('cls')

def back():
    kembali = ("Silahkan Tekan Enter Untuk Kembali")
    if kembali == '':
        clear_all()
    else:
        back()
    return


def main_menu():
    print(r'''
_  _ ____ _  _ _  _    _  _ ___ ____ _  _ ____
|\/| |___ |\ | |  |    |  |  |  |__| |\/| |__|
|  | |___ | \| |__|    |__|  |  |  | |  | |  |
    1. Register
    2. Login
    ''')
    select_menu = input("Pilih Main Menu (1/2) : ")
    while True:
        if select_menu == "1":
            clear_all()
            register()
        elif select_menu == "2":
            clear_all()
            login()
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
        
        nama = input("Masukkan Nama Lengkap: ")
        alamat = input("Masukkan Alamat (nama jalan): ")
        nomor_telepon = input("Masukkan Nomor Telepon: ")
        desa = input("Masukkan Desa: ")
        kecamatan = input("Masukkan Kecamatan: ")
        kabupaten = input("Masukkan Kabupaten: ")
        username = input("Masukkan Username: ")
        password = input("Masukkan Password: ")
        role = "penjual" 
        
        check_query = "SELECT username_pengguna FROM pengguna WHERE username_pengguna = %s"
        cursor.execute(check_query, (username,))
        check_user = cursor.fetchone()
        
        if check_user:
            print("\nUsername sudah terdaftar! Silahkan gunakan username lain.")
            input("Tekan Enter untuk melanjutkan...")
            cursor.close()
            connection.close()
            clear_all()
            register_penjual()
            return
  
        insert_query = """
        INSERT INTO pengguna (nama_pengguna, alamat_pengguna, no_telp_pengguna, username_pengguna, password_pengguna, role)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (nama, alamat, nomor_telepon, username, password, role))
        connection.commit()

        insert_query = """"
        INSERT INTO desa (nama_desa)
        VALUES (%s)
        """
        cursor.execute(insert_query, (desa,))
        connection.commit()

        insert_query = """"
        INSERT INTO kecamatan (nama_kecamatan)
        VALUES (%s)
        """
        cursor.execute(insert_query, (kecamatan,))
        connection.commit()

        insert_query = """"
        INSERT INTO desa (nama_kabupaten)
        VALUES (%s)
        """
        cursor.execute(insert_query, (kabupaten,))
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
        
        nama = input("Masukkan Nama Lengkap: ")
        alamat = input("Masukkan Alamat (nama jalan): ")
        nomor_telepon = input("Masukkan Nomor Telepon: ")
        desa = input("Masukkan Desa: ")
        kecamatan = input("Masukkan Kecamatan: ")
        kabupaten = input("Masukkan Kabupaten: ")
        username = input("Masukkan Username: ")
        password = input("Masukkan Password: ")
        role = "pembeli"  

        check_query = "SELECT username_pengguna FROM pengguna WHERE username_pengguna = %s"
        cursor.execute(check_query, (username,))
        check_user = cursor.fetchone()
        
        if check_user:
            print("\nUsername sudah terdaftar! Silahkan gunakan username lain.")
            input("Tekan Enter untuk melanjutkan...")
            cursor.close()
            connection.close()
            clear_all()
            register_pembeli()
            return
        
        insert_query = """
        INSERT INTO pengguna (nama_pengguna, alamat_pengguna, no_telp_pengguna, username_pengguna, password_pengguna, role)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (nama, alamat, nomor_telepon, username, password, role))
        connection.commit()

        insert_query = """"
        INSERT INTO desa (nama_desa)
        VALUES (%s)
        """
        cursor.execute(insert_query, (desa,))
        connection.commit()

        insert_query = """"
        INSERT INTO kecamatan (nama_kecamatan)
        VALUES (%s)
        """
        cursor.execute(insert_query, (kecamatan,))
        connection.commit()

        insert_query = """"
        INSERT INTO desa (nama_kabupaten)
        VALUES (%s)
        """
        cursor.execute(insert_query, (kabupaten,))
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

        username_pengguna = input("Masukkan Username : ")
        password_pengguna = input("Masukkan Password : ")

        check_query = """
        SELECT id_pengguna, nama_pengguna, role 
        FROM pengguna 
        WHERE username_pengguna = %s AND password_pengguna = %s
        """
        cursor.execute(check_query, (username_pengguna, password_pengguna))
        check_user = cursor.fetchone()
        
        if check_user:
            id_pengguna = check_user[0]
            nama_pengguna = check_user[1]
            role = check_user[2]
            print(f"\nLogin Berhasil!")
            print(f"Selamat datang {nama_pengguna}")
            print(f"Sebagai {role}")

            input("\nTekan Enter untuk melanjutkan...")
            cursor.close()
            connection.close()
            clear_all()

            if role == "admin":
                menu_admin(username_pengguna)
            elif role == "penjual":
                menu_penjual(username_pengguna)
            elif role == "pembeli":
                menu_pembeli(username_pengguna)
            else:
                print("Role tidak dikenali!")
                main_menu()
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
        main_menu()

# def kelola_produk():
#     clear_all()
#     connection = connect_db()
#     if connection is None:
#         print("Koneksi tidak berhasil")
#         return
    
#     try:
#         cursor = connection.cursor()


    






print(r'''
███████╗███████╗██╗      █████╗ ███╗   ███╗ █████╗ ████████╗
██╔════╝██╔════╝██║     ██╔══██╗████╗ ████║██╔══██╗╚══██╔══╝
███████╗█████╗  ██║     ███████║██╔████╔██║███████║   ██║   
╚════██║██╔══╝  ██║     ██╔══██║██║╚██╔╝██║██╔══██║   ██║   
███████║███████╗███████╗██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   
╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   
                                                            
██████╗  █████╗ ████████╗ █████╗ ███╗   ██╗ ██████╗         
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗████╗  ██║██╔════╝         
██║  ██║███████║   ██║   ███████║██╔██╗ ██║██║  ███╗        
██║  ██║██╔══██║   ██║   ██╔══██║██║╚██╗██║██║   ██║        
██████╔╝██║  ██║   ██║   ██║  ██║██║ ╚████║╚██████╔╝        
╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝                                
''')
input("Silahkan Tekan Enter Untuk Melanjutkan Ke Sistem")
clear_all()
main_menu()