import threading  # mengimport modul threading
import time       # mengimport modul time
class PeriodicTimer:    # membuat class PeriodicTimer
    def __init__(self, interval): # fungsi class __init__ sebagai konstraktor dengan self sebagai instant/objek yang dapat diakses dan insterval sebagai argument
        self.interval = interval # mengakses variabel interval dengan menggunakan self 
        self.flag = 0  # mengakses variabel flag dengan menggunakan self 
        self.cv = threading.Condition() # membuat variabel cv dengan fungsi threading.condition yang memungkinkan satu atau lebih thread menunggu hingga diberi tahu oleh thread lain. 
    def start(self): # fungsi class Start dengan self sebagai instant/objek yang dapat diakses
        t = threading.Thread(target=self.run)   # variabel t dengan fungsi theading.Thread untuk memanggil target self.run
        t.daemon = True # membuat ketentuan daemon pada variabel t yang menggunakan fungsi theading.Thread
        t.start()   # t dengan fungsi start
    def run(self):  # fungsi class run dengan self sebagai instant/objek yang dapat diakses
        ''' menjalankan timer dan notif thread setelah interval '''
        while True:
            time.sleep(self.interval)   # menjalan timer dan notif setalah interval
            with self.cv:   # dengan ketentuan cv 
                self.flag ^= 1 # pada variabel flag dimulai dari 1
                self.cv.notify_all()    # method notify_all membangunkan semua thread yang menunggu variabel kondisi. 

    def menunggu_waktu(self): # fungsi class menunggu_waktu dengan self sebagai instant/objek yang dapat diakses
        ''' menunggu pengaturan waktu selanjutnya '''
        with self.cv:  # dengan ketentuan cv 
            last_flag = self.flag # menentukan last_flag = self.flag
            while last_flag == self.flag: # ketika lask_flag = self.flag
                self.cv.wait() # self.cv dengan method wait akan menunggu hingga evaluasi kondisi sudah benar


ptimer = PeriodicTimer(5) # memanggil class periodictimer
ptimer.start()  #method mulai class

# Two threads that synchronize on the timer
def countdown(n): # fungsi countdown untuk hitung mundur
    while n > 0: # ketika n > 0 maka
        ptimer.menunggu_waktu() # objek ptimer akan menjalankan fungsi "menunggu_waktu"
        print('waktu', n) # lalu menprint "waktu"
        n -= 1 # dengan n - 1

def countup(last): # fungsi countup untuk hitung maju
    n = 0 
    while n < last: # ketika n < last
        ptimer.menunggu_waktu() # objek ptimer akan menjalankan fungsi "menunggu_waktu"
        print('menghitung', n) # lalu menprint "menghitung" dengan jumlah n
        n += 1 # dengan n + 1

threading.Thread(target=countdown, args=(10,)).start()  # menjalankan fungsi countdown dengan menggunkan theading.Thread
threading.Thread(target=countup, args=(10,)).start() # menjalankan fungsi countup dengan menggunkan theading.Thread

