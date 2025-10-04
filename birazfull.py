import os
import requests
from bs4 import BeautifulSoup

class OSIsportsManager:
    def __init__(self, cikti_dosyasi, start_number=27, max_attempts=150):
        os.makedirs(os.path.dirname(cikti_dosyasi), exist_ok=True)
        self.cikti_dosyasi = cikti_dosyasi
        self.start_number = start_number
        self.max_attempts = max_attempts

    def find_latest_domain(self):
        """En güncel 'birazciksporXX.xyz' domainini bul"""
        for i in range(self.max_attempts):
            number = self.start_number + i
            domain = f"https://birazcikspor{number}.xyz/"
            try:
                r = requests.get(domain, timeout=5)
                if r.status_code == 200:
                    print(f"✅ Geçerli domain bulundu: {domain}")
                    return domain
            except Exception:
                continue
        fallback = f"https://birazcikspor{self.start_number}.xyz/"
        print(f"⚠️ Güncel domain bulunamadı, varsayılan kullanılıyor: {fallback}")
        return fallback

    def fetch_channel_ids(self, domain):
        """Sayfadaki iframe ID’lerini çek"""
        try:
            r = requests.get(domain, timeout=10)
            r.raise_for_status()
        except Exception as e:
            print(f"⚠️ Domain erişim hatası: {e}")
            return []

        soup = BeautifulSoup(r.text, "html.parser")
        channel_ids = []

        for iframe in soup.find_all("iframe"):
            src = iframe.get("src")
            if src and "id=" in src:
                cid = src.split("id=")[1]
                channel_ids.append(cid)
        return channel_ids

    def build_m3u8_content(self, channel_ids):
        m3u = ["#EXTM3U"]
        baseurl = "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/"

        for cid in channel_ids:
            stream_url = f"{baseurl}{cid}.m3u8"
            m3u.append(f'#EXTINF:-1 group-title="Birazcikspor", {cid}')
            m3u.append(stream_url)
        return "\n".join(m3u)

    def calistir(self):
        print("🚀 M3U dosyası oluşturuluyor...")
        domain = self.find_latest_domain(
