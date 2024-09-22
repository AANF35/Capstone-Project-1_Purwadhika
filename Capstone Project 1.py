
# Fungsi untuk menyimpan data sehingga database tidak ter-reset ketika program dijalankan lagi (setelah program dihentikan)
import json
# Untuk menyimpan database
def Simpan_data(data_penyewa, data_mobil, List_RencanaSewa, filename="database_CP1.json"):
    # Simpan data ke dalam file
    with open(filename, "w") as f:
        json.dump({"penyewa": data_penyewa, "mobil": data_mobil, "keranjang": List_RencanaSewa}, f)

# Untuk memuat database ke dalam program
def Muat_data(filename="database_CP1.json"):
    # Muat data jika ada
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return data["penyewa"], data["mobil"]
    except FileNotFoundError:
        # Jika tidak ada data, return data kosong...
        print("Data tidak ditemukan, memulai dengan data kosong.")
        return {}, {}


# Database Awal
Data_Mobil = {
    "Daihatsu Xenia R 2019" : True,
    "Honda Brio RS 2020" : False,
    "Honda BRV Prestige 2023" : True,
    "Suzuki Ertiga GX 2022" : True,
    "Mitsubishi Xpander Ultimate 2022" : False,
    "Mitsubishi Pajero Sport 4x2 Dakar 2022" : True,
    "Toyota Avanza G 2022" : True,
    "Toyota Veloz Q 2022" : True,
    "Toyota Innova Venturer 2019" : False,
    "Toyota Fortuner VRZ 2017" : True
}

Data_Penyewa = {
    "Ahmad Azhar Naufal Farizky" : ["Toyota Innova Venturer 2019", "Mitsubishi Xpander Ultimate 2022"],
    "Aurellia Primata" : ["Honda Brio RS 2020"],
}

# List daftar rencana mobil yang akan disewa (sebagai keranjang)
List_RencanaSewa = []



## Untuk Menu "Sewa Mobil"

# Fungsi Pemilihan User di Main Menu
def Ops_MainMenu():
    # Input pilihan dan periksa input
    opsMainMenuPelanggan = input('Ketik Angka Pilihan : ')
    cond_opsMainMenuPelanggan = opsMainMenuPelanggan.isnumeric() and (int(opsMainMenuPelanggan) in [1,2,3,4])
    # Selama input salah, ulangi lagi permintaan input hingga sesuai
    while not cond_opsMainMenuPelanggan:        
        print("Input Salah!")
        opsMainMenuPelanggan = input('Ketik Angka Pilihan : ')
        cond_opsMainMenuPelanggan = opsMainMenuPelanggan.isnumeric() and (int(opsMainMenuPelanggan) in [1,2,3,4])
    return int(opsMainMenuPelanggan)


# Menu Cek Stok (Read Data_Mobil)
def CekStokPelanggan(data):
    while True:
        print("=" * 80)
        print(f"{'Unit Mobil':<50} {'Ketersediaan':<15}")
        print("=" * 80)
        for Mobil, Tersedia in data.items():
            if Tersedia:
                Ketersediaan_tabel = "Ada"
            else:
                Ketersediaan_tabel = "Tidak (Sedang Disewa)"
            print(f"{Mobil:<50} {Ketersediaan_tabel:<15}")
        print("=" * 80)
        input("Ketik apapun untuk kembali : ")
        break


# Read/Display Mobil yang masih tersedia di dalam subMenu MainMenu
def Read_MobilTersedia(data):
    List_MobilTersedia = [Mobil for Mobil, Tersedia in data.items() if Tersedia]    
    print("=" * 50)
    print(f"{'No.':<5} {'Unit Mobil':<50}")
    print("=" * 50)    
    for Mobil in List_MobilTersedia:
        print(f"{List_MobilTersedia.index(Mobil)+1:<5} {Mobil:<50}")    
    print("=" * 50)    

# Read/Display Mobil yang ada di dalam List_RencanaSewa (ketika Pelanggan telah menambahkan mobil untuk pertama kalinya)
def Read_RencanaSewaMobil(List_RencanaSewa):
    if len(List_RencanaSewa) > 0:
        print("=" * 50)
        print(f"{'No.':<5} {'Rencana Sewa':<45}")
        print("=" * 50)
        for Mobil in List_RencanaSewa:
            print(f"{List_RencanaSewa.index(Mobil) + 1:<5} {Mobil:<45}")
        print("=" * 50)


# Menu Aksi di dalam SewaPelanggan()
def Ops_AksiSewaPelanggan(List_MobilTersedia, List_RencanaSewa):
    while True:
        # Display mobil yang ada dalam list rencana sewa
        Read_RencanaSewaMobil(List_RencanaSewa)
        # Display Semua Aksi yang dapat dilakukan Pelanggan
        List_Aksi = ["Sewa/Tambah Mobil", "Ganti Mobil", "Hapus Mobil", "Proses Penyewaan", "(Kembali)"]
        print("=" * 80)
        print("Pilih aksi :")
        for Aksi in List_Aksi:
            print(f"{List_Aksi.index(Aksi)+1}. {Aksi}")    
        print("=" * 80)

        # Meminta input dan memeriksa input harus benar-benar sesuai
        opsAksi = input("Masukkan Angka Aksi : ")
        cond_opsAksi = opsAksi.isnumeric() and int(opsAksi) in [1,2,3,4,5]
        while not cond_opsAksi:
            opsAksi = input("Masukkan Angka Aksi : ")
            cond_opsAksi = opsAksi.isnumeric() and int(opsAksi) in [1,2,3,4,5]
                
        # Kasus pelanggan belum menambahkan mobil sama sekali ke rencana sewa        
        if len(List_RencanaSewa) == 0 and (int(opsAksi) in [2,3,4]):
            print("Anda belum menambahkan mobil sama sekali")
        # Kasus tidak ada mobil tersedia yang dapat disewa (semua mobil tersedia telah masuk ke dalam rencana sewa)
        elif len(List_MobilTersedia) == 0 and (int(opsAksi) == 1):
            print("Tidak ada mobil yang dapat disewa")        
        else:
            break
    return int(opsAksi)
            
    
# Fungsi Create + Update: menambahkan mobil terpilih ke dalam list rencana sewa, 
# mengupdate database sehingga mobil terpilih tidak tersedia (sementara hingga dihapus/diganti)
def AddPilihMobil(List_MobilTersedia, List_RencanaSewa, data_mobil, opsPilihMobil):
    # Tambah mobil terpilih ke dalam list rencana sewa
    Mobil = List_MobilTersedia[opsPilihMobil - 1]
    List_RencanaSewa.append(Mobil)

    # Update database sehingga mobil terpilih tidak tersedia
    data_mobil[Mobil] = False

    # Informasi mobil berhasil dimasukkan ke dalam daftar rencana sewa
    print(f"Anda berhasil menambahkan {Mobil} ke dalam rencana sewa")


# Fungsi Ketika Pelanggan memilih Sewa/Tambah (dalam fungsi SewaPelanggan())
def Ops_AddPilihMobil(List_RencanaSewa, data_mobil):
    # Update list mobil tersedia (melalui database)
    List_MobilTersedia = [Mobil for Mobil, Tersedia in data_mobil.items() if Tersedia]
    
    # Display semua mobil tersedia
    Read_MobilTersedia(data_mobil)
    
    # Meminta input pilihan mobil dari list mobil tersedia (input harus sesuai)
    opsPilihMobil = input("Masukkan Nomor Mobil dari Pilihan di atas : ")
    cond_opsPilihMobil = opsPilihMobil.isnumeric() and (int(opsPilihMobil) in range(1, len(List_MobilTersedia) + 1))    
    while not cond_opsPilihMobil:
        print("Input Salah!")
        opsPilihMobil = input("Masukkan Nomor Mobil dari Pilihan di atas : ")
        cond_opsPilihMobil = opsPilihMobil.isnumeric() and (int(opsPilihMobil) in range(1, len(List_MobilTersedia) + 1))
    
    # Tambahkan mobil dalam daftar rencana sewa
    opsPilihMobil = int(opsPilihMobil)
    AddPilihMobil(List_MobilTersedia, List_RencanaSewa, data_mobil, opsPilihMobil)


