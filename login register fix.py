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
            database = "entropin_final"
        )
        return connection
    except Error as error:
        print("Terjadi kesalahan, gagal terkoneksi dengan database", error)

def clear_all():
    os.system('cls')

def next():
    kembali = input("Silahkan Tekan Enter Untuk Lanjut")
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
        
        while True:
            nama = input('Nama Lengkap: ').strip()
            if nama == '':
                print('\nNama tidak boleh kosong')
                next()
                continue
            else:
                next()
                break
        while True:
            alamat = input('Nama Jalan(ct. jalan jawa): ').strip()
            if alamat == '':
                print('\nNama jalan tidak boleh kosong')
                next()
                continue
            else:
                next()
                break
        while True:
            print(''' ===== DATA NAMA DESA =====
                1. desa sumberagung
                2. desa sidomulyo
                3. desa karangrejo
                4. desa wonorejo
                5. desa purwosari
                ''')
            desa = input('Nama Desa: ').strip()
            if desa == '':
                print('\nNama desa tidak boleh kosong')
                next()
                continue
            
            cursor.execute("SELECT id_desa FROM desa WHERE nama_desa = %s", (desa,))
            data_desa = cursor.fetchone()
            if data_desa is None:
                print('\nNama desa tidak ditemukan. Harap masukkan nama desa sesuai data')
                next()
                continue
            elif data_desa is not None:
                id_desa = data_desa[0]
                next()
                break
        while True:
            nomor_telepon = input('Nomor Telepon: ').strip()
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
            username = input('Username (5-15 karakter): ').strip()
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
            password = input('Password (5-15 karakter): ').strip()
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
        INSERT INTO pengguna (nama_pengguna, alamat_pengguna, no_telp_pengguna, username_pengguna, password_pengguna, role, id_desa)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (nama, alamat, nomor_telepon, username, password, role, id_desa))
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
            alamat = input('Nama Jalan (ct. jalan jawa) : ').strip()
            if alamat == '':
                print('\nNama jalan tidak boleh kosong')
                next()
                continue
            else:
                next()
                break
        while True:
            print(''' ===== DATA NAMA DESA =====
                1. desa sumberagung
                2. desa sidomulyo
                3. desa karangrejo
                4. desa wonorejo
                5. desa purwosari
                ''')
            desa = input('Nama Desa : ').strip()
            if desa == '':
                print('\nNama desa tidak boleh kosong')
                next()
                continue
            
            cursor.execute("SELECT id_desa FROM desa WHERE nama_desa = %s", (desa,))
            data_desa = cursor.fetchone()
            if data_desa is None:
                print('\nNama desa tidak ditemukan. Harap masukkan nama desa sesuai data')
                next()
                continue
            elif data_desa is not None:
                id_desa = data_desa[0]
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
        INSERT INTO pengguna (nama_pengguna, alamat_pengguna, no_telp_pengguna, username_pengguna, password_pengguna, role, id_desa)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (nama, alamat, nomor_telepon, username, password, role, id_desa))
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

        if username == "adminentropin" and password == "entropin":
            print("\nLogin berhasil sebagai ADMIN!")
            input("Tekan Enter...")
            cursor.close()
            connection.close()
            clear_all()
            menu_admin(username)
            return

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

            input("\nTekan Enter untuk melanjutkan...")
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
        main_menu()

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