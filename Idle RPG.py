from random import randint
import sqlite3

class Uye():
    def __init__(self,kullaniciAdi,sifre):

        self.kullaniciAdi = kullaniciAdi
        self.sifre = sifre
        self.karakterListesi = []

uyeListesi = []

class Karakter():

    def __init__(self,isim,seviye,sinif):
        self.isim = isim
        self.seviye = seviye
        self.seviyeMevcut = float(0)
        self.seviyeToplam = float(2*self.seviye)
        self.seviyeYuzde = float((self.seviyeMevcut / self.seviyeToplam)*100)
        self.sinif = sinif

        yetenekPuani = 12*(self.seviye-1)
        kuvvetStat = yetenekPuani - randint(0,yetenekPuani)
        yetenekPuani -= kuvvetStat
        ceviklikStat = yetenekPuani - randint(0,yetenekPuani)
        yetenekPuani -= ceviklikStat
        zekaStat = yetenekPuani - randint(0,yetenekPuani)
        yetenekPuani -= zekaStat
        saldiriStat = yetenekPuani

        self.saldiri = 1 + saldiriStat
        if self.sinif == 1:
            self.kuvvet = 2 + kuvvetStat
            self.hasar = 10*self.saldiri + 5*self.kuvvet
        else:
            self.kuvvet = 1 + kuvvetStat
        if self.sinif == 2:
            self.ceviklik = 4 + ceviklikStat
            self.hasar = 10*self.saldiri + 5*self.ceviklik
        else:
            self.ceviklik = 2 + ceviklikStat
        if self.sinif == 3:
            self.zeka = 3 + zekaStat
            self.hasar = 10*self.saldiri + 5*self.zeka
        else:
            self.zeka = 1 + zekaStat

        self.saglik = 200*self.kuvvet
        self.mana = 400 + (100*self.zeka)
        self.tbh = self.hasar * int((self.ceviklik / 2))

db = sqlite3.connect("SaveData.db")
imlec = db.cursor()
imlec.execute("CREATE TABLE IF NOT EXISTS uyeTablosu (kullaniciAdi,sifre)")
imlec.execute("SELECT * FROM uyeTablosu")
uyeVeriler = imlec.fetchall()
db.close()

for i in uyeVeriler:
    uyeListesi.append(Uye(i[0],i[1]))

for i in uyeListesi:

    db = sqlite3.connect("SaveData.db")
    imlec = db.cursor()
    imlec.execute("CREATE TABLE IF NOT EXISTS karakterTablosu (kullanici,isim,seviye,seviyeMevcut,seviyeToplam,"
                  "seviyeYuzde,sinif,saldiri,kuvvet,ceviklik,zeka,hasar,saglik,mana,tbh)")
    imlec.execute("SELECT * FROM karakterTablosu WHERE kullanici=?",[i.kullaniciAdi])
    karakterVeriler = imlec.fetchall()
    db.close()

    tur = -1
    for y in karakterVeriler:
        tur += 1
        i.karakterListesi.append(Karakter(y[1],y[2],y[6]))
        i.karakterListesi[tur].kullanici = y[0]
        i.karakterListesi[tur].seviyeMevcut = y[3]
        i.karakterListesi[tur].seviyeToplam = y[4]
        i.karakterListesi[tur].seviyeYuzde = y[5]
        i.karakterListesi[tur].saldiri = y[7]
        i.karakterListesi[tur].kuvvet = y[8]
        i.karakterListesi[tur].ceviklik = y[9]
        i.karakterListesi[tur].zeka = y[10]
        i.karakterListesi[tur].hasar = y[11]
        i.karakterListesi[tur].saglik = y[12]
        i.karakterListesi[tur].mana = y[13]
        i.karakterListesi[tur].tbh = y[14]

def ka_uye(ka):
    for i in uyeListesi:
        if ka == i.kullaniciAdi:
            return i