# Read daftar rencana sewa
def Read_RencanaSewa(List_RencanaSewa):
    print("=" * 80)
    for Mobil in List_RencanaSewa:
        print(f"{List_RencanaSewa.index(Mobil)+1}. {Mobil}")
    print("=" * 80)


# Fungsi menukar mobil dari daftar rencana sewa
def ReplacePilihMobil(List_MobilTersedia, List_RencanaSewa, data_mobil, opsPilihMobil_1, opsPilihMobil_2):    
    # Select kedua mobil yang ingin ditukar
    Mobil_awal = List_RencanaSewa[opsPilihMobil_1 - 1]    
    Mobil_tukar = List_MobilTersedia[opsPilihMobil_2 - 1]

    # Ganti mobil dalam daftar rencanan sewa
    List_RencanaSewa[opsPilihMobil_1 - 1] = Mobil_tukar

    # Tukar kondisi ketersediaan dalam database, update list mobil tersedia dari database, dan konfirmasi
    data_mobil[Mobil_awal] = True
    data_mobil[Mobil_tukar] = False            
    List_MobilTersedia = [Mobil for Mobil, Tersedia in data_mobil.items() if Tersedia]
    print(f"{Mobil_awal} berhasil diganti dengan {Mobil_tukar} dalam rencana sewa")    
    
    # Update list mobil tersedia dari database
    List_MobilTersedia = [Mobil for Mobil, Tersedia in data_mobil.items() if Tersedia]


# Menu menukar mobil dalam Menu SewaPelanggan()
def Ops_ReplacePilihMobil(List_MobilTersedia, List_RencanaSewa, data_mobil):
    # Display mobil yang sebelumnya telah masuk dalam list rencana sewa
    Read_RencanaSewa(List_RencanaSewa)
    
    # Minta input mobil yang ingin diganti (input harus sesuai)
    opsPilihMobil_1 = input("Pilih nomor mobil yang akan diganti : ")
    cond_opsPilihMobil_1 = opsPilihMobil_1.isnumeric() and (int(opsPilihMobil_1) in range(1, len(List_RencanaSewa)+1))
    while not cond_opsPilihMobil_1:
        print("Input Salah!")
        opsPilihMobil_1 = input("Pilih nomor mobil yang akan diganti : ")
        cond_opsPilihMobil_1 = opsPilihMobil_1.isnumeric() and (int(opsPilihMobil_1) in range(1, len(List_RencanaSewa)+1))

    # Display mobil yang tersedia
    Read_MobilTersedia(data_mobil)

    # Minta input mobil yang ingin ditukarkan (input harus sesuai)
    opsPilihMobil_2 = input("Pilih nomor mobil yang menggantikan : ")
    cond_opsPilihMobil_2 = opsPilihMobil_2.isnumeric() and (int(opsPilihMobil_2) in range(1, len(List_MobilTersedia)+1))
    while not cond_opsPilihMobil_2:
        print("Input Salah!")
        opsPilihMobil_2 = input("Pilih nomor mobil yang menggantikan : ")
        cond_opsPilihMobil_2 = opsPilihMobil_2.isnumeric() and (int(opsPilihMobil_2) in range(1, len(List_MobilTersedia)+1))
    
    # Casting input pilihan mobil yang akan ditukar dalam daftar rencana sewa
    opsPilihMobil_1 = int(opsPilihMobil_1)
    opsPilihMobil_2 = int(opsPilihMobil_2)

    # Tukar kedua mobil
    ReplacePilihMobil(List_MobilTersedia, List_RencanaSewa, data_mobil, opsPilihMobil_1, opsPilihMobil_2)
        

