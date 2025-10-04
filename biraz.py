from httpx import Client
from datetime import datetime
import random
import time
import os

class OSIsportsManager:
    def __init__(self, cikti_dosyasi="Osibusibiraz.m3u"):
        self.cikti_dosyasi = cikti_dosyasi
        self.client = Client(timeout=10, verify=False)
        self.baseurls = [
            "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/",
            "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/"
        ]
        self.channel_ids = [
            "androstreamlivebs1",
            "androstreamlivebs2",
            "androstreamlivebs3",
            "androstreamlivebs4",
            "androstreamlivebs5",
            "androstreamlivets1",
            "androstreamlivets2",
            "androstreamlivets3",
            "androstreamlivechstream233",
            "androstreamlivechstream234",
        ]
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def resolve_source_from_id(self, cid):
        random.seed(time.time())
        if cid.startswith("androstreamlivechstream"):
            after = cid.replace("androstreamlivechstream", "")
            if not after:
                return None
            return f"https://bllovdes.d4ssgk.su/o1/stream{after}/playlist.m3u8"
        elif cid.startswith("androstreamlive"):
            baseurl = random.choice(self.baseurls)
            return f"{baseurl}{cid}.m3u8"
        return None

    def build_m3u8_content(self):
        m3u = ["#EXTM3U"]
        for cid in self.channel_ids:
            stream_url = self.resolve_source_from_id(cid)
            if not stream_url:
                continue
            channel_name = cid.replace("-", " ").title()
            m3u.append(f'#EXTINF:-1 group-title="Birazcikspor", {channel_name}')
            m3u.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u.append(stream_url)
        return "\n".join(m3u)

    def calistir(self):
        domain = "https://birazcikspor27./"
        print(f"🌐 Domain sabit olarak kullanılıyor: {domain}")

        try:
            r = self.client.get(domain, headers=self.headers)
            if r.status_code != 200:
                raise RuntimeError(f"Domain erişildi ama HTTP {r.status_code} döndü.")
            if "androstreamlive" not in r.text:
                raise RuntimeError("Beklenen içerik domain sayfasında bulunamadı.")
        except Exception as e:
            print(f"⚠️ Domain erişiminde hata: {e}")
            print("❗ Domain erişimi başarısız olsa bile M3U dosyası üretilecek...")

        # M3U içeriği oluştur
        m3u_icerik = self.build_m3u8_content()

        # Güncelleme tarihi etiketi ekle
        tarih_satiri = "# Güncellendi: " + datetime.now().isoformat()
        m3u_icerik = m3u_icerik + "\n" + tarih_satiri + "\n"

        # 📁 Dosya yoksa otomatik oluştur
        os.makedirs(os.path.dirname(self.cikti_dosyasi) or ".", exist_ok=True)

        with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
            f.write(m3u_icerik)

        print(f"✅ M3U dosyası '{self.cikti_dosyasi}' başarıyla oluşturuldu ve güncellendi.")


if __name__ == "__main__":
    OSIsportsManager 
