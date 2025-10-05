import os
import time
import httpx
from bs4 import BeautifulSoup

M3U_PATH = os.path.join(os.getcwd(), "M3U/selcuksports.m3u")
URL = "https://sohbetdj.xyz/selcuksports/selcuksports_elwyj.html"

os.makedirs(os.path.dirname(M3U_PATH), exist_ok=True)

def fetch_channels():
    """Web sayfasından tüm canlı yayın linklerini çek"""
    try:
        with httpx.Client(timeout=15) as client:
            r = client.get(URL)
            r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("ul li a[data-url]")

        channels = []
        for item in items:
            name_tag = item.select_one(".name")
            time_tag = item.select_one("time")
            url = item['data-url']
            name = name_tag.text.strip() if name_tag else "Unknown"
            start_time = time_tag.text.strip() if time_tag else ""
            channels.append((name, url, start_time))
        return channels
    except Exception as e:
        print(f"⚠️ Yayınlar çekilemedi: {e}")
        return []

def build_m3u(channels):
    """M3U formatını oluştur"""
    lines = ["#EXTM3U"]
    for name, url, start_time in channels:
        lines.append(f'#EXTINF:-1 group-title="Selcuksports", {name} {start_time}')
        lines.append(url)
    return "\n".join(lines)

def write_m3u(content):
    with open(M3U_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ M3U dosyası güncellendi: {M3U_PATH}")

def main():
    while True:
        print("🚀 Yayınlar çekiliyor ve M3U güncelleniyor...")
        channels = fetch_channels()
        if channels:
            m3u_content = build_m3u(channels)
            write_m3u(m3u_content)
        else:
            print("⚠️ Yayın bulunamadı.")
        print("⏳ 3 saat bekleniyor...")
        time.sleep(3 * 3600)  # 3 saat

if __name__ == "__main__":
    main()