# Fungsi untuk mengapus mobil terpilih dari list rencana sewa
def DeletePilihMobil(List_RencanaSewa, data_mobil, opsDeleteMobil):    
    # Hapus mobil terpilih dari list rencana sewa
    Mobil = List_RencanaSewa[opsDeleteMobil - 1]    
    List_RencanaSewa.remove(Mobil)    

    # Update database sehingga mobil terpilih tersedia kembali di database
    data_mobil[Mobil] = True

    # Informasi mobil berhasil dihapus dari daftar rencana sewa
    print(f"Anda berhasil menghapus {Mobil} dari rencana sewa")


# Menu menghapus mobil dari daftar rencana sewa
def Ops_DeletePilihMobil(List_RencanaSewa,data_mobil):
    # Display mobil yang sebelumnya telah masuk dalam list rencana sewa
    Read_RencanaSewa(List_RencanaSewa)
    
    # Minta input mobil yang ingin diganti (input harus sesuai)
    opsDeleteMobil = input("Pilih nomor mobil yang akan dihapus : ")
    cond_opsDeleteMobil = opsDeleteMobil.isnumeric() and (int(opsDeleteMobil) in range(1, len(List_RencanaSewa)+1))
    while not cond_opsDeleteMobil:
        print("Input Salah!")
        opsDeleteMobil = input("Pilih nomor mobil yang akan dihapus : ")
        cond_opsDeleteMobil = opsDeleteMobil.isnumeric() and (int(opsDeleteMobil) in range(1, len(List_RencanaSewa)+1))

    # Casting opsi dan hapus mobil dari rencana daftar sewa
    opsDeleteMobil = int(opsDeleteMobil)
    DeletePilihMobil(List_RencanaSewa, data_mobil, opsDeleteMobil)    


# Fungsi untuk memeriksa apakah penyewa masih memiliki mobil yang sedang dipinjam
def Periksa_Penyewa(Nama_Penyewa, data_penyewa):
    if Nama_Penyewa.title() in data_penyewa.keys():
        print(f"Terdapat mobil yang masih sedang Anda sewa atas nama {Nama_Penyewa.title()}. Apakah Anda ingin tetap melanjutkan sewa?")
        opsConfirm = str(input("Ketik (T) untuk melanjutkan atau (F) untuk (kembali) : "))
        cond_opsConfirm = opsConfirm.upper() == "T" or opsConfirm.upper() == "F"
        while not cond_opsConfirm:
            opsConfirm = str(input("Ketik (T) untuk melanjutkan atau (F) untuk (kembali) : "))
            cond_opsConfirm = opsConfirm.upper() == "T" or opsConfirm.upper() == "F"
        # Return berupa "T", "F", atau None
        return opsConfirm
    

# Fungsi untuk menambahkan nama penyewa/pelanggan dan daftar mobil yang disewa ke dalam database
def Add_DaftarPelanggan(Nama_Penyewa, data_penyewa, List_RencanaSewa):
    # Jika penyewa belum menyewa sama sekali
    if Nama_Penyewa not in data_penyewa.keys():        
        data_penyewa[Nama_Penyewa] = []
        data_penyewa[Nama_Penyewa].extend(List_RencanaSewa)
    # Jika penyewa pernah menyewa dan masih terdapat mobil yang sedang disewa
    elif Nama_Penyewa in data_penyewa.keys():
        data_penyewa[Nama_Penyewa].extend(List_RencanaSewa)
    
    # Menghapus daftar rencana sewa (karena telah masuk dalam database)
    List_RencanaSewa.clear()


