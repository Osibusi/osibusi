import requests
from bs4 import BeautifulSoup
import os

class OSIsportsManager:
    def __init__(self, cikti_dosyasi, start_number=27, max_attempts=100):
        # M3U klasörü yoksa oluştur
        os.makedirs(os.path.dirname(cikti_dosyasi), exist_ok=True)
        self.cikti_dosyasi = cikti_dosyasi
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.start_number = start_number
        self.max_attempts = max_attempts

    def find_latest_domain(self):
        """En güncel domaini bulur"""
        for i in range(self.max_attempts):
            number = self.start_number + i
            domain = f"https://birazcikspor{number}.xyz/"
            try:
                r = requests.get(domain, headers=self.headers, timeout=5)
                if r.status_code == 200:
                    print(f"✅ Geçerli domain bulundu: {domain}")
                    return domain
            except:
                continue
        fallback = f"https://birazcikspor{self.start_number}.xyz/"
        print(f"⚠️ Güncel domain bulunamadı, varsayılan kullanılıyor: {fallback}")
        return fallback

    def fetch_channel_links(self, domain):
        """Domain sayfasındaki tüm m3u8 kanallarını çeker"""
        try:
            r = requests.get(domain, headers=self.headers, timeout=5)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            channels = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href.endswith(".m3u8"):
                    channels.append(href)
            print(f"✅ {len(channels)} kanal bulundu.")
            return channels
        except Exception as e:
            print(f"⚠️ Kanal listesi çekilemedi: {e}")
            return []

    def build_m3u8_content(self):
        domain = self.find_latest_domain()
        channels = self.fetch_channel_links(domain)
        m3u = ["#EXTM3U"]
        for idx, url in enumerate(channels, 1):
            m3u.append(f'#EXTINF:-1 group-title="Birazcikspor", Kanal {idx}')
            m3u.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u.append(url)
        return "\n".join(m3u)

    def calistir(self):
        print("🚀 M3U dosyası oluşturuluyor...")
        m3u_icerik = self.build_m3u8_content()
        with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
            f.write(m3u_icerik)
        print(f"✅ M3U dosyası '{self.cikti_dosyasi}' başarıyla oluşturuldu.")

if __name__ == "__main__":
    OSIsportsManager("M3U/Osibusibirazfull.m3u").calistir()