def isimYaratici():

    from random import choice
    from random import randint

    harfListesi = []
    harfSayisi = randint(1, 8)
    mevcutSayi = 0

    sesliKucukler = "aeiou"
    sesliBuyukler = "AEIOU"
    sessizKucukler = "bcdfghjklmnprstvyz"
    sessizBuyukler = "BCDFGHJKLMNPRSTVYZ"

    sesliler = sesliKucukler + sesliBuyukler
    sessizler = sessizKucukler + sessizBuyukler
    kucukler = sesliKucukler + sessizKucukler
    buyukler = sesliBuyukler + sessizBuyukler

    def sesliKucuk():
        return (choice(sesliKucukler))

    def sesliBuyuk():
        return (choice(sesliBuyukler))

    def sessizKucuk():
        return (choice(sessizKucukler))

    def sessizBuyuk():
        return (choice(sessizBuyukler))

    def sesli():
        return (choice(sesliler))

    def sessiz():
        return (choice(sessizler))

    def kucuk():
        return (choice(kucukler))

    def buyuk():
        return (choice(buyukler))

    harfListesi.append(buyuk())
    mevcutSayi += 1

    if harfListesi[0] in sesliler:
        harfListesi.append(sessizKucuk())
    elif harfListesi[0] in sessizler:
        harfListesi.append(sesliKucuk())
    mevcutSayi += 1

    for i in range(2, 7):
        if mevcutSayi < harfSayisi:
            if harfListesi[i - 1] in sesliler:
                harfListesi.append(sessizKucuk())
            elif harfListesi[i - 1] in sessizler:
                if mevcutSayi == harfSayisi - 1:
                    harfListesi.append(sesliKucuk())
                elif harfListesi[i - 2] in sessizler:
                    harfListesi.append(sesliKucuk())
                elif harfListesi[i - 2] in sesliler:
                    harfListesi.append(kucuk())
        else:
            break
        mevcutSayi += 1

    x = ""
    for i in harfListesi:
        i = str(i)
        x += i
    return(x)

