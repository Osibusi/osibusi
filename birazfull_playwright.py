import os
from playwright.sync_api import sync_playwright
import requests

class OSIsportsManager:
    def __init__(self, cikti_dosyasi, start_number=27, max_attempts=150):
        os.makedirs(os.path.dirname(cikti_dosyasi), exist_ok=True)
        self.cikti_dosyasi = cikti_dosyasi
        self.start_number = start_number
        self.max_attempts = max_attempts

    def find_latest_domain(self):
        for i in range(self.max_attempts):
            number = self.start_number + i
            domain = f"https://birazcikspor{number}.xyz/"
            try:
                r = requests.get(domain, timeout=5)
                if r.status_code == 200:
                    print(f"✅ Geçerli domain bulundu: {domain}")
                    return domain
            except:
                continue
        fallback = f"https://birazcikspor{self.start_number}.xyz/"
        print(f"⚠️ Domain bulunamadı, varsayılan: {fallback}")
        return fallback

    def fetch_channel_ids(self, domain):
        """Playwright ile JS render sonrası iframe ID’lerini al"""
        channel_ids = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(domain, timeout=15000)
            page.wait_for_timeout(5000)  # JS yüklemesi için bekle

            iframes = page.query_selector_all("iframe")
            for iframe in iframes:
                src = iframe.get_attribute("src")
                if src and "id=" in src:
                    cid = src.split("id=")[1]
                    channel_ids.append(cid)
            browser.close()
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
        domain = self.find_latest_domain()
        channel_ids = self.fetch_channel_ids(domain)
        print(f"✅ {len(channel_ids)} kanal bulundu.")
        m3u_content = self.build_m3u8_content(channel_ids)
        with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print(f"✅ M3U dosyası '{self.cikti_dosyasi}' başarıyla oluşturuldu.")


if __name__ == "__main__":
    OSIsportsManager("M3U/Osibusibirazfull.m3u").calistir()
