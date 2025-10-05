import os
import time
import requests
from bs4 import BeautifulSoup

class SelcukSportsHD:
    def __init__(self, cikti_dosyasi="M3U/SelcukSportsHD.m3u"):
        self.cikti_dosyasi = os.path.join(os.getcwd(), cikti_dosyasi)
        os.makedirs(os.path.dirname(self.cikti_dosyasi), exist_ok=True)
        self.base_url = "https://selcuksportshd.biz/"  # Örnek site
        self.m3u_content = ["#EXTM3U"]

    def fetch_channels(self):
        try:
            r = requests.get(self.base_url, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")

            # Tüm channel linklerini bul
            links = soup.find_all("a", {"data-url": True})
            for a in links:
                stream_url = a.get("data-url")
                name_tag = a.find("div", class_="name")
                channel_name = name_tag.text.strip() if name_tag else "Unknown"
                self.m3u_content.append(f'#EXTINF:-1 group-title="SelcukSportsHD", {channel_name}')
                self.m3u_content.append(stream_url)

        except Exception as e:
            print(f"⚠️ Kanal bilgisi alınamadı: {e}")

    def write_m3u(self):
        with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
            f.write("\n".join(self.m3u_content))
        print(f"✅ M3U dosyası oluşturuldu: {self.cikti_dosyasi}")

    def run(self):
        print("🚀 M3U dosyası oluşturuluyor...")
        self.fetch_channels()
        self.write_m3u()
        print("✅ İşlem tamamlandı.")

if __name__ == "__main__":
    manager = SelcukSportsHD()
    manager.run()
