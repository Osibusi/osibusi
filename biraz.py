from httpx import Client

class OSIsportsManager:
    def __init__(self, cikti_dosyasi):
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
            # İstersen burada diğer kanal ID’lerini ekleyebilirsin
        ]
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def resolve_source_from_id(self, cid):
        if cid.startswith("androstreamlivechstream"):
            after = cid.replace("androstreamlivechstream", "")
            if not after:
                return None
            return f"https://bllovdes.d4ssgk.su/o1/stream{after}/playlist.m3u8"
        elif cid.startswith("androstreamlive"):
            import random
            baseurl = random.choice(self.baseurls)
            return f"{baseurl}{cid}.m3u8"
        else:
            return None

    def build_m3u8_content(self):
        m3u = ["#EXTM3U"]
        for cid in self.channel_ids:
            stream_url = self.resolve_source_from_id(cid)
            if not stream_url:
                continue
            channel_name = cid.replace("-", " ").title()
            m3u.append(f'#EXTINF:-1 group-title="Birazcikspor", {channel_name}')
            m3u.append(f'#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u.append(f'{stream_url}')
        return "\n".join(m3u)

    def calistir(self):
        domain = "https://birazcikspor27./"
        print(f"Domain sabit olarak kullanılıyor: {domain}")

        # Sayfa içeriği kontrolü
        try:
            r = self.client.get(domain, headers=self.headers)
            if r.status_code != 200:
                raise RuntimeError(f"Domain erişildi ama HTTP {r.status_code} döndü.")
            if "androstreamlive" not in r.text:
                raise RuntimeError("Beklenen içerik domain sayfasında bulunamadı.")
        except Exception as e:
            raise RuntimeError(f"Domain erişiminde hata: {e}")

        # M3U içeriği oluşturuluyor
        m3u_icerik = self.build_m3u8_content()
        with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
            f.write(m3u_icerik)
        print(f"M3U dosyası '{self.cikti_dosyasi}' başarıyla oluşturuldu.")

if __name__ == "__main__":
    OSIsportsManager("Osibusibiraz.m3u").calistir()