# Menu melanjutkan proses sewa dalam Menu SewaPelanggan()
def Ops_ProceedSewa(List_RencanaSewa, data_penyewa):    
    while True:
        # Meminta input nama penyewa (non-case sensitive)
        Nama_Penyewa = str(input("Masukkan nama Anda : "))

        # Periksa apakah pelanggan pernah meminjam sebelumnya dan terdapat mobil yang masih sedang disewa
        opsConfirm_1 = Periksa_Penyewa(Nama_Penyewa, data_penyewa)
        # Jika pelanggan batal menyewa setelah diberitahu bahwa pelanggan masih sedang menyewa suatu/beberapa mobil
        if opsConfirm_1 == "F":
            return "F"

        # Display kembali daftar rencana sewa sebagai pilihan final
        Read_RencanaSewa(List_RencanaSewa)

        # Meminta input konfirmasi penyewaan (input harus sesuai)
        print(f"Apakah Anda yakin untuk menyewa semua mobil pada daftar rencana sewa atas nama {Nama_Penyewa.title()}?")
        opsProceed = str(input("Ketik (T) untuk lanjut menyewa atau (F) untuk (kembali) : "))
        cond_opsProceed = opsProceed.upper() == "T" or opsProceed.upper() == "F"
        while not cond_opsProceed:
            opsProceed = str(input("Ketik (T) untuk lanjut menyewa atau (F) untuk (kembali) : "))
            cond_opsProceed = opsProceed.upper() == "T" or opsProceed.upper() == "F"
                
        # Jika pelanggan batal melanjutkan sewa
        if opsProceed == "F":
            return "F"
        else:
            # Memasukkan List_RencanaSewa dan Nama_Penyewa ke Data_Penyewa
            Add_DaftarPelanggan(Nama_Penyewa, data_penyewa, List_RencanaSewa)            

            # Konfirmasi sewa telah berhasil dilakukan
            print("=" * 80)
            print("Sewa telah berhasil dilakukan. Selamat menikmati mobil sewaan kami :)")
            print("=" * 80)
                        
            return "T"    



# Menu Sewa (ketika pelanggan ingin menyewa)
def SewaPelanggan():    
    while True:    
        List_MobilTersedia = [Mobil for Mobil, Tersedia in Data_Mobil.items() if Tersedia]
        # Opsi User untuk menambah, mengganti, menghapus mobil dari list rencana sewa, atau kembali ke menu        
        opsAksi = Ops_AksiSewaPelanggan(List_MobilTersedia, List_RencanaSewa)
        if opsAksi == 1:            
            Ops_AddPilihMobil(List_RencanaSewa, Data_Mobil)            
            continue
        elif opsAksi == 2:            
            Ops_ReplacePilihMobil(List_MobilTersedia, List_RencanaSewa, Data_Mobil)
            continue
        elif opsAksi == 3:
            Ops_DeletePilihMobil(List_MobilTersedia, List_RencanaSewa, Data_Mobil)
            continue
        elif opsAksi == 4:
            Proceed = Ops_ProceedSewa(List_RencanaSewa, Data_Penyewa)
            if Proceed == "F":
                continue
            elif Proceed == "T":                
                break
        elif opsAksi == 5:
            break                    
    




## Untuk Menu "Mengembalikan Mobil "

# Fungsi untuk memeriksa apakah nama penyewa ada di dalam database
def Periksa_DaftarPenyewa(data_penyewa):
    while True:
        # Meminta input nama penyewa (input harus sesuai)
        Nama_Penyewa = str(input("Masukkan nama yang Anda gunakan pada saat menyewa atau ketik (#99) untuk (kembali) : "))        
        cond_Nama_Penyewa = Nama_Penyewa.title() in data_penyewa or Nama_Penyewa == "#99"
        while not cond_Nama_Penyewa:
            print("Nama tidak ada di dalam daftar penyewa kami.")
            Nama_Penyewa = str(input("Silahkan coba lagi atau ketik (#99) untuk (kembali) : "))        
            cond_Nama_Penyewa = Nama_Penyewa.title() in data_penyewa or Nama_Penyewa == "#99"
        
        # Jika diputuskan untuk kembali ke Main Menu (baik karena nama tidak ada dalam daftar penyewa maupun bukan)
        if Nama_Penyewa == "#99":
            return "F"
        # Jika nama ada
        else:
            return Nama_Penyewa.title()
            