def seviyeAtla(karakter):

    print()
    print("Seviye {} oldunuz! Yetenek puanlarınızı yerleştirin.".format(karakter.seviye+1))
    print("""
    - Saldırı  : {}  ---->  Hasar gücünüzü arttırır.
    - Kuvvet   : {}  ---->  Dayanıklılığınızı arttırır. Savaşçılara ekstra hasar sağlar.
    - Çeviklik : {}  ---->  Saldırı hızınızı arttırır. Süikastçilere ekstra hasar sağlar.
    - Zeka     : {}  ---->  Mana miktarınızı arttırır. Büyücülere ekstra hasar sağlar.
    """.format(karakter.saldiri,karakter.kuvvet,karakter.ceviklik,karakter.zeka))
    print("12 adet yetenek puanınız bulunmaktadır. Bunları özellikleriniz arasında dağıtın.")

    while True:

        while True:
            try:
                saldiri = int(input("Eklemek istediğiniz puan; Saldırı: "))
                break
            except:
                print("Lütfen sayı giriniz.")
                continue

        while True:
            try:
                kuvvet = int(input("Kuvvet: "))
                break
            except:
                print("Lütfen sayı giriniz.")
                continue

        while True:
            try:
                ceviklik = int(input("Çeviklik: "))
                break
            except:
                print("Lütfen sayı giriniz.")
                continue

        while True:
            try:
                zeka = int(input("Zeka: "))
                break
            except:
                print("Lütfen sayı giriniz.")
                continue

        if saldiri + kuvvet + ceviklik + zeka != 12:
            print("Girdiğiniz değerlerin toplamı 12 etmemektedir. Lütfen tekrar deneyiniz.")
            continue

        elif saldiri + kuvvet + ceviklik + zeka == 12:
            print("Yetenek puanlarınız eklendi.")
            input("Devam etmek için 'enter'a basınız...")
            break

    karakter.seviye += 1
    karakter.seviyeMevcut = float(0)
    karakter.seviyeToplam = float(2 * karakter.seviye)
    karakter.seviyeYuzde = float((karakter.seviyeMevcut / karakter.seviyeToplam) * 100)
    karakter.saldiri += saldiri

    karakter.kuvvet += kuvvet
    karakter.ceviklik += ceviklik
    karakter.zeka += zeka
    karakter.saglik = 200 * karakter.kuvvet
    karakter.mana = 400 + (100 * karakter.zeka)

    if karakter.sinif == 1:
        karakter.hasar = (10 * karakter.saldiri) + (5 * karakter.kuvvet)
    elif karakter.sinif == 2:
        karakter.hasar = (10 * karakter.saldiri) + (5 * karakter.ceviklik)
    elif karakter.sinif == 3:
        karakter.hasar = (10 * karakter.saldiri) + (5 * karakter.zeka)

    karakter.tbh = karakter.hasar * int(karakter.ceviklik / 2)

    db = sqlite3.connect("SaveData.db")

    imlec = db.cursor()
    imlec.execute("CREATE TABLE IF NOT EXISTS karakterTablosu (kullanici,isim,seviye,seviyeMevcut,seviyeToplam,"
                  "seviyeYuzde,sinif,saldiri,kuvvet,ceviklik,zeka,hasar,saglik,mana,tbh)")

    imlec.execute("UPDATE karakterTablosu SET seviye=? WHERE isim=?", (karakter.seviye,karakter.isim))
    db.commit()
    imlec.execute("UPDATE karakterTablosu SET seviyeMevcut=? WHERE isim=?", (karakter.seviyeMevcut, karakter.isim))
    db.commit()
    imlec.execute("UPDATE karakterTablosu SET seviyeToplam=? WHERE isim=?", (karakter.seviyeToplam, karakter.isim))
    db.commit()
    imlec.execute("UPDATE karakterTablosu SET seviyeYuzde=? WHERE isim=?", (karakter.seviyeYuzde, karakter.isim))
    db.commit()
    imlec.execute("UPDATE karakterTablosu SET saldiri=? WHERE isim=?", (karakter.saldiri, karakter.isim))
    db.commit()
    imlec.execute("UPDATE karakterTablosu SET hasar=? WHERE isim=?", (karakter.hasar, karakter.isim))
    db.commit()
    imlec.execute("UPDATE karakterTablosu SET kuvvet=? WHERE isim=?", (karakter.kuvvet, karakter.isim))
    db.commit()
    imlec.execute("UPDATE karakterTablosu SET ceviklik=? WHERE isim=?", (karakter.ceviklik, karakter.isim))
    db.commit()
    imlec.execute("UPDATE karakterTablosu SET zeka=? WHERE isim=?", (karakter.zeka, karakter.isim))
    db.commit()
    imlec.execute("UPDATE karakterTablosu SET saglik=? WHERE isim=?", (karakter.saglik, karakter.isim))
    db.commit()
    imlec.execute("UPDATE karakterTablosu SET mana=? WHERE isim=?", (karakter.mana, karakter.isim))
    db.commit()
    imlec.execute("UPDATE karakterTablosu SET tbh=? WHERE isim=?", (karakter.tbh, karakter.isim))
    db.commit()

    db.close()

