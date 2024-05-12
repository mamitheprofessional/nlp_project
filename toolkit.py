import tkinter as tk
from tkinter import messagebox
import Levenshtein
from textblob import TextBlob
from nltk.tokenize import word_tokenize
import string
from collections import Counter
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

import nltk
nltk.download('punkt')  # "punkt" dosyası önceden eğitilmiş bir dil modeli, cümle ve kelimeleri tokenleştirmeye yarıyor


class MetinAnaliz:
    @staticmethod
    def duygu_analiz(metin):
        if metin:
            duygu = TextBlob(metin).sentiment
            return duygu.polarity, duygu.subjectivity
        else:
            return None

    @staticmethod
    def benzerlik_analiz(metin1, metin2):
        if metin1 and metin2:
            distance = Levenshtein.distance(metin1, metin2)
            return distance
        else:
            return None
        
    @staticmethod
    def token_analiz(metin):
        tokens = word_tokenize(metin)
        return tokens
    
    @staticmethod
    def metin_istatistik(metin):
        harf_sayısı = sum(1 for char in metin if char.isalpha()) # her harfi 1 sayısına dönüştürür sonra sum ile 1 leri toplar

        kelime_sayısı = len(metin.split())

        etkisiz_kelimeler = ["and", "or", "but", "however", "although", "yet", "so", "for", "because", "since"]
        etkisiz_kelimeler_sayısı = sum(1 for kelime in metin.split() if kelime.lower() in etkisiz_kelimeler)

        # Kelime frekansları
        kelimeler = metin.lower().translate(str.maketrans("", "", string.punctuation)).split()
        kelime_sayıları = Counter(kelimeler)

        # En çok geçen 5 kelime
        en_cok_gecenler = kelime_sayıları.most_common(5)

        # En az geçen 5 kelime
        en_az_gecenler = kelime_sayıları.most_common()[:-6:-1]

        return harf_sayısı, kelime_sayısı, etkisiz_kelimeler_sayısı, en_cok_gecenler, en_az_gecenler

    @staticmethod
    def kelimeyi_tarat(metin, kelime):
        if metin and kelime:
            bulunanlar = []
            baslangic_konum = '1.0'
            while True:
                baslangic_konum = metin.search(kelime, baslangic_konum, stopindex=tk.END)
                if not baslangic_konum:
                    break
                son_konum = f"{baslangic_konum}+{len(kelime)}c"
                bulunanlar.append((baslangic_konum, son_konum))
                baslangic_konum = son_konum
            return bulunanlar
        else:
            return []