# Fungsi Read untuk display semua mobil yang sedang disewa
def Read_PinjamanPenyewa(List_MobilDisewa):
    print("=" * 80)
    print(f"{'No.':<5} {'Mobil yang sedang dipinjam':<50}")
    print("=" * 80)
    for Mobil in List_MobilDisewa:
        print(f"{List_MobilDisewa.index(Mobil)+1:<5} {Mobil:<50}")   
    print(f"{len(List_MobilDisewa)+1:<5} {'(Kembali ke Main Menu)':<50}") 
    print("=" * 80)


# Fungsi Read untuk display semua mobil di dalam daftar rencana pengembalian
def Read_RencanaPengembalian(List_RencanaPengembalian):
    print("=" * 80)
    print("=" * 80)
    print(f"{'No.':<5} {'Mobil dalam Daftar Rencana Pengembalian':<50}")
    print("=" * 80)
    for Mobil in List_RencanaPengembalian:
        print(f"{List_RencanaPengembalian.index(Mobil)+1:<5} {Mobil:<50}")    
    print("=" * 80)


# Fungsi Create dan Delete untuk menambahkan mobil ke dalam daftar rencana pengembalian
def Add_PengembalianMobil(List_MobilDisewa_Temp, List_RencanaPengembalian, Mobil):
    # Tambahkan mobil terpilih ke daftar rencana pengembalian    
    List_RencanaPengembalian.append(Mobil)

    # Update List_MobilDisewa sehingga mobil terpilih sebelumnya tidak ditampilkan kembali
    List_MobilDisewa_Temp.remove(Mobil)    

    # Display konfirmasi mobil berhasil ditambahkan ke daftar rencana pengembalian
    print(f"{Mobil} berhasil ditambahkan ke daftar pengembalian mobil")

    return List_RencanaPengembalian, List_MobilDisewa_Temp


# Menu Konfirmasi dalam Menu ReturnPelanggan() 
def Confirm_ReturnMobil(List_MobilDisewa_Temp, List_RencanaPengembalian, data_penyewa, data_mobil, Nama_Penyewa):
    while True:    
        # Konfirmasi apakah penyewa yakin mengembalikan semua mobil tersebut (input harus sesuai)
        print("Apakah Anda yakin untuk mengembalikan semua mobil tersebut?")
        opsConfirmReturn = str(input("Ketik (T) jika yakin atau (F) untuk tidak : "))
        cond_opsConfirmReturn = opsConfirmReturn.upper() == "T" or opsConfirmReturn.upper() == "F"
        while not cond_opsConfirmReturn:
            opsConfirmReturn = str(input("Ketik (T) jika yakin atau (F) untuk tidak : "))
            cond_opsConfirmReturn = opsConfirmReturn.upper() == "T" or opsConfirmReturn.upper() == "F"

        if opsConfirmReturn.upper() == "F":
            return "F"
        elif opsConfirmReturn.upper() == "T":
            # Hapus semua mobil terkembalikan dalam Data_Penyewa dab update Data_Mobil sehingga mobil tersedia kembali untuk disewa
            for Mobil in List_RencanaPengembalian:
                data_mobil[Mobil] = True
                data_penyewa[Nama_Penyewa].remove(Mobil)                

            # Jika masih terdapat mobil yang sedang dipinjam dan belum dikembalikan, display notifikasi
            if len(List_MobilDisewa_Temp) > 0:                
                print("=" * 80)
                print("Masih terdapat mobil yang Anda pinjam. Selamat melanjutkan penyewaan dan jangan lupa mengembalikannya!")
            # Jika sudah tidak ada lagi,
            else:
                # Display notifikasi dan hapus seluruh data terkait dalam Data_Penyewa
                print("=" * 80)
                print("Semua mobil Anda telah dikembalikan. Terima kasih telah menyewa mobil kami :)")
                data_penyewa.pop(Nama_Penyewa)

            # Hapus semua data sementara List_MobilDisewa_Temp
            List_MobilDisewa_Temp.clear()            

            return "T"
                        

