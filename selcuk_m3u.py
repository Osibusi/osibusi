import os
import time
import subprocess
import requests
from bs4 import BeautifulSoup

class SelcukSportsHD:
    def __init__(self, cikti_dosyasi="m3u/SelcukSportsHD.m3u", branch="main", max_retries=3, retry_delay=5):
        self.cikti_dosyasi = os.path.join(os.getcwd(), cikti_dosyasi)
        os.makedirs(os.path.dirname(self.cikti_dosyasi), exist_ok=True)
        self.base_url = "https://selcuksportshd.biz/"  # Örnek site
        self.branch = branch
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Git config (gerekiyorsa)
        subprocess.run(["git", "config", "--global", "user.email", "you@example.com"])
        subprocess.run(["git", "config", "--global", "user.name", "Your Name"])

    def fetch_channels(self):
        """Kanal listesini al ve m3u formatına ekle. Retry destekli."""
        m3u_content = ["#EXTM3U"]
        for attempt in range(1, self.max_retries + 1):
            try:
                r = requests.get(self.base_url, timeout=10)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, "html.parser")
                links = soup.find_all("a", {"data-url": True})

                if not links:
                    raise ValueError("⚠️ Kanal bulunamadı. Site değişmiş olabilir.")

                for a in links:
                    stream_url = a.get("data-url")
                    name_tag = a.find("div", class_="name")
                    channel_name = name_tag.text.strip() if name_tag else "Unknown"
                    m3u_content.append(f'#EXTINF:-1 group-title="SelcukSportsHD", {channel_name}')
                    m3u_content.append(stream_url)
                
                print(f"✅ Kanal listesi alındı ({len(links)} kanal).")
                return m3u_content

            except Exception as e:
                print(f"⚠️ Deneme {attempt}/{self.max_retries} başarısız: {e}")
                if attempt < self.max_retries:
                    print(f"⏳ {self.retry_delay} saniye sonra tekrar denenecek...")
                    time.sleep(self.retry_delay)
                else:
                    print("❌ Maksimum deneme sayısına ulaşıldı. İşlem iptal edildi.")
                    return m3u_content  # Boş olsa da dön

    def write_m3u(self, m3u_content):
        with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
            f.write("\n".join(m3u_content))
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

    def run_once(self):
        print("🚀 M3U dosyası oluşturuluyor ve Git ile entegre ediliyor...")
        m3u_content = self.fetch_channels()
        self.write_m3u(m3u_content)
        self.git_commit_and_push()
        print("✅ İşlem tamamlandı.")

if __name__ == "__main__":
    manager = SelcukSportsHD()
    while True:
        manager.run_once()
        print("⏰ 3 saat bekleniyor...")
        time.sleep(3 * 60 * 60)  # 3 saat bekle
