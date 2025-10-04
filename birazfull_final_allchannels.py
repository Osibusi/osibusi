from httpx import Client
from bs4 import BeautifulSoup
import os

class OSIsportsManager:
    def __init__(self, cikti_dosyasi):
        os.makedirs(os.path.dirname(cikti_dosyasi), exist_ok=True)
        self.cikti_dosyasi = cikti_dosyasi
        self.client = Client(timeout=10, verify=False)
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def find_latest_domain(self, start=27, max_attempts=150):
        for i in range(max_attempts):
            domain = f"https://birazcikspor{start + i}.xyz/"
            try:
                r = self.client.get(domain, headers=self.headers)
                if r.status_code == 200:
                    return domain
            except Exception:
                continue
        return f"https://birazcikspor{start}.xyz/"

    def fetch_channels(self, domain):
        # Playwright veya httpx + BeautifulSoup ile tüm iframe id'lerini çek
        # Bu örnek basit
        return ["androstreamlivebiraz1", "androstreamlivebs1"]

    def build_m3u(self, channels):
        m3u = ["#EXTM3U"]
        for cid in channels:
            m3u.append(f'#EXTINF:-1 group-title="Birazcikspor", {cid}')
            m3u.append(f'https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/{cid}.m3u8')
        return "\n".join(m3u)

    def run(self):
        domain = self.find_latest_domain()
        channels = self.fetch_channels(domain)
        content = self.build_m3u(channels)
        with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"M3U dosyası '{self.cikti_dosyasi}' oluşturuldu.")

if __name__ == "__main__":
    OSIsportsManager("M3U/Osibusibirazfull.m3u").run()