# Menu "Mengembalikan Mobil" setelah konfirmasi adanya nama penyewa di dalam database Data_Penyewa
def ReturnPelanggan(Nama_Penyewa, data_penyewa, data_mobil):
    List_RencanaPengembalian = []
    List_MobilDisewa_Temp = [Mobil for Mobil in data_penyewa[Nama_Penyewa.title()]]              
    while True:
        # Selama terdapat setidaknya satu mobil yang sedang dipinjam...
        if len(List_MobilDisewa_Temp) > 0:
            # Display semua mobil yang sedang disewa (daftar mobil disewa)
            Read_PinjamanPenyewa(List_MobilDisewa_Temp)

            # Ketika terdapat mobil yang berhasil ditambahkan sebelumnya ke daftar rencana pengembalian, display juga mobil tersebut
            if len(List_RencanaPengembalian) > 0:
                Read_RencanaPengembalian(List_RencanaPengembalian)
            
            # Meminta input pilihan mobil yang ingin dikembalikan (input harus sesuai) 
            opsReturnMobil = input("Masukkan nomor mobil yang sedang dipinjam dan ingin dikembalikan : ")
            cond_opsReturnMobil = opsReturnMobil.isnumeric() and (int(opsReturnMobil) in range(1, (len(List_MobilDisewa_Temp) + 1) + 1))
            while not cond_opsReturnMobil:
                print("Input Salah!")
                opsReturnMobil = input("Masukkan nomor mobil yang sedang dipinjam dan ingin dikembalikan : ")
                cond_opsReturnMobil = opsReturnMobil.isnumeric() and (int(opsReturnMobil) in range(1, (len(List_MobilDisewa_Temp) + 1) + 1))
            opsReturnMobil = int(opsReturnMobil)

            # Jika batal untuk mengembalikan, pergi kembali ke Main Menu
            if opsReturnMobil == (len(List_MobilDisewa_Temp) + 1):
                break
            else:
                # Tanyakan apakah penyewa yakin mobil terpilih ingin dimasukkan dalam daftar pengembalian mobil (input harus sesuai)
                Mobil = List_MobilDisewa_Temp[opsReturnMobil - 1]
                print(f"Apakah Anda yakin untuk memasukkan {Mobil} ke daftar pengembalian mobil?")
                opsConfirmAddReturn = str(input("Ketik (T) jika yakin atau (F) untuk tidak : "))
                cond_opsConfirmAddReturn = opsConfirmAddReturn.upper() == "T" or opsConfirmAddReturn.upper() == "F"
                while not cond_opsConfirmAddReturn:
                    opsConfirmAddReturn = str(input("Ketik (T) jika yakin atau (F) untuk tidak : "))
                    cond_opsConfirmAddReturn = opsConfirmAddReturn.upper() == "T" or opsConfirmAddReturn.upper() == "F"
                
                # Jika tidak, kembali ke Menu ReturnPelanggan()
                if opsConfirmAddReturn.upper() == "F":
                    continue
                # Jika yakin,
                elif opsConfirmAddReturn.upper() == "T":
                    # Tambahkan mobil terpilih ke daftar rencana dan konfirmasi
                    List_RencanaPengembalian, List_MobilDisewa_Temp = Add_PengembalianMobil(List_MobilDisewa_Temp, List_RencanaPengembalian, Mobil) 

                    # Display daftar pengembalian mobil yang diperbarui
                    Read_RencanaPengembalian(List_RencanaPengembalian)

                    # Selama masih ada mobil di dalam Daftar_Penyewa
                    if len(List_MobilDisewa_Temp) > 0:
                        # Tanyakan apakah ada mobil lain yang ingin dikembalikan (input harus sesuai)
                        print("Apakah ada mobil lain yang ingin dikembalikan?")
                        opsAddReturnMobil = str(input("Ketik (T) untuk menambahkan atau (F) untuk tidak : "))
                        cond_opsAddReturnMobil = opsAddReturnMobil.upper() == "T" or opsAddReturnMobil.upper() == "F"
                        while not cond_opsAddReturnMobil:
                            opsAddReturnMobil = str(input("Ketik (T) untuk menambahkan atau (F) untuk tidak : "))
                            cond_opsAddReturnMobil = opsAddReturnMobil.upper() == "T" or opsAddReturnMobil.upper() == "F"

                        # Jika ada mobil yang ingin dikembalikan lagi, kembali ke Menu ReturnPelanggan()
                        if opsAddReturnMobil.upper() == "T":
                            continue
                        # Jika tidak, pergi ke Menu Confirm_ReturnMobil()
                        elif opsAddReturnMobil.upper() == "F":
                            confirmReturn = Confirm_ReturnMobil(List_MobilDisewa_Temp, List_RencanaPengembalian, data_penyewa, data_mobil, Nama_Penyewa)
                            if confirmReturn.upper() == "F":
                                continue
                            elif confirmReturn.upper() == "T":
                                break
                    
                    # Jika semua mobil telah masuk ke dalam daftar rencana pengembalian
                    else:
                        confirmReturn = Confirm_ReturnMobil(List_MobilDisewa_Temp, List_RencanaPengembalian, data_penyewa, data_mobil, Nama_Penyewa)
                        if confirmReturn.upper() == "F":
                            continue
                        elif confirmReturn.upper() == "T":
                            break        
        else:        
            break
        

