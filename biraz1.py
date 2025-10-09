import os
import time
import random
import re
from httpx import Client
import subprocess

class OSIsportsManager:
    def __init__(self, cikti_dosyasi="M3U/Osibusibiraz1.m3u", start_number=27, max_attempts=50):
        # Dizini oluştur
        os.makedirs(os.path.dirname(cikti_dosyasi), exist_ok=True)
        self.cikti_dosyasi = cikti_dosyasi
        self.client = Client(timeout=5, verify=False)
        self.start_number = start_number
        self.max_attempts = max_attempts

      
        # Kanal ID’leri
        self.channel_ids = [
            "androstreamlivebs1", "androstreamlivebs2", "androstreamlivebs3",
            "androstreamlivebs4", "androstreamlivebs5", "androstreamlivebsm1",
            "androstreamlivebsm2", "androstreamlivets1", "androstreamlivets2",
            "androstreamlivets3", "androstreamlivesm1", "androstreamlivesm2",
            "androstreamlivees1", "androstreamlivees2", "androstreamlivetb1",
            "androstreamlivetb2", "androstreamlivetb3", "androstreamlivetb4",
            "androstreamlivetb5", "androstreamlivess1", "androstreamlivess2",
            "androstreamlivefb", "androstreamlivetrt1", "androstreamlivetv8",
            "androstreamlivetrts", "androstreamliveht", "androstreamlivetjk",
            "androstreamlivea2", "androstreamlivecbcs","androstreamliveexn1",
            "androstreamliveexn2","androstreamliveexn3","androstreamliveexn4",
            "androstreamliveexn5","androstreamliveexn6","androstreamliveexn7",
            "androstreamliveexn8","androstreamliveidm",
        ]

        # Kanal isimleri
        self.channel_names = {
            "androstreamlivebs1": "Bein Spor Live 1",
            "androstreamlivebs2": "Bein Spor Live 2",
            "androstreamlivebs3": "Bein Spor Live 3",
            "androstreamlivebs4": "Bein Spor Live 4",
            "androstreamlivebs5": "Bein Spor Live 5",
            "androstreamlivebsm1": "Bein Spor Max 1",
            "androstreamlivebsm2": "Bein Spor Max 2",
            "androstreamlivets1": "Tivibu Spor 1",
            "androstreamlivets2": "Tivibu Spor 2",
            "androstreamlivets3": "Tivibu Spor 3",
            "androstreamlivesm1": "Smart Spor 1",
            "androstreamlivesm2": "Smart Spor 2",
            "androstreamlivees1": "Eurosport 1",
            "androstreamlivees2": "Eurosport 2",
            "androstreamlivetb1": "Tabi 1",
            "androstreamlivetb2": "Tabi 2",
            "androstreamlivetb3": "Tabi 3",
            "androstreamlivetb4": "Tabi 4",
            "androstreamlivetb5": "Tabi 5",
            "androstreamlivess1": "Sports 1",
            "androstreamlivess2": "Sports 2",
            "androstreamlivefb": "® Fenerbahçe Live",
            "androstreamlivetrt1": "TRT 1",
            "androstreamlivetv8": "TV8",
            "androstreamlivetrts": "TRT Spor",
            "androstreamliveht": "HT Spor",
            "androstreamlivetjk": "AT TV ",
            "androstreamlivea2": "A2",
            "androstreamlivecbcs": "Cbc sport",
            "androstreamliveexn1": "EXXEN 1",
            "androstreamliveexn2": "EXXEN 2",
            "androstreamliveexn3": "EXXEN 3",
            "androstreamliveexn4": "EXXEN 4",
            "androstreamliveexn5": "EXXEN 5",
            "androstreamliveexn6": "EXXEN 6",
            "androstreamliveexn7": "EXXEN 7",
            "androstreamliveexn8": "EXXEN 8",
            "androstreamliveidm": "IDMAN TV",
         
        }

        self.baseurls = [
            f"https://wandering-pond-{random.randint(1000,9999)}.androsd2390asd.workers.dev/checklist/",
            f"https://wandering-pond-{random.randint(1000,9999)}.androsd2390asd.workers.dev/checklist/"
        ]

        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.worker_base = self.detect_worker_base()  # Otomatik güncel worker ID

    def detect_worker_base(self):
        """Sitedeki güncel worker ID’yi tespit eder"""
        test_url = "https://wandering-pond-ff44.androsd2390asd.workers.dev/checklist/"
        try:
            r = self.client.get(test_url, headers=self.headers)
            match = re.search(r"https://wandering-pond-([0-9a-z]+)\.androsd2390asd\.workers\.dev", r.text)
            if match:
                worker_id = match.group(1)
                print(f"✅ Güncel worker ID bulundu: {worker_id}")
                return f"https://wandering-pond-{worker_id}.androsd2390asd.workers.dev/checklist/"
        except Exception as e:
            print(f"⚠️ Worker ID tespiti başarısız: {e}")
        return "https://wandering-pond-ff44.androsd2390asd.workers.dev/checklist/"

    def setup_git_identity(self):
        """CI ortamında git commit için kullanıcı bilgilerini ayarlar"""
        try:
            subprocess.run(["git", "config", "user.name", "OSIsportsBot"], check=True)
            subprocess.run(["git", "config", "user.email", "osibot@example.com"], check=True)
            print("🔧 Git kimliği ayarlandı.")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Git kimliği ayarlanamadı: {e}")

    def find_latest_domain(self):
        for i in range(self.start_number, self.start_number + self.max_attempts):
            domain = f"https://birazcikspor{i}.xyz/"
            try:
                r = self.client.head(domain, headers=self.headers, timeout=5)
                if r.status_code == 200:
                    print(f"✅ Geçerli domain bulundu: {domain}")
                    return domain
            except Exception:
                continue
        print("⚠️ Geçerli domain bulunamadı.")
        return None

    def resolve_source_from_id(self, cid):
        if cid.startswith("androstreamlivechstream"):
            after = cid.replace("androstreamlivechstream", "")
            return f"https://bllovdes.d4ssgk.su/o1/stream{after}/playlist.m3u8"
        elif cid.startswith("androstreamlive"):
            index = self.channel_ids.index(cid) % len(self.baseurls)
            return f"{self.worker_base}{cid}.m3u8"
        return None

    def build_m3u8_content(self):
        m3u = ["#EXTM3U"]
        latest_domain = self.find_latest_domain()
        for cid in self.channel_ids:
            stream_url = self.resolve_source_from_id(cid)
            if not stream_url:
                continue
            channel_name = self.channel_names.get(cid, cid.replace("-", " ").title())
            m3u.append(f'#EXTINF:-1 group-title="Birazcikspor", {channel_name}')
            m3u.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u.append(stream_url)
        if latest_domain:
            m3u.append(f'#EXTINF:-1 group-title="Birazcikspor_OSI", Güncel Domain')
            m3u.append(latest_domain)
        m3u.append(f'# Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}')
        return "\n".join(m3u)

    def write_m3u_file(self):
        if not os.path.exists(self.cikti_dosyasi):
            print("⚠️ M3U dosyası bulunamadı, yeniden oluşturuluyor...")
        else:
            print(f"⚠️ Dosya üzerine yazılıyor: {self.cikti_dosyasi}")
        m3u_content = self.build_m3u8_content()
        with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print(f"✅ M3U dosyası '{self.cikti_dosyasi}' oluşturuldu/güncellendi.")

    def git_commit_and_push(self):
        try:
            subprocess.run(["git", "add", self.cikti_dosyasi], check=True)
            commit_msg = f"Update M3U: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(["git", "commit", "--allow-empty", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("✅ Git commit ve push tamamlandı.")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Git hatası: {e}")

    def run(self):
        print("🚀 M3U dosyası oluşturuluyor ve Git ile entegre ediliyor...")
        self.setup_git_identity()
        self.write_m3u_file()
        self.git_commit_and_push()

if __name__ == "__main__":
    manager = OSIsportsManager()
    manager.run()