def kapisma(oyuncu,dusman):

    oMevcutSaglik = oyuncu.saglik
    oMevcutMana = oyuncu.mana
    dMevcutSaglik = dusman.saglik
    dMevcutMana = dusman.mana

    if oyuncu.sinif == 1:
        os = "Savaşçı"
    elif oyuncu.sinif == 2:
        os = "Süikastçi"
    elif oyuncu.sinif == 3:
        os = "Büyücü"
    if dusman.sinif == 1:
        ds = "Savaşçı"
    elif dusman.sinif == 2:
        ds = "Süikastçi"
    elif dusman.sinif == 3:
        ds = "Büyücü"

    while True:

        print(100 * "=")
        print("""
            {}  |  Seviye {} {}  |  Sağlık: {} / {}  |  Mana: {} / {}  |  Tur Başına Hasar: {}
            VS.
            {}  |  Seviye {} {}  |  Sağlık: {} / {}  |  Mana: {} / {}  |  Tur Başına Hasar: {}
            """.format(oyuncu.isim, oyuncu.seviye,os,oMevcutSaglik, oyuncu.saglik, oMevcutMana, oyuncu.mana,
                       oyuncu.tbh, dusman.isim,
                       dusman.seviye,ds, dMevcutSaglik, dusman.saglik, dMevcutMana, dusman.mana, dusman.tbh))
        print(100 * "=")

        tumKarakterler = []
        for i in uyeListesi:
            for y in i.karakterListesi:
                tumKarakterler.append(y)

        if dusman in tumKarakterler:
            print("""
            [1] Saldır
            [2] Kendine can bas (500 Mana)
            [3] Kaç
                """)
        else:
            print("""
            [1] Saldır
            [2] Kendine can bas (500 Mana)
            [3] Kaç (Tecrübe kaybettirir)
                """)

        while True:
            sec = input("Seçiminiz: ")
            if sec != "1" and sec != "2" and sec != "3":
                print("Hatalı giriş.")
                continue
            elif sec == "2" and oMevcutMana < 500:
                print("Yetersiz mana.")
                continue
            elif sec == "2" and oMevcutSaglik == oyuncu.saglik:
                print("Sağlığınız zaten tam dolu.")
                continue
            else:
                print()
                break

        if sec == "1":
            eskiSaglik = dMevcutSaglik
            dMevcutSaglik -= oyuncu.tbh
            print("{} rakibine {} kadar hasar verdi.".format(oyuncu.isim, oyuncu.tbh))
            print("{} için {} olan sağlıktan {} kaldı.".format(dusman.isim, eskiSaglik, dMevcutSaglik))

        elif sec == "2":
            eskiSaglik = oMevcutSaglik
            oMevcutSaglik += int(oyuncu.saglik / 4)
            oMevcutMana -= 500
            print("{} kendisine can bastı.".format(oyuncu.isim))
            print("Sağlığı {} iken {} oldu.".format(eskiSaglik, oMevcutSaglik))

        elif sec == "3":
            if oyuncu.seviyeMevcut == 0:
                print("{} kaçtı.".format(oyuncu.isim))
                input("Devam etmek için 'enter'a basınız...")
                break
            else:
                eskiSeviye = oyuncu.seviyeYuzde
                oyuncu.seviyeMevcut = oyuncu.seviyeMevcut / 2
                oyuncu.seviyeYuzde = (oyuncu.seviyeMevcut / oyuncu.seviyeToplam) * 100

                db = sqlite3.connect("SaveData.db")
                imlec = db.cursor()
                imlec.execute(
                    "CREATE TABLE IF NOT EXISTS karakterTablosu (kullanici,isim,seviye,seviyeMevcut,seviyeToplam,"
                    "seviyeYuzde,sinif,saldiri,kuvvet,ceviklik,zeka,hasar,saglik,mana,tbh)")
                imlec.execute("UPDATE karakterTablosu SET seviyeMevcut=? WHERE isim=?",
                              (oyuncu.seviyeMevcut, oyuncu.isim))
                db.commit()
                imlec.execute("UPDATE karakterTablosu SET seviyeYuzde=? WHERE isim=?",
                              (oyuncu.seviyeYuzde, oyuncu.isim))
                db.commit()
                db.close()

                print("{} kaçtı. % {} olan tecrübe puanından % {} kaldı.".format(oyuncu.isim,eskiSeviye,oyuncu.seviyeYuzde))
                input("Devam etmek için 'enter'a basınız...")
                break

        print()

        if dMevcutSaglik <= int(3*(dusman.saglik / 4)) and dMevcutMana >= 500:
            eskiSaglik = dMevcutSaglik
            dMevcutSaglik += int(dusman.saglik / 4)
            dMevcutMana -= 500
            print("{} kendisine can bastı.".format(dusman.isim))
            print("Sağlığı {} iken {} oldu.".format(eskiSaglik,dMevcutSaglik))

        else:
            eskiSaglik = oMevcutSaglik
            oMevcutSaglik -= dusman.tbh
            print("{} rakibine {} kadar hasar verdi.".format(dusman.isim,dusman.tbh))
            print("{} için {} olan sağlıktan {} kaldı.".format(oyuncu.isim,eskiSaglik,oMevcutSaglik))

        print()
        input("Devam etmek için 'enter'a basınız.")
        print()

        if oMevcutSaglik <= 0 and dMevcutSaglik <= 0:
            print("Mücadele beraberlikle sonuçlandı.")
            input("Devam etmek için 'enter'a basınız...")
            break

        elif oMevcutSaglik <= 0:
            oyuncu.seviyeMevcut = float(0)
            oyuncu.seviyeYuzde = float(0)

            db = sqlite3.connect("SaveData.db")
            imlec = db.cursor()
            imlec.execute(
                "CREATE TABLE IF NOT EXISTS karakterTablosu (kullanici,isim,seviye,seviyeMevcut,seviyeToplam,"
                "seviyeYuzde,sinif,saldiri,kuvvet,ceviklik,zeka,hasar,saglik,mana,tbh)")
            imlec.execute("UPDATE karakterTablosu SET seviyeMevcut=? WHERE isim=?", (oyuncu.seviyeMevcut, oyuncu.isim))
            db.commit()
            imlec.execute("UPDATE karakterTablosu SET seviyeYuzde=? WHERE isim=?", (oyuncu.seviyeYuzde, oyuncu.isim))
            db.commit()
            db.close()

            print("{} kaybetti. Tecrübe puanı sıfırlandı.".format(oyuncu.isim))
            input("Devam etmek için 'enter'a basınız...")
            break

        elif dMevcutSaglik <= 0:
            dusman.seviyeMevcut = float(0)
            dusman.seviyeYuzde = float(0)

            db = sqlite3.connect("SaveData.db")
            imlec = db.cursor()
            imlec.execute(
                "CREATE TABLE IF NOT EXISTS karakterTablosu (kullanici,isim,seviye,seviyeMevcut,seviyeToplam,"
                "seviyeYuzde,sinif,saldiri,kuvvet,ceviklik,zeka,hasar,saglik,mana,tbh)")
            imlec.execute("UPDATE karakterTablosu SET seviyeMevcut=? WHERE isim=?", (dusman.seviyeMevcut, dusman.isim))
            db.commit()
            imlec.execute("UPDATE karakterTablosu SET seviyeYuzde=? WHERE isim=?", (dusman.seviyeYuzde, dusman.isim))
            db.commit()
            db.close()

            if dusman not in tumKarakterler:

                oyuncu.seviyeMevcut += 1
                oyuncu.seviyeYuzde = oyuncu.seviyeYuzde = int((oyuncu.seviyeMevcut / oyuncu.seviyeToplam)*100)

                db = sqlite3.connect("SaveData.db")
                imlec = db.cursor()
                imlec.execute(
                    "CREATE TABLE IF NOT EXISTS karakterTablosu (kullanici,isim,seviye,seviyeMevcut,seviyeToplam,"
                    "seviyeYuzde,sinif,saldiri,kuvvet,ceviklik,zeka,hasar,saglik,mana,tbh)")
                imlec.execute("UPDATE karakterTablosu SET seviyeMevcut=? WHERE isim=?", (oyuncu.seviyeMevcut,oyuncu.isim))
                db.commit()
                imlec.execute("UPDATE karakterTablosu SET seviyeYuzde=? WHERE isim=?", (oyuncu.seviyeYuzde, oyuncu.isim))
                db.commit()
                db.close()
            if dusman not in tumKarakterler:
                print("{} kazandı. ( + Tecrübe )".format(oyuncu.isim))
            else:
                print("{} kazandı.".format(oyuncu.isim))
            input("Devam etmek için 'enter'a basınız...")
            break

