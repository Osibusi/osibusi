from httpx import Client
import os
import time
import random

class OSIsportsManager:
    def __init__(self, cikti_dosyasi="M3U/Osibusibiraz1.m3u", start_number=27, max_attempts=50):
        os.makedirs(os.path.dirname(cikti_dosyasi), exist_ok=True)
        self.cikti_dosyasi = cikti_dosyasi
        self.client = Client(timeout=5, verify=False)
        self.start_number = start_number
        self.max_attempts = max_attempts

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

        # Baseurl'leri rastgele değiştirerek M3U içeriğini farklılaştırıyoruz
        self.baseurls = [
            f"https://wandering-pond-{random.randint(1000,9999)}.andorrmaid278.workers.dev/checklist/",
            f"https://wandering-pond-{random.randint(1000,9999)}.andorrmaid278.workers.dev/checklist/"
        ]

        self.headers = {"User-Agent": "Mozilla/5.0"}

    def find_latest_domain(self):
        """En güncel geçerli domaini bulur."""
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
        """Kanal ID'sinden M3U8 URL'si üretir."""
        if cid.startswith("androstreamlivechstream"):
            after = cid.replace("androstreamlivechstream", "")
            return f"https://bllovdes.d4ssgk.su/o1/stream{after}/playlist.m3u8"
        elif cid.startswith("androstreamlive"):
            index = self.channel_ids.index(cid) % len(self.baseurls)
            return f"{self.baseurls[index]}{cid}.m3u8"
        return None

    def build_m3u8_content(self):
        """M3U dosya içeriğini oluşturur."""
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

        # Zaman damgası içerikte kalsın, dosya adı değişmeden M3U her zaman güncel görünsün
        m3u.append(f'# Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}')
        return "\n".join(m3u)

    def calistir(self):
        print("🚀 M3U dosyası oluşturuluyor...")
        m3u_icerik = self.build_m3u8_content()
        # Dosya her çalıştırmada üzerine yazılıyor
        with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
            f.write(m3u_icerik)
        print(f"✅ M3U dosyası '{self.cikti_dosyasi}' başarıyla güncellendi.")

if __name__ == "__main__":
    OSIsportsManager().calistir()
