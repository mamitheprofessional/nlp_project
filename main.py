from textblob import TextBlob
from nltk.tokenize import word_tokenize
import string
from collections import Counter
import matplotlib.pyplot as plt
import customtkinter
import tkinter as tk
from tkinter import scrolledtext  
import Levenshtein
from tkinter import messagebox



class MetinAnaliz:
    @staticmethod
    def duygu_analiz(metin):
        if metin:
            duygu = TextBlob(metin).sentiment
            return duygu.polarity, duygu.subjectivity
        else:
            return None
        
    @staticmethod
    def token_analiz(metin):
        tokens = word_tokenize(metin)
        return tokens
    
    @staticmethod
    def benzerlik_analiz(metin1, metin2):
        if metin1 and metin2:
            distance = Levenshtein.distance(metin1, metin2)
            return distance
        else:
            return None
    
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




class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("NLP Uygulama")
        self.geometry("1400x650")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)



        # sol frame kısmı
        self.sol_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.sol_frame.grid(row=0, column=0, sticky="wns")
        self.sol_frame.grid_rowconfigure(4, weight=1)
        self.sol_frame_label = customtkinter.CTkLabel(self.sol_frame, text="MENU", compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.sol_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.sol_frame, height=40, text="Metin Analiz",
                                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),anchor="w", command=self.text_girisi)  # Komut ekledim
        self.home_button.grid(row=1, column=0, sticky="ew")




        self.test_button = customtkinter.CTkButton(self.sol_frame, height=40, text="Test",
                                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),anchor="w", command=self.toolkit_ac)  # Test butonu eklendi
        self.test_button.grid(row=3, column=0, sticky="ew", pady=(10, 0))



        self.tema_menu = customtkinter.CTkOptionMenu(self.sol_frame, values=["Light", "Dark", "System"], command=self.tema_mod_sec)
        self.tema_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")



        # ana frame kısmı
        self.ana_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.ana_frame.grid_columnconfigure(0, weight=1)

        self.analiz_buton_tanim = customtkinter.CTkButton(self.ana_frame, text="Analiz Yap" ,command=self.analiz_yap)
        self.analiz_buton_tanim.grid(row=3, column=1, padx=20, pady=10)

        self.benzerlik_checkbutton()  # checkbuttonu çağırmak için






    def select_frame_by_name(self, name):
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "Metin Analiz" else "transparent")
        if name == "Metin Analiz":
            self.ana_frame.grid(row=0, column=1, sticky="nsew")




    def analiz_yap(self):
        if self.check_var.get():
            self.levenshtein_benzerlik()
        else:
            metin = self.text_input.get("1.0", tk.END)

            kelimeler = metin.lower().split()
            kelime_sayıları = Counter(kelimeler)

            # En çok geçen 5 kelimeyi al
            en_cok_gecenler = kelime_sayıları.most_common(15)
            en_az_gecenler = kelime_sayıları.most_common()[:-6:-1]

            # Çekirdek grafiğini oluştur
            fig, ax = plt.subplots(2, 1, figsize=(8, 6))
            self.cekirdek_grafigi(ax[0], en_cok_gecenler, "En Çok Geçen Kelimeler")
            self.cekirdek_grafigi(ax[1], en_az_gecenler, "En Az Geçen Kelimeler")
            plt.tight_layout()

            # Sonuçları metin olarak göster
            sonuc_metni = self.analiz_bilgileri(metin)
            plt.figtext(0.5, 0.01, sonuc_metni, ha="center", fontsize=10, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})

            # Çekirdek grafiğini göster
            plt.show()



    def cekirdek_grafigi(self, ax, kelime_listesi, baslik):
        kelimeler, frekanslar = zip(*kelime_listesi)

        ax.bar(kelimeler, frekanslar)
        ax.set_ylabel('Frekans')
        ax.set_title(baslik)
        ax.tick_params(axis='x', rotation=45)

    def analiz_bilgileri(self, metin):
        # Metin analizi bilgilerini hesapla
        kelime_sayisi = len(metin.split())
        harf_sayisi = sum(1 for char in metin if char.isalpha())
        etkisiz_kelimeler = ["and", "or", "but", "however", "although", "yet", "so", "for", "because", "since"]
        etkisiz_kelimeler_sayisi = sum(1 for kelime in metin.split() if kelime.lower() in etkisiz_kelimeler)

        # Bilgileri metin olarak formatla
        bilgi_metni = f"Kelime Sayısı: {kelime_sayisi}\nHarf Sayısı: {harf_sayisi}\nEtkisiz Kelime Sayısı: {etkisiz_kelimeler_sayisi}"

        return bilgi_metni


    def text_girisi(self):
        self.select_frame_by_name("Metin Analiz")
        # Metin girişi widget'ını oluştur
        self.text_input = scrolledtext.ScrolledText(self.ana_frame, wrap=tk.WORD, width=167, height=5)
        self.text_input.grid(row=2, column=1, padx=20, pady=(50, 70), sticky="s")
        self.ana_frame.grid_rowconfigure(0, weight=1)
        self.ana_frame.grid_columnconfigure(0, weight=1)
        self.text_input.configure(bg="#424949", fg="#F2F3F4")
        self.second_text_input = None  # ikinci metin giriş widgeti için başlangıç değeri none
        self.dosya_getir() #radiobutton için


    def benzerlik_checkbutton(self):
        self.check_var = tk.BooleanVar()
        self.check_button = customtkinter.CTkCheckBox(self.ana_frame, text="Benzerlik Analizi", variable=self.check_var, command=self.ikinci_ekrani_ac)
        self.check_button.grid(row=0, column=1, padx=20, pady=30, sticky="nw")
    
    def ikinci_ekrani_ac(self):
        if self.check_var.get():
            self.second_text_input = scrolledtext.ScrolledText(self.ana_frame, wrap=tk.WORD, width=167, height=5)
            self.second_text_input.grid(row=1, column=1, padx=20, pady=(10, 70), sticky="s")
            self.second_text_input.configure(bg="#424949", fg="#F2F3F4")
        else:
            if self.second_text_input:
                self.second_text_input.destroy()
                self.second_text_input = None

    def levenshtein_benzerlik(self):
        if self.check_var.get():
            metin1 = self.text_input.get("1.0", "end").strip()
            metin2 = self.second_text_input.get("1.0", "end").strip()

            if metin1 and metin2:
                mesafe = Levenshtein.distance(metin1, metin2)
                benzerlik = 1 - (mesafe / max(len(metin1), len(metin2)))
                sonuc = f"Levenshtein Mesafesi: {mesafe}\nBenzerlik Oranı: {benzerlik:.2f}"
                messagebox.showinfo("Benzerlik Analizi Sonucu", sonuc)
            else:
                messagebox.showwarning("Uyarı", "Lütfen her iki metin kutusunu da doldurun.")



    def dosya_secimi(self):
        secili_dosya = self.secim.get()
        if secili_dosya == 1:
            dosya_yolu = "/home/noctt137/Masaüstü/nlp projesi/nlp_project/text_belgeler/alice.txt"
        elif secili_dosya == 2:
            dosya_yolu = "/home/noctt137/Masaüstü/nlp projesi/nlp_project/text_belgeler/hamlet.txt"
        else:
            dosya_yolu = "/home/noctt137/Masaüstü/nlp projesi/nlp_project/text_belgeler/macbeth.txt"
        dosya_metni = self.dosyadan_metin_oku(dosya_yolu)
        self.text_input.delete('1.0', tk.END)
        self.text_input.insert(tk.END, dosya_metni)

    def dosyadan_metin_oku(self, dosya_yolu):
        with open(dosya_yolu, "r", encoding="utf-8") as file:
            return file.read()



    def dosya_getir(self):
        self.secim = tk.IntVar()

        self.dosya_secim_1 = customtkinter.CTkRadioButton(self.ana_frame, text="Alice", variable=self.secim, value=1, command=self.dosya_secimi)
        self.dosya_secim_1.grid(row=3, column=1, sticky="w", padx=20)

        self.dosya_secim_2 = customtkinter.CTkRadioButton(self.ana_frame, text="Hamlet", variable=self.secim, value=2, command=self.dosya_secimi)
        self.dosya_secim_2.grid(row=3, column=1, sticky="w", padx=120)

        self.dosya_secim_3 = customtkinter.CTkRadioButton(self.ana_frame, text="Macbeth", variable=self.secim, value=3, command=self.dosya_secimi)
        self.dosya_secim_3.grid(row=3, column=1, sticky="w", padx=220)



    def tema_mod_sec(self, yeni_tema_mod):
        customtkinter.set_appearance_mode(yeni_tema_mod)


    def toolkit_ac(self):
        import toolkit

if __name__ == "__main__":
    app = App()
    app.mainloop()

