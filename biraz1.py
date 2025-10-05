from httpx import Client
import os
import random

class OSIsportsManager:
    def __init__(self, cikti_dosyasi="M3U/Osibusibiraz1.m3u", start_number=27, max_attempts=200):
        os.makedirs(os.path.dirname(cikti_dosyasi), exist_ok=True)
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
            "androstreamlivesm1",
            "androstreamlivesm2",
            "androstreamlivees1",
            "androstreamlivees2",
            "androstreamlivetb1",
            "androstreamlivetb2",
            "androstreamlivetb3",
            "androstreamlivetb4",
            "androstreamlivetb5",
            "androstreamlivefb",
            "androstreamlivechstream233",
            "androstreamlivechstream234",
        ]
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.start_number = start_number
        self.max_attempts = max_attempts

    def find_latest_domain(self):
        for i in range(self.max_attempts):
            number = self.start_number + i
            domain = f"https://birazcikspor{number}.xyz/"
            try:
                r = self.client.get(domain, headers=self.headers)
                if r.status_code == 200:
                    print(f"✅ Geçerli domain bulundu: {domain}")
                    return domain
            except Exception:
                continue
        fallback = f"https://birazcikspor{self.start_number}.xyz/"
        print(f"⚠️ Güncel domain bulunamadı, varsayılan kullanılıyor: {fallback}")
        return fallback

    def resolve_source_from_id(self, cid):
        if cid.startswith("androstreamlivechstream"):
            after = cid.replace("androstreamlivechstream", "")
            if not after:
                return None
            return f"https://bllovdes.d4ssgk.su/o1/stream{after}/playlist.m3u8"
        elif cid.startswith("androstreamlive"):
            baseurl = random.choice(self.baseurls)
            return f"{baseurl}{cid}.m3u8"
        else:
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
            # Eğer baseurl kullanılıyorsa güncel domain ile değiştir
            for base in self.baseurls:
                stream_url = stream_url.replace(base, latest_domain)
            m3u.append(stream_url)
        return "\n".join(m3u)

    def calistir(self):
        print("🚀 M3U dosyası oluşturuluyor...")
        m3u_icerik = self.build_m3u8_content()
        with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
            f.write(m3u_icerik)
        print(f"✅ M3U dosyası '{self.cikti_dosyasi}' başarıyla oluşturuldu.")


if __name__ == "__main__":
    OSIsportsManager().calistir()
