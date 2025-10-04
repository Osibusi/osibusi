from httpx import Client
import os
from datetime import datetime

class OSIsportsManager:
    def __init__(self, cikti_dosyasi):
        os.makedirs(os.path.dirname(cikti_dosyasi), exist_ok=True)
        self.cikti_dosyasi = cikti_dosyasi
        self.channel_ids = [
            "androstreamlivebiraz1",
            "androstreamlivebs1",
            "androstreamlivebs2",
            "androstreamlivebs3",
        ]
        self.baseurls = [
            "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/",
        ]
        self.client = Client(timeout=10, verify=False)

    def resolve_source_from_id(self, cid):
        import random
        baseurl = random.choice(self.baseurls)
        return f"{baseurl}{cid}.m3u8"

    def build_m3u8_content(self):
        m3u = ["#EXTM3U"]
        for cid in self.channel_ids:
            url = self.resolve_source_from_id(cid)
            m3u.append(f'#EXTINF:-1 group-title="Birazcikspor", {cid}')
            m3u.append(url)
        m3u.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return "\n".join(m3u)

    def calistir(self):
        m3u_icerik = self.build_m3u8_content()
        with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
            f.write(m3u_icerik)
        print(f"✅ M3U dosyası '{self.cikti_dosyasi}' başarıyla oluşturuldu.")

if __name__ == "__main__":
    OSIsportsManager("M3U/Osibusi_birazyedek.m3u").calistir()