# Main Menu
def MainMenuPelanggan():
    # Muat data dari file database
    global Data_Penyewa, Data_Mobil
    Data_Penyewa, Data_Mobil = Muat_data(filename="database_CP1.json")

    while True:
        print("=" * 75)
        print('Selamat datang di SewaMobil.AANF, Pelanggan! \nPilih Menu: \n1. Cek Stok Mobil \n2. Sewa Mobil \n3. Mengembalikan Mobil \n4. (Keluar)')
        print("=" * 75)
        
        # Input Pelanggan untuk keempat menu selanjutnya
        opsMainMenuPelanggan = Ops_MainMenu()
        # Memeriksa Stok Mobil yang tersedia untuk disewa (dari semua mobil yang dimiliki)
        if opsMainMenuPelanggan == 1:
            CekStokPelanggan(Data_Mobil)
        # Menyewa Mobil
        elif opsMainMenuPelanggan == 2:            
            SewaPelanggan()
        # Mengembalikan Sewaan Mobil
        elif opsMainMenuPelanggan == 3:            
            # Periksa terlebih dahulu apakah nama pelanggan terdaftar dalam data
            Nama_Penyewa = Periksa_DaftarPenyewa(Data_Penyewa)
            # Jika ada, lanjutkan ke menu pengembalian            
            if Nama_Penyewa != "F":
                ReturnPelanggan(Nama_Penyewa, Data_Penyewa, Data_Mobil)
        # Keluar dari Aplikasi
        elif opsMainMenuPelanggan == 4:
            # Simpan data terlebih dahulu
            Simpan_data(Data_Penyewa, Data_Mobil, List_RencanaSewa)
            print("Sampai jumpa lagi...")    
            break


# Main Program
MainMenuPelanggan()