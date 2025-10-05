import os
import time
import random
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

        self.channel_ids = [
            "androstreamlivebs1": "BeinSpor 1","androstreamlivebs2": "BeinSpor 2","androstreamlivebs3": "BeinSpor 3",
            "androstreamlivebs4","androstreamlivebs5","androstreamlivets1",
            "androstreamlivets2","androstreamlivets3","androstreamlivesm1",
            "androstreamlivesm2","androstreamlivees1","androstreamlivees2",
            "androstreamlivetb1","androstreamlivetb2","androstreamlivetb3",
            "androstreamlivetb4","androstreamlivetb5","androstreamlivefb",
            "androstreamlivetrt1","androstreamlivetrts","androstreamliveht",
            "androstreamlivechstream233","androstreamlivechstream234"
        ]

        self.baseurls = [
            f"https://wandering-pond-{random.randint(1000,9999)}.andorrmaid278.workers.dev/checklist/",
            f"https://wandering-pond-{random.randint(1000,9999)}.andorrmaid278.workers.dev/checklist/"
        ]

        self.headers = {"User-Agent": "Mozilla/5.0"}

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
            return f"{self.baseurls[index]}{cid}.m3u8"
        return None

    def build_m3u8_content(self):
        m3u = ["#EXTM3U"]
        latest_domain = self.find_latest_domain()
        for cid in self.channel_ids:
            stream_url = self.resolve_source_from_id(cid)
            if not stream_url:
                continue
            channel_name = cid.replace("-", " ").title()
            m3u.append(f'#EXTINF:-1 group-title="Birazcikspor", {channel_name}')
            m3u.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u.append(stream_url)
        if latest_domain:
            m3u.append(f'#EXTINF:-1 group-title="Birazcikspor", Güncel Domain')
            m3u.append(latest_domain)
        m3u.append(f'# Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}')
        return "\n".join(m3u)

    def write_m3u_file(self):
        # Eğer dosya yoksa veya eski dosya silinmişse yeniden oluştur
        if not os.path.exists(self.cikti_dosyasi):
            print("⚠️ M3U dosyası bulunamadı, yeniden oluşturuluyor...")
        m3u_content = self.build_m3u8_content()
        with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print(f"✅ M3U dosyası '{self.cikti_dosyasi}' oluşturuldu/güncellendi.")

    def git_commit_and_push(self):
        try:
            subprocess.run(["git", "add", self.cikti_dosyasi], check=True)
            commit_msg = f"Update M3U: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("✅ Git commit ve push işlemi tamamlandı.")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Git işlemlerinde hata: {e}")

    def run(self):
        print("🚀 M3U dosyası oluşturuluyor ve Git ile entegre ediliyor...")
        self.write_m3u_file()
        self.git_commit_and_push()

if __name__ == "__main__":
    manager = OSIsportsManager()
    manager.run()
