import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ======================================================
# 🔍 Geçerli domain bulma
# ======================================================
def find_latest_domain():
    base = "https://birazcikspor"
    for i in range(200, 0, -1):
        for suffix in ["", "1"]:
            url = f"{base}{i}{suffix}.xyz/"
            try:
                r = requests.get(url, timeout=5)
                if r.status_code == 200 and "iframe" in r.text:
                    print(f"✅ Geçerli domain bulundu: {url}")
                    return url
            except requests.RequestException:
                continue
    print("⚠️ Geçerli domain bulunamadı.")
    return None

# ======================================================
# 📡 Kanal listesini çek
# ======================================================
def extract_channels(domain):
    try:
        r = requests.get(domain, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        iframes = soup.find_all("iframe")

        channels = []
        for iframe in iframes:
            src = iframe.get("src", "")
            match = re.search(r"id=([a-zA-Z0-9_-]+)", src)
            if match:
                cid = match.group(1)
                if cid.startswith("androstreamlive"):
                    channels.append(cid)

        print(f"✅ {len(channels)} kanal bulundu.")
        return list(set(channels))
    except Exception as e:
        print(f"❌ Kanal çekme hatası: {e}")
        return []

# ======================================================
# 🧾 M3U dosyasını oluştur
# ======================================================
def save_m3u(channels):
    os.makedirs("M3U", exist_ok=True)
    m3u_path = "M3U/Osibusibirazfull.m3u"

    # Eski dosyayı yedekle
    if os.path.exists(m3u_path):
        backup = f"{m3u_path}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
        os.rename(m3u_path, backup)
        print(f"💾 Mevcut M3U dosyası yedeklendi: {backup}")

    with open(m3u_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in channels:
            url = f"https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/{ch}.m3u8"
            f.write(f'#EXTINF:-1 group-title="Birazcikspor", {ch}\n{url}\n')
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"✅ M3U dosyası '{m3u_path}' başarıyla oluşturuldu.")

# ======================================================
# 🚀 Ana akış
# ======================================================
def main():
    print("\n🚀 M3U dosyası oluşturuluyor...")
    domain = find_latest_domain()
    if not domain:
        return
    channels = extract_channels(domain)
    if channels:
        save_m3u(channels)
    else:
        print("⚠️ Hiç kanal bulunamadı.")

if __name__ == "__main__":
    main()
