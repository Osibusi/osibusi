import os
import time
import random
from httpx import Client
import subprocess

class OSIsportsManager:
    def __init__(self, cikti_dosyasi="M3U/Osibusibiraz1.m3u", start_number=27, max_attempts=50):
        # Çalışma dizini + tam yol
        self.cikti_dosyasi = os.path.join(os.getcwd(), cikti_dosyasi)
        os.makedirs(os.path.dirname(self.cikti_dosyasi), exist_ok=True)

        self.client = Client(timeout=5, verify=False)
        self.start_number = start_number
        self.max_attempts = max_attempts

        # Kanal ID’leri
        self.channel_ids = [
            "androstreamlivebs1","androstreamlivebs2","androstreamlivebs3",
            "androstreamlivebs4","androstreamlivebs5","androstreamlivets1",
            "androstreamlivets2","androstreamlivets3","androstreamlivesm1",
            "androstreamlivesm2","androstreamlivees1","androstreamlivees2",
            "androstreamlivetb1","androstreamlivetb2","androstreamlivetb3",
            "androstreamlivetb4","androstreamlivetb5","androstreamlivefb",
            "androstreamlivetrt1","androstreamlivetrts","androstreamliveht",
            "androstreamlivechstream233","androstreamlivechstream234"
        ]

        # Kanal isimleri
        self.channel_names = {
            "androstreamlivebs1":"Beşiktaş Live 1",
            "androstreamlivebs2":"Beşiktaş Live 2",
            "androstreamlivebs3":"Beşiktaş Live 3",
            "androstreamlivebs4":"Beşiktaş Live 4",
            "androstreamlivebs5":"Beşiktaş Live 5",
            "androstreamlivets1":"Trabzonspor Live 1",
            "androstreamlivets2":"Trabzonspor Live 2",
            "androstreamlivets3":"Trabzonspor Live 3",
            "androstreamlivesm1":"Süper Lig 1",
            "androstreamlivesm2":"Süper Lig 2",
            "androstreamlivees1":"Espanyol Live 1",
            "androstreamlivees2":"Espanyol Live 2",
            "androstreamlivetb1":"Tivibu 1",
            "androstreamlivetb2":"Tivibu 2",
            "androstreamlivetb3":"Tivibu 3",
            "androstreamlivetb4":"Tivibu 4",
            "androstreamlivetb5":"Tivibu 5",
            "androstreamlivefb":"Fenerbahçe Live",
            "androstreamlivetrt1":"TRT 1",
            "androstreamlivetrts":"TRT Spor",
            "androstreamliveht":"HT Spor",
            "androstreamlivechstream233":"Channel 233",
            "androstreamlivechstream234":"Channel 234"
        }

        # Rastgele base URL’ler
        self.baseurls = [
            f"https://wandering-pond-{random.randint(1000,9999)}.andorrmaid278.workers.dev/checklist/",
            f"https://wandering-pond-{random.randint(1000,9999)}.andorrmaid278.workers.dev/checklist/"
        ]

        self.headers = {"User-Agent": "Mozilla/5.0"}

    # Rastgele domain
    def find_latest_domain(self):
        latest = f"https://birazcikspor{random.randint(self.start_number, self.start_number + self.max_attempts)}.xyz/"
        print(f"✅ Güncel domain seçildi: {latest}")
        return latest

    # Kanal URL çözümü
    def resolve_source_from_id(self, cid):
        if cid.startswith("androstreamlivechstream"):
            after = cid.replace("androstreamlivechstream","")
            return f"https://bllovdes.d4ssgk.su/o1/stream{after}/playlist.m3u8"
        elif cid.startswith("androstreamlive"):
            baseurl = random.choice(self.baseurls)
            return f"{baseurl}{cid}.m3u8"
        return None

    # M3U içeriği
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
        # Güncel domain ve timestamp + random ID ile içerik değişikliği garanti
        m3u.append(f'#EXTINF:-1 group-title="Birazcikspor", Güncel Domain')
        m3u.append(latest_domain)
        m3u.append(f'# Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}')
        m3u.append(f'# RandomID: {random.randint(100000,999999)}')
        return "\n".join(m3u)

    # Dosyayı güvenle yaz
    def write_m3u_file(self):
        print(f"⚠️ Dosya üzerine yazılıyor: {self.cikti_dosyasi}")
        m3u_content = self.build_m3u8_content()
        try:
            with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
                f.write(m3u_content)
            print(f"✅ M3U dosyası oluşturuldu/güncellendi.")
        except Exception as e:
            print(f"❌ Dosya yazılamadı: {e}")

    # Git commit & push (her durumda commit)
    def git_commit_and_push(self):
        try:
            subprocess.run(["git", "add", self.cikti_dosyasi], check=True)
            commit_msg = f"Update M3U: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(["git", "commit", "-m", commit_msg, "--allow-empty"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("✅ Git commit ve push tamamlandı.")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Git hatası: {e}")

    def run(self):
        print("🚀 M3U dosyası oluşturuluyor...")
        self.write_m3u_file()
        self.git_commit_and_push()

if __name__ == "__main__":
    manager = OSIsportsManager()
    manager.run()
