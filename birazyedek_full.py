import os
from datetime import datetime
from playwright.sync_api import sync_playwright

OUTPUT_FILE = "M3U/Osibusibirazfull.m3u"

class OSIsportsManager:
    def __init__(self, output_file):
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        self.output_file = output_file

    def get_latest_domain(self, start=27, max_attempts=100):
        from httpx import Client
        client = Client(timeout=10, verify=False)
        for i in range(max_attempts):
            number = start + i
            domain = f"https://birazcikspor{number}.xyz/"
            try:
                r = client.get(domain)
                if r.status_code == 200:
                    print(f"✅ Geçerli domain bulundu: {domain}")
                    return domain
            except Exception:
                continue
        fallback = f"https://birazcikspor{start}.xyz/"
        print(f"⚠️ Domain bulunamadı, varsayılan: {fallback}")
        return fallback

    def fetch_channels(self, domain):
        channels = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(domain, timeout=15000)
            page.wait_for_timeout(3000)  # sayfanın yüklenmesi için bekle
            frames = page.frames
            for frame in frames:
                src = frame.url
                if "androstreamlive" in src and src.endswith(".m3u8"):
                    channels.append(src)
            browser.close()
        return list(set(channels))  # benzersiz kanallar

    def build_m3u(self, channels):
        lines = ["#EXTM3U"]
        for url in channels:
            # kanal adını url'den al
            name = url.split("/")[-1].replace(".m3u8", "")
            lines.append(f'#EXTINF:-1 group-title="Birazcikspor", {name}')
            lines.append(url)
        lines.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return "\n".join(lines)

    def run(self):
        print("🚀 M3U dosyası oluşturuluyor...")
        domain = self.get_latest_domain()
        channels = self.fetch_channels(domain)
        print(f"✅ {len(channels)} kanal bulundu.")
        m3u_content = self.build_m3u(channels)

        # Mevcut dosyayı yedekle
        if os.path.exists(self.output_file):
            bak_name = self.output_file + "." + datetime.now().strftime("%Y%m%d_%H%M%S") + ".bak"
            os.rename(self.output_file, bak_name)
            print(f"💾 Mevcut M3U yedeklendi: {bak_name}")

        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print(f"✅ M3U dosyası '{self.output_file}' başarıyla oluşturuldu.")


if __name__ == "__main__":
    OSIsportsManager(OUTPUT_FILE).run()