while True:

    print("""
    *** IDLE RPG ***
    
    [1] Üye girişi
    [2] Üye ol
    [3] Çıkış
    """)

    while True:
        secim1 = input("Seçiminiz: ")
        if secim1 != "1" and secim1 != "2" and secim1 != "3":
            print("Hatalı giriş.")
        elif secim1 == "1" and len(uyeListesi) == 0:
            print("Henüz üyelik bulunmamaktadır.")
        else:
            break

    if secim1 == "1":

        while True:
            kullaniciAdi = input("Kullanıcı adı: ")
            if ka_uye(kullaniciAdi) not in uyeListesi:
                print("Kullanıcı adı bulunamadı.")

                while True:
                    tekrar = input("Tekrar dene? ( e / h ) ")
                    if tekrar != "e" and tekrar != "E" and tekrar != "h" and tekrar != "H":
                        print("Hatalı giriş.")
                        continue
                    else:
                        break

                if tekrar == "e" or tekrar == "E":
                    continue
                elif tekrar == "h" or tekrar == "H":
                    break
            else:
                break

        if ka_uye(kullaniciAdi) in uyeListesi:

            while True:
                sifre = input("Şifre: ")
                if sifre != ka_uye(kullaniciAdi).sifre:
                    print("Şifre hatalı.")

                    while True:
                        tekrar = input("Tekrar dene? ( e / h ) ")
                        if tekrar != "e" and tekrar != "E" and tekrar != "h" and tekrar != "H":
                            print("Hatalı giriş.")
                            continue
                        else:
                            break

                    if tekrar == "e" or tekrar == "E":
                        continue
                    elif tekrar == "h" or tekrar == "H":
                        break
                else:
                    break

            if sifre == ka_uye(kullaniciAdi).sifre:









                while True:

                    print("""
    [1] Karakter seçimi
    [2] Karakter yarat
    [3] Karakter sil
    [4] Ana menüye dön
                    """)
                    print(kullaniciAdi)

                    while True:
                        secim2 = input("Seçiminiz: ")
                        if secim2 != "1" and secim2 != "2" and secim2 != "3" and secim2 != "4":
                            print("Hatalı giriş.")
                        elif secim2 == "1" and len(ka_uye(kullaniciAdi).karakterListesi) == 0:
                            print("Karakteriniz bulunmamaktadır.")
                        elif secim2 == "3" and len(ka_uye(kullaniciAdi).karakterListesi) == 0:
                            print("Karakteriniz bulunmamaktadır.")
                        else:
                            break










                    if secim2 == "1":

                        print()
                        tur = 0
                        for i in ka_uye(kullaniciAdi).karakterListesi:
                            tur += 1
                            if i.sinif == 1:
                                sinifIsim = "Savaşçı"
                            elif i.sinif == 2:
                                sinifIsim = "Süikastçi"
                            elif i.sinif == 3:
                                sinifIsim = "Büyücü"
                            print("[{}] {}  |  Seviye {} {}".format(tur,i.isim,i.seviye,sinifIsim))
                        print()

                        while True:
                            try:
                                secim3 = int(input("Karakter seçiniz: "))
                            except:
                                print("Hatalı giriş.")
                                continue
                            if secim3 < 1 or secim3 > len(ka_uye(kullaniciAdi).karakterListesi):
                                print("Hatalı giriş.")
                                continue
                            else:
                                break

                        karakter = ka_uye(kullaniciAdi).karakterListesi[secim3-1]

                        while True:









                            if karakter.sinif == 1:
                                sinifIsim = "Savaşçı"
                            elif karakter.sinif == 2:
                                sinifIsim = "Süikastçi"
                            elif karakter.sinif == 3:
                                sinifIsim = "Büyücü"

                            print("""
    {}
    Seviye {} {}
    Tecrübe : % {}
    Sağlık  :   {}
    Mana    :   {}
    Kuvvet  :   {}
    Çeviklik:   {}
    Zeka    :   {}
    Tur Başına Hasar: {}
                                                """.format(karakter.isim, karakter.seviye, sinifIsim,
                                                           karakter.seviyeYuzde, karakter.saglik,
                                                           karakter.mana, karakter.kuvvet, karakter.ceviklik,
                                                           karakter.zeka, karakter.tbh))

                            print("""
    [1] Rastgele bir düşmana saldır
    [2] Mevcut bir karaktere meydan oku
    [3] Bir önceki menüye dön
                                                """)

                            tumKarakterler = []
                            for i in uyeListesi:
                                for y in i.karakterListesi:
                                    tumKarakterler.append(y)

                            while True:
                                secim4 = input("Seçiminiz: ")
                                if secim4 != "1" and secim4 != "2" and secim4 != "3":
                                    print("Hatalı giriş.")
                                    continue
                                elif secim4 == "2" and len(tumKarakterler) < 2:
                                    print("Yalnızca 1 adet karakter bulunmaktadır.")
                                else:
                                    break

                            if secim4 == "1":

                                ri = isimYaratici()
                                yeniDusman = Karakter(ri,karakter.seviye,randint(1,3))

                                if karakter.seviye == 1:
                                    yeniDusman.kuvvet = 1
                                    yeniDusman.ceviklik = 2
                                    yeniDusman.zeka = 1
                                    yeniDusman.saglik = 200
                                    yeniDusman.tbh = 20

                                kapisma(karakter,yeniDusman)
                                if karakter.seviyeMevcut >= karakter.seviyeToplam:
                                    seviyeAtla(karakter)
                                continue


                            if secim4 == "2":

                                print()
                                tur = 0
                                for i in uyeListesi:
                                    for y in i.karakterListesi:
                                        if y.isim != karakter.isim:
                                            tur += 1
                                            print("[{}] {} (Kullanıcı: {})".format(tur,y.isim,i.kullaniciAdi))
                                print()

                                while True:
                                    try:
                                        secim5 = int(input("Kaç numaralı rakibe meydan okumak istiyorsunuz? "))
                                    except:
                                        print("Hatalı giriş.")
                                        continue
                                    if secim5 < 1 or secim5 > len(tumKarakterler) - 1:
                                        print("Hatalı giriş.")
                                        continue
                                    else:
                                        break

                                tumKarakterler.remove(karakter)
                                kapisma(karakter,tumKarakterler[secim5-1])
                                continue





                            elif secim4 == "3":
                                break








                    elif secim2 == "2":

                        while True:
                            karakterAdi = input("Karakter İsmi: ")
                            isimListesi = []
                            for i in uyeListesi:
                                for y in i.karakterListesi:
                                    isimListesi.append(y.isim)
                            if karakterAdi in isimListesi:
                                print("Bu karakter ismi daha önce kullanılmış.")
                            else:
                                break

                        print("""
    *** SINIFLAR ***
    
    [1] Savaşçı: Dayanıklılıkları sayesinde göğüs göğüse mücadele etmekten çekinmezler. 'Kuvvet' değerleri aynı zamanda hasar güçlerini de etkiler.
    [2] Süikastçi: Saldırı yetenekleri sayesinde rakiplerine kısa zamanda yüksek hasar verme konusunda ustalaşmıştırlar. 'Çeviklik' değerleri aynı zamanda hasar güçlerini de etkiler.
    [3] Büyücü: Can basma büyüleri sayesinde kritik anlardan ustalıkla kurtulma becerisine sahiptirler. 'Zeka' değerleri aynı zamanda hasar güçlerini de etkiler.
                        """)

                        while True:
                            try:
                                sinif = int(input("Sınıf seçiniz: "))
                            except:
                                print("Hatalı giriş.")
                                continue
                            if sinif != 1 and sinif != 2 and sinif != 3:
                                print("Hatalı giriş.")
                            else:
                                break

                        ka_uye(kullaniciAdi).karakterListesi.append(Karakter(karakterAdi,1,sinif))

                        db = sqlite3.connect("SaveData.db")
                        imlec = db.cursor()
                        imlec.execute("CREATE TABLE IF NOT EXISTS karakterTablosu (kullanici,isim,seviye,seviyeMevcut,seviyeToplam,"
                                      "seviyeYuzde,sinif,saldiri,kuvvet,ceviklik,zeka,hasar,saglik,mana,tbh)")
                        k = ka_uye(kullaniciAdi).karakterListesi[len(ka_uye(kullaniciAdi).karakterListesi)-1]
                        imlec.execute("INSERT INTO karakterTablosu VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(kullaniciAdi,
                                                                                                             k.isim,k.seviye,k.seviyeMevcut,
                                                                                                             k.seviyeToplam,k.seviyeYuzde,k.sinif,
                                                                                                             k.saldiri,k.kuvvet,k.ceviklik,k.zeka,
                                                                                                             k.hasar,k.saglik,k.mana,k.tbh))
                        db.commit()
                        db.close()

                        print("Karakteriniz oluşturuldu.")
                        input("Devam etmek için 'enter'a basınız...")
                        continue

                    elif secim2 == "3":
                        tur = 0
                        for i in ka_uye(kullaniciAdi).karakterListesi:
                            tur += 1
                            if i.sinif == 1:
                                sinifIsim = "Savaşçı"
                            elif i.sinif == 2:
                                sinifIsim = "Süikastçi"
                            elif i.sinif == 3:
                                sinifIsim = "Büyücü"
                            print("[{}] {}  |  Seviye {} {}".format(tur, i.isim, i.seviye, sinifIsim))

                        while True:
                            try:
                                sil = int(input("Kaç numarayı silmek istiyorsunuz? "))
                            except:
                                print("Hatalı giriş.")
                                continue
                            if sil < 1 or sil > len(ka_uye(kullaniciAdi).karakterListesi):
                                print("Hatalı giriş.")
                                continue
                            else:
                                break

                        db = sqlite3.connect("SaveData.db")
                        imlec = db.cursor()
                        imlec.execute("DELETE FROM karakterTablosu WHERE isim=?", [ka_uye(kullaniciAdi).karakterListesi[sil-1].isim])
                        db.commit()
                        db.close()

                        ka_uye(kullaniciAdi).karakterListesi.remove(ka_uye(kullaniciAdi).karakterListesi[sil - 1])

                        print("Karakteriniz silindi.")
                        input("Devam etmek için 'enter'a basınız.")
                        continue

                    elif secim2 == "4":
                        break












    elif secim1 == "2":

        while True:
            kullaniciAdi = input("Kullanıcı Adı: ")
            if ka_uye(kullaniciAdi) in uyeListesi:
                print("Bu kullanıcı adı daha önce alınmış.")
            else:
                break

        sifre = input("Şifre: ")

        uyeListesi.append(Uye(kullaniciAdi,sifre))

        db = sqlite3.connect("SaveData.db")
        imlec = db.cursor()
        imlec.execute("CREATE TABLE IF NOT EXISTS uyeTablosu (kullaniciAdi,sifre)")
        imlec.execute("INSERT INTO uyeTablosu VALUES (?,?)", (kullaniciAdi,sifre))
        db.commit()
        db.close()

        print("Üyelik oluşturuldu.")
        input("Devam etmek için 'enter'a basınız...")

    elif secim1 == "3":
        quit()



































