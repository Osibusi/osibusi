import os
from playwright.sync_api import sync_playwright
import requests
from datetime import datetime
import re
import shutil
import time

class OSIsportsManager:
    def __init__(self, cikti_dosyasi, start_number=27, max_attempts=150, wait_ms=20000, retry=3):
        os.makedirs(os.path.dirname(cikti_dosyasi), exist_ok=True)
        self.cikti_dosyasi = cikti_dosyasi
        self.start_number = start_number
        self.max_attempts = max_attempts
        self.wait_ms = wait_ms
        self.retry = retry
        self.baseurls = [
            "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/",
            "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/"
        ]

    def backup_existing_m3u(self):
        if os.path.exists(self.cikti_dosyasi):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{self.cikti_dosyasi}.{timestamp}.bak"
            shutil.copy2(self.cikti_dosyasi, backup_file)
            print(f"💾 Mevcut M3U dosyası yedeklendi: {backup_file}")

    def find_latest_domain(self):
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
        print(f"⚠️ Domain bulunamadı, varsayılan: {fallback}")
        return fallback

    def fetch_channel_ids(self, domain):
        for attempt in range(1, self.retry + 1):
            print(f"🔄 Kanal çekme denemesi {attempt}/{self.retry}...")
            channel_ids = set()
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    page.goto(domain, timeout=30000)
                    page.wait_for_timeout(self.wait_ms)

                    # iframe src içindeki id parametrelerini al
                    iframes = page.query_selector_all("iframe")
                    for iframe in iframes:
                        src = iframe.get_attribute("src")
                        if src and "id=" in src:
                            cid = re.search(r"id=(androstreamlive\w+)", src)
                            if cid:
                                channel_ids.add(cid.group(1))

                    # script içindeki id parametrelerini tara
                    scripts = page.query_selector_all("script")
                    for script in scripts:
                        content = script.inner_html()
                        matches = re.findall(r"id=(androstreamlive\w+)", content)
                        channel_ids.update(matches)

                    browser.close()
                    if channel_ids:
                        return sorted(channel_ids)
            except Exception as e:
                print(f"⚠️ Playwright hatası: {e}")
            time.sleep(2)
        print("⚠️ Kanal ID’leri alınamadı!")
        return []

    def resolve_source_from_id(self, cid):
        if cid.startswith("androstreamlivech"):
            afterCh = cid.replace("androstreamlivech", "")
            if not afterCh:
                return None
            return f"https://bllovdes.d4ssgk.su/o1/{afterCh}/playlist.m3u8"
        elif cid.startswith("androstreamlive"):
            import random
            baseurl = random.choice(self.baseurls)
            return f"{baseurl}{cid}.m3u8"
        else:
            return None

    def build_m3u8_content(self, channel_ids):
        m3u = ["#EXTM3U"]
        for cid in channel_ids:
            stream_url = self.resolve_source_from_id(cid)
            if not stream_url:
                continue
            m3u.append(f'#EXTINF:-1 group-title="Birazcikspor", {cid}')
            m3u.append(stream_url)
        m3u.append(f'# Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        return "\n".join(m3u)

    def calistir(self):
        print("🚀 M3U dosyası oluşturuluyor...")
        self.backup_existing_m3u()
        domain = self.find_latest_domain()
        channel_ids = self.fetch_channel_ids(domain)
        print(f"✅ {len(channel_ids)} kanal bulundu.")
        m3u_content = self.build_m3u8_content(channel_ids)
        with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print(f"✅ M3U dosyası '{self.cikti_dosyasi}' başarıyla oluşturuldu.")

if __name__ == "__main__":
    OSIsportsManager("M3U/Osibusibirazfull.m3u").calistir()
