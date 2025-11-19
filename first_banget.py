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
            register()
        elif select_menu == "2":
            login()
        else :
            print("Pilihan Tidak Ditemukan")
            main_menu()
    return


def register():
    print('''=== Silahkan memilih tipe pelaku ===
          1. Petani
          2. UMKM
          3. Pelanggan
''')
    tipe_pelaku = input("Pilih Tipe Pelaku (1/2/3) : ")
    while True :
        if tipe_pelaku == "1":
            register_petani()
        elif tipe_pelaku == "2":
            register_umkm()
        elif tipe_pelaku == "3":
            register_pelanggan()
        else:
            print("Pilihan tidak tersedia")
            register()
        return


def register_petani():
    os.system('cls')
    connection = connect_db()
    if connection is None:
        print ("Koneksi tidak berhasil")
        return

    print('''=== SYARAT REGISTER ===
          1. Contoh Alamat : jalan cahaya 14
          2. Contoh Username : yareuu45
          3. Contoh Password : 1234
''')
    nama = input("Masukkan Nama : ").title()
    alamat = input("Masukkan Alamat (ct. jalan cahaya 14) : ").title()
    kontak = int(input("Masukkan Nomor HP (ct. 081234567) : "))
    usia = int(input("Masukkan Usia (ct. 35): "))
    username = input("Buat Username (huruf & angka): ").lower()
    password_penjual = input("Buat Password (4 angka) : ")
    if not password_penjual.isdigit():
        print("Password bukan angka")
    elif len(password_penjual) < 4:
        print("Password kurang dari 4 angka. Silahkan membuat password lagi")
    elif len(password_penjual) > 4:
        print("Password lebih dari 4 angka. Silahkan membuat password lagi")
    elif len(password_penjual) == 4:
        print("Registrasi petani berhasil!")
    else:
        print("Password tidak sesuai")
        
    return{
        "nama" : nama,
        "alamat" : alamat,
        "kontak" : kontak,
        "usia" : usia,
        "username" : username
    }

    try:
        cursor = connection.cursor()

        data_petani = """
        INSERT INTO penjual 
        (nama, alamat, kontak, usia, tipe_pelaku, username, password_penjual)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s)
"""                      
        data = (nama, alamat, kontak, usia, "Petani", username, password_penjual)
        cursor.execute(data_petani, data)

        connection.commit()
        print("---Selamat Anda Telah Terdaftar Sebagai Petani di ENTROPIN---")

    except Exception as error:
        print("Telah Terjadi Kesalahan", error)
    
    finally:
        cursor.close()
        connection.close()

def register_umkm():
    nama = input("Masukkan Nama: ")
    alamat = input("Masukkan Alamat: ")
    kontak = input("Masukkan Nomor HP: ")
    username = input("Buat Username: ")
    password = input("Buat Password: ")
    print("Registrasi UMKM berhasil!")

def register_pelanggan():
    nama = input("Masukkan Nama: ")
    alamat = input("Masukkan Alamat: ")
    kontak = input("Masukkan Nomor HP: ")
    username = input("Buat Username: ")
    password = input("Buat Password: ")
    print("Registrasi Pelanggan berhasil!")


def login():
     print('''=== Silahkan memilih tipe pelaku ===
          1. Petani
          2. UMKM
          3. Pelanggan
          4. Admin Gudang
''')
     login_akun = input("Silahkan Pilih Tipe Pelaku (1/2/3/4) : ")
     if login_akun == "4":
         login_admin()

def login_admin():
    user_admin = "Adminentropin"
    pw_admin = "entropinkeren"
    
    while True:
        user_admin = input("Masukkan Username Admin : ").capitalize()
        if user_admin != "Adminentropin":
            print("Username Anda Salah")
            continue
        
        while True:
            pw_admin = input("Masukkan Password Admin : ").lower()
            if pw_admin != "entropinkeren":
                print("Password Anda Salah")
                continue
            elif pw_admin == "entropinkeren":
                print(f"Username Anda : {user_admin}")
                print(f"Password Anda : {pw_admin}")
                print("Selamat Anda Telah Berhasil Login")
            return
        
         

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
main_menu()