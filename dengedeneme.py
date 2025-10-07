from httpx import Client
import os

class Dengetv54Manager:
    def __init__(self, ana_m3u_dosyasi):
        self.ana_m3u_dosyasi = ana_m3u_dosyasi
        self.httpx = Client(timeout=10, verify=False)
        self.channel_files = [
            "yayinzirve",
            "yayin1",
            "yayininat",
            "yayinb2",
            "yayinb3",
            "yayinb4",
            "yayinb5",
            "yayinbm1",
            "yayinbm2",
            "yayinss",
            "yayinss2",
            "yayint1",
            "yayint2",
            "yayint3",
            "yayinsmarts",
            "yayinsms2",
            "yayintrtspor",
            "yayintrtspor2",
            "yayintrt1",
            "yayinas",
            "yayinatv",
            "yayintv8",
            "yayintv85",
            "yayinf1",
            "yayinnbatv",
            "yayineu1",
            "yayineu2",
            "yayinex1",
            "yayinex2",
            "yayinex3",
            "yayinex4",
            "yayinex5",
            "yayinex6",
            "yayinex7",
            "yayinex8"
        ]
        self.referer_url = "https://audi.zirvedesin19.sbs/"
        os.makedirs(os.path.dirname(self.ana_m3u_dosyasi), exist_ok=True)

    def build_m3u8_content(self):
        m3u_content = ["#EXTM3U"]
        for channel in self.channel_files:
            m3u_content.append(f'#EXTINF:-1 group-title="Dengetv54",{channel.capitalize()}')
            m3u_content.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u_content.append(f'#EXTVLCOPT:http-referrer={self.referer_url}')
            m3u_content.append(f'https://audi.zirvedesin19.sbs/{channel}.m3u8')
        return "\n".join(m3u_content)

    def ana_m3u_guncelle(self, yeni_icerik):
        with open(self.ana_m3u_dosyasi, "w", encoding='utf-8') as dosya:
            dosya.write(yeni_icerik)
        print(f"💾 {self.ana_m3u_dosyasi} kaydedildi.")

    def calistir(self):
        m3u8_icerik = self.build_m3u8_content()
        self.ana_m3u_guncelle(m3u8_icerik)
        print("✅ Kanallar başarıyla M3U’ye eklendi.")

if __name__ == "__main__":
    manager = Dengetv54Manager("M3U/osibusidengedeneme.m3u")
    manager.calistir()
