import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import requests
from datetime import datetime
import time

class OSIsportsManager:
    def __init__(self, cikti_dosyasi, start_number=27, max_attempts=150, wait_ms=15000, retry=3):
        os.makedirs(os.path.dirname(cikti_dosyasi), exist_ok=True)
        self.cikti_dosyasi = cikti_dosyasi
        self.start_number = start_number
        self.max_attempts = max_attempts
        self.wait_ms = wait_ms
        self.retry = retry

    def find_latest_domain(self):
        """En güncel domaini bul"""
        for i in range(self.max_attempts):
            number = self.start_number + i
            domain = f"https://birazcikspor{number}.xyz/"
            try:
                r = requests.get(domain, timeout=5)
                if r.status_code == 200:
                    print(f"✅ Geçerli domain bulundu: {domain}")
                    return domain
            except Exception as e:
                print(f"⚠️ Domain {domain} deneme hatası: {e}")
        fallback = f"https://birazcikspor{self.start_number}.xyz/"
        print(f"⚠️ Domain bulunamadı, varsayılan: {fallback}")
        return fallback

    def fetch_channel_ids(self, domain):
        """Playwright ile JS render sonrası tüm iframe ID’lerini al"""
        for attempt in range(1, self.retry + 1):
            print(f"🔄 Kanal çekme denemesi {attempt}/{self.retry}...")
            channel_ids = set()
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    page.goto(domain, timeout=20000)
                    page.wait_for_timeout(self.wait_ms)  # JS yüklemesi için bekle

                    # Tüm iframe elementlerini tara
                    iframes = page.query_selector_all("iframe")
                    for iframe in iframes:
                        src = iframe.get_attribute("src")
                        if src and "id=" in src:
                            cid = src.split("id=")[1]
                            channel_ids.add(cid)

                    browser.close()
                    if channel_ids:
                        return list(channel_ids)
            except PlaywrightTimeoutError:
                print("⚠️ Timeout oluştu, tekrar denenecek...")
            except Exception as e:
                print(f"⚠️ Playwright hatası: {e}")
            time.sleep(2)  # kısa bekleme ile retry
        print("⚠️ Kanal ID’leri alınamadı!")
        return []

    def build_m3u8_content(self, channel_ids):
        m3u = ["#EXTM3U"]
        baseurl = "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/"
        for cid in channel_ids:
            stream_url = f"{baseurl}{cid}.m3u8"
            m3u.append(f'#EXTINF:-1 group-title="Birazcikspor", {cid}')
            m3u.append(stream_url)
        m3u.append(f'# Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
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
