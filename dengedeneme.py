from httpx import Client
import os

class DengetvManager:
    def __init__(self, ana_m3u_dosyasi):
        self.ana_m3u_dosyasi = ana_m3u_dosyasi
        self.httpx = Client(timeout=10, verify=False)
        self.referer_url = None

        # Tüm kanal ID’leri
        self.channel_ids = [
            "yayinzirve","yayin1","yayininat","yayinb2","yayinb3","yayinb4","yayinb5",
            "yayinbm1","yayinbm2","yayinss","yayinss2","yayint1","yayint2","yayint3",
            "yayinsmarts","yayinsms2","yayintrtspor","yayintrtspor2","yayintrt1",
            "yayinas","yayinatv","yayintv8","yayintv85","yayinf1","yayinnbatv",
            "yayineu1","yayineu2","yayinex1","yayinex2","yayinex3","yayinex4",
            "yayinex5","yayinex6","yayinex7","yayinex8"
        ]

        # M3U klasörünü oluştur
        os.makedirs(os.path.dirname(self.ana_m3u_dosyasi), exist_ok=True)

    # Çalışan referer URL bul
    def find_working_referer(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        for i in range(65, 105):
            test_domain = f"https://dengetv{i}.live/"
            print(f"🔍 {test_domain} kontrol ediliyor...")
            try:
                r = self.httpx.get(test_domain, headers=headers)
                if r.status_code == 200 and r.text.strip():
                    print(f"✅ Çalışan referer bulundu: {test_domain}")
                    self.referer_url = test_domain
                    return True
            except Exception as e:
                continue
        print("❌ Hiçbir referer bulunamadı!")
        return False

    # M3U içeriği oluştur
    def build_m3u_content(self):
        if not self.referer_url:
            print("❌ Referer bulunamadığı için M3U oluşturulamıyor.")
            return ""

        m3u_content = ["#EXTM3U"]
        for channel_id in self.channel_ids:
            channel_name = channel_id.capitalize()
            m3u_content.append(f'#EXTINF:-1 group-title="Dengetv54",{channel_name}')
            m3u_content.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u_content.append(f'#EXTVLCOPT:http-referrer={self.referer_url}')
            m3u_content.append(f"{self.referer_url}channel?id={channel_id}")
        return "\n".join(m3u_content)

    # M3U dosyasını kaydet
    def save_m3u(self, content):
        if not content:
            return
        with open(self.ana_m3u_dosyasi, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"💾 {self.ana_m3u_dosyasi} kaydedildi.")

    # Scripti çalıştır
    def calistir(self):
        if self.find_working_referer():
            m3u_content = self.build_m3u_content()
            self.save_m3u(m3u_content)
            print("✅ Tüm kanallar başarıyla M3U’ye eklendi.")


if __name__ == "__main__":
    manager = DengetvManager("M3U/osibusidengedeneme.m3u")
    manager.calistir()