class Arayüz:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Metin Analiz Uygulaması")
        self.pencere.geometry("800x600")

        self.main_frame = tk.Frame(pencere)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(self.main_frame, bg="lightblue", width=100)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.duygu_analiz_buton = tk.Button(self.left_frame, text="Duygu Analizi", command=self.duygu_analiz_ekran)
        self.duygu_analiz_buton.pack(pady=10)

        self.benzerlik_analiz_buton = tk.Button(self.left_frame, text="Benzerlik Analizi", command=self.benzerlik_analiz_ekran)
        self.benzerlik_analiz_buton.pack(pady=10)

        self.token_analiz_buton = tk.Button(self.left_frame, text="token Analizi", command=self.token_analiz_ekran)
        self.token_analiz_buton.pack(pady=10)

        self.metin_istatistik_buton = tk.Button(self.left_frame, text="Metin İstatistik", command=self.metin_istatistik_ekran)
        self.metin_istatistik_buton.pack(pady=10)

        self.filtre_buton = tk.Button(self.left_frame, text = "Kelime Filtrele", command=self.filtrele_ekran)
        self.filtre_buton.pack(pady=10) 




    def duygu_analiz_ekran(self):
        self.main_frame.destroy()  # önceki frame ve butonları kaldır
        self.main_frame = tk.Frame(self.pencere)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.metin_giris = tk.Entry(self.main_frame)
        self.metin_giris.pack()

        self.analiz_buton = tk.Button(self.main_frame, text="Analiz Yap", command=self.duygu_analiz_yol)
        self.analiz_buton.pack()

        self.geri_don_buton = tk.Button(self.main_frame, text="Ana Ekrana Geri Dön", command=self.geri_don)
        self.geri_don_buton.pack()

    def duygu_analiz_yol(self):
        metin = self.metin_giris.get().strip()
        duygu = MetinAnaliz.duygu_analiz(metin)
        if duygu:
            messagebox.showinfo("Duygu Analizi Sonucu", f"Metnin duygusu: {duygu[0]}, metnin öznellik değeri: {duygu[1]}")



    def benzerlik_analiz_ekran(self):
        self.main_frame.destroy()  # Sol frame'i ve butonları kaldır
        self.main_frame = tk.Frame(self.pencere)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.metin1_giris = tk.Entry(self.main_frame)
        self.metin1_giris.pack()

        self.metin2_giris = tk.Entry(self.main_frame)
        self.metin2_giris.pack()

        self.analiz_buton = tk.Button(self.main_frame, text="Analiz Yap", command=self.benzerlik_analiz_yol)
        self.analiz_buton.pack()

        self.geri_don_buton = tk.Button(self.main_frame, text="Ana Ekrana Geri Dön", command=self.geri_don)
        self.geri_don_buton.pack()

    def benzerlik_analiz_yol(self):
        metin1 = self.metin1_giris.get().strip()
        metin2 = self.metin2_giris.get().strip()
        distance = MetinAnaliz.benzerlik_analiz(metin1, metin2)
        if distance is not None:
            messagebox.showinfo("Benzerlik Analizi Sonucu", f"Metinler arasındaki Levenshtein mesafesi: {distance}")



    def token_analiz_ekran(self):
        self.main_frame.destroy()  
        self.main_frame = tk.Frame(self.pencere)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.metin_giris = tk.Entry(self.main_frame)
        self.metin_giris.pack()

        self.analiz_buton = tk.Button(self.main_frame, text="Analiz Yap", command=self.token_analiz_yol)
        self.analiz_buton.pack()

        self.geri_don_buton = tk.Button(self.main_frame, text="Ana Ekrana Geri Dön", command=self.geri_don)
        self.geri_don_buton.pack()

    def token_analiz_yol(self):
        metin = self.metin_giris.get().strip()
        tokenler = MetinAnaliz.token_analiz(metin)
        if tokenler:
            messagebox.showinfo("Tokenize işlemi", f"Tokenize sonuç: {tokenler}")

    

    def metin_istatistik_ekran(self):
        self.main_frame.destroy()
        self.main_frame = tk.Frame(self.pencere)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.metin_giris = tk.Text(self.main_frame, height=10, width=50)  #text widgetini çağırdım
        self.metin_giris.pack()

        self.temizle_buton = tk.Button(self.main_frame, text="Analiz Et", command=self.metin_istatistik_yol)
        self.temizle_buton.pack()

        self.geri_don_buton = tk.Button(self.main_frame, text="Ana Ekrana Geri Dön", command=self.geri_don)
        self.geri_don_buton.pack()

    def metin_istatistik_yol(self):
        metin_girdisi = self.metin_giris.get("1.0", "end-1c")  # metni aldım

        # istatistikleri sınıfın metodundan aldım
        harf_sayısı, kelime_sayısı, etkisiz_kelimeler_sayısı, en_cok_gecenler, en_az_gecenler = MetinAnaliz.metin_istatistik(metin_girdisi)

        # Yeni bir pencere oluştur
        istatistik_penceresi = tk.Toplevel(self.pencere)
        istatistik_penceresi.title("Metin İstatistikleri")

        # İstatistikleri gösterecek etiketleri oluştur
        label_harf = ttk.Label(istatistik_penceresi, text="Harf Sayısı: {}".format(harf_sayısı))
        label_kelime = ttk.Label(istatistik_penceresi, text="Kelime Sayısı: {}".format(kelime_sayısı))
        label_etkisiz = ttk.Label(istatistik_penceresi, text="Etkisiz Kelime Sayısı: {}".format(etkisiz_kelimeler_sayısı))
        label_en_cok = ttk.Label(istatistik_penceresi, text="En Çok Geçen 5 Kelime: {}".format(", ".join([kelime[0] for kelime in en_cok_gecenler])))
        label_en_az = ttk.Label(istatistik_penceresi, text="En Az Geçen 5 Kelime: {}".format(", ".join([kelime[0] for kelime in en_az_gecenler])))

        # Etiketleri düzenle
        label_harf.grid(row=0, column=0, sticky="w")
        label_kelime.grid(row=1, column=0, sticky="w")
        label_etkisiz.grid(row=2, column=0, sticky="w")
        label_en_cok.grid(row=3, column=0, sticky="w")
        label_en_az.grid(row=4, column=0, sticky="w")


    def filtrele_ekran(self):
        self.main_frame.destroy()  
        self.main_frame = tk.Frame(self.pencere)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.secim = tk.IntVar()

        self.dosya_secim_1 = tk.Radiobutton(self.main_frame, text="Alice", variable=self.secim, value=1, command=self.dosya_secimi)
        self.dosya_secim_1.pack(anchor=tk.W)

        self.dosya_secim_2 = tk.Radiobutton(self.main_frame, text="Hamlet", variable=self.secim, value=2, command=self.dosya_secimi)
        self.dosya_secim_2.pack(anchor=tk.W)

        self.dosya_secim_3 = tk.Radiobutton(self.main_frame, text="Macbeth", variable=self.secim, value=3, command=self.dosya_secimi)
        self.dosya_secim_3.pack(anchor=tk.W)

        self.text = ScrolledText(self.main_frame, wrap=tk.WORD)
        self.text.pack(expand=True, fill='both')

        self.temizle_butonu = tk.Button(self.main_frame, text="Temizle", command=self.yaziyi_temizle)
        self.temizle_butonu.pack()

        self.arama_alani = tk.Entry(self.main_frame, width=30)
        self.arama_alani.pack(pady=5)

        self.ara_butonu = tk.Button(self.main_frame, text="Ara", command=self.kelimeyi_ara_arayuz)
        self.ara_butonu.pack()

        self.geri_don_buton = tk.Button(self.main_frame, text="Ana Ekrana Geri Dön", command=self.geri_don)
        self.geri_don_buton.pack()



    def dosyadan_metin_oku(self, dosya_yolu):
        try:
            with open(dosya_yolu, 'r', encoding='utf-8') as dosya:
                metin = dosya.read()
        except FileNotFoundError:
            messagebox.showerror("Hata", f"Dosya Bulunamadı")
        return metin

    def dosya_secimi(self):
        secili_dosya = self.secim.get()
        if secili_dosya == 1:
            dosya_yolu = "/home/noctt137/Masaüstü/nlp projesi/text_belgeler/alice.txt"
        elif secili_dosya == 2:
            dosya_yolu = "/home/noctt137/Masaüstü/nlp projesi/text_belgeler/hamlet.txt"
        else:
            dosya_yolu = "/home/noctt137/Masaüstü/nlp projesi/text_belgeler/macbeth.txt"
        dosya_metni = self.dosyadan_metin_oku(dosya_yolu)
        self.text.delete('1.0', tk.END)
        self.text.insert(tk.END, dosya_metni)

    def kelimeyi_ara_arayuz(self):
        metin = self.text
        kelime = self.arama_alani.get()
        if kelime:
            bulunanlar = MetinAnaliz.kelimeyi_tarat(metin, kelime)
            if bulunanlar:
                for baslangic_konum, son_konum in bulunanlar:
                    self.text.tag_add('bulunan', baslangic_konum, son_konum)
                    self.text.tag_config('bulunan', background="yellow")


    def yaziyi_temizle(self):
        self.text.delete('1.0', tk.END)

    def geri_don(self):
        self.main_frame.destroy()  # butona basıldığında fonksyonun ekranından çıkış yap
        self.__init__(self.pencere)  # ara yüzü tekrar çağır


pencere = tk.Tk()
program = Arayüz(pencere)
pencere.mainloop()

