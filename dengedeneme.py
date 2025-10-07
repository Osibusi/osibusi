from httpx import Client
import os

class Dengetv54Manager:
    def __init__(self, ana_m3u_dosyasi):
        self.ana_m3u_dosyasi = ana_m3u_dosyasi
        self.httpx = Client(timeout=10, verify=False)
        self.referer_url = None
        self.zirvedesin_domain = None
        self.channel_files = [
            "yayinzirve.m3u8",
            "yayin1.m3u8",
            "yayininat.m3u8",
            "yayinb2.m3u8",
            "yayinb3.m3u8",
            "yayinb4.m3u8",
            "yayinb5.m3u8",
            "yayinbm1.m3u8",
            "yayinbm2.m3u8",
            "yayinss.m3u8",
            "yayinss2.m3u8",
            "yayint1.m3u8",
            "yayint2.m3u8",
            "yayint3.m3u8",
            "yayinsmarts.m3u8",
            "yayinsms2.m3u8",
            "yayintrtspor.m3u8",
            "yayintrtspor2.m3u8",
            "yayintrt1.m3u8",
            "yayinas.m3u8",
            "yayinatv.m3u8",
            "yayintv8.m3u8",
            "yayintv85.m3u8",
            "yayinf1.m3u8",
            "yayinnbatv.m3u8",
            "yayineu1.m3u8",
            "yayineu2.m3u8",
            "yayinex1.m3u8",
            "yayinex2.m3u8",
            "yayinex3.m3u8",
            "yayinex4.m3u8",
            "yayinex5.m3u8",
            "yayinex6.m3u8",
            "yayinex7.m3u8",
            "yayinex8.m3u8"
        ]

        # M3U klasörünü oluştur
        os.makedirs(os.path.dirname(self.ana_m3u_dosyasi), exist_ok=True)

    # Referer taraması
    def find_working_domain(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        for i in range(54, 105):
            test_domain = f"https://dengetv{i}.live/"
            print(f"🔍 {test_domain} kontrol ediliyor...")
            try:
                r = self.httpx.get(test_domain, headers=headers)
                if r.status_code == 200 and r.text.strip():
                    print(f"✅ Çalışan referer bulundu: {test_domain}")
                    return test_domain
            except:
                continue
        print("❌ Hiçbir referer bulunamadı!")
        return None

    # Zirvedesin domain taraması (audi sabit)
    def find_zirvedesin_domain(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        for i in range(1, 100):
            test_domain = f"https://audi.zirvedesin{i}.sbs/"
            try:
                r = self.httpx.head(f"{test_domain}{self.channel_files[0]}", headers=headers)
                if r.status_code == 200:
                    print(f"✅ Çalışan zirvedesin domain bulundu: {test_domain}")
                    return test_domain
            except:
                continue
        print("❌ Hiçbir zirvedesin domain bulunamadı!")
        return None

    # M3U içeriği oluştur
    def build_m3u8_content(self):
        m3u_content = ["#EXTM3U"]
        for file_name in self.channel_files:
            channel_name = file_name.replace(".m3u8", "").capitalize()
            m3u_content.append(f'#EXTINF:-1 group-title="Dengetv54",{channel_name}')
            m3u_content.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u_content.append(f'#EXTVLCOPT:http-referrer={self.referer_url}')
            m3u_content.append(f"{self.zirvedesin_domain}{file_name}")
        return "\n".join(m3u_content)

    # M3U dosyasını güncelle
    def ana_m3u_guncelle(self, yeni_icerik):
        with open(self.ana_m3u_dosyasi, "w", encoding="utf-8") as f:
            f.write(yeni_icerik)
        print(f"💾 {self.ana_m3u_dosyasi} güncellendi.")

    # Scripti çalıştır
    def calistir(self):
        self.referer_url = self.find_working_domain()
        if not self.referer_url:
            print("❌ Referer bulunamadığı için işlem iptal edildi.")
            return

        self.zirvedesin_domain = self.find_zirvedesin_domain()
        if not self.zirvedesin_domain:
            print("❌ Zirvedesin domain bulunamadığı için işlem iptal edildi.")
            return

        m3u8_icerik = self.build_m3u8_content()
        self.ana_m3u_guncelle(m3u8_icerik)
        print("✅ Kanallar başarıyla eklendi.")


if __name__ == "__main__":
    manager = Dengetv54Manager("M3U/osibusidengedeneme.m3u")
    manager.calistir()
