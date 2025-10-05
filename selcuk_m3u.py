import os
import time
import subprocess
import requests
from bs4 import BeautifulSoup

class SelcukSportsHD:
    def __init__(self, cikti_dosyasi="M3U/SelcukSportsHD.m3u", branch="main"):
        self.cikti_dosyasi = os.path.join(os.getcwd(), cikti_dosyasi)
        os.makedirs(os.path.dirname(self.cikti_dosyasi), exist_ok=True)
        self.base_url = "https://selcuksportshd.biz/"  # Örnek site
        self.m3u_content = ["#EXTM3U"]
        self.branch = branch

        # Git config (gerekiyorsa)
        subprocess.run(["git", "config", "--global", "user.email", "you@example.com"])
        subprocess.run(["git", "config", "--global", "user.name", "Your Name"])

    def fetch_channels(self):
        try:
            r = requests.get(self.base_url, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")

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

    def git_commit_and_push(self):
        try:
            subprocess.run(["git", "add", self.cikti_dosyasi], check=True)
            commit_msg = f"Update M3U: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(["git", "commit", "-m", commit_msg, "--allow-empty"], check=True)
            subprocess.run(["git", "push", "origin", self.branch], check=True)
            print("✅ Git commit ve push tamamlandı.")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Git hatası: {e}")

    def run(self):
        print("🚀 M3U dosyası oluşturuluyor ve Git ile entegre ediliyor...")
        self.fetch_channels()
        self.write_m3u()
        self.git_commit_and_push()
        print("✅ Tüm işlemler tamamlandı.")

if __name__ == "__main__":
    manager = SelcukSportsHD()
    manager.run()
