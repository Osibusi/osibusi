import httpx
import random

class XYZsportsManager:
    def __init__(self, cikti_dosyasi):
        self.cikti_dosyasi = cikti_dosyasi
        self.client = httpx.Client(timeout=10, verify=False)
        self.channel_ids = [
            "androstreamlivebs1",
            "androstreamlivebs2",
            "androstreamlivechstream233",
            "androstreamlivechstream234"
            # Kanal listesini ihtiyaç halinde buraya ekle
        ]
        self.baseurls = [
            "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/",
            "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/"
        ]

    def find_working_domain(self, start=1, end=500):
        headers = {"User-Agent": "Mozilla/5.0"}
        for i in range(start, end+1):
            url = f"https://birazcikspor{i}.xyz/"
            print(f"Deniyor: {url}")
            try:
                r = self.client.get(url, headers=headers)
                if r.status_code == 200 and "clappr.min.js" in r.text:
                    print(f"Çalışan domain bulundu: {url}")
                    return url
            except Exception as e:
                print(f"Hata: {e}")
        return None

    def resolve_stream_url(self, id_):
        if id_.startswith("androstreamlivechstream"):
            stream_no = id_.replace("androstreamlivechstream", "")
            return f"https://bllovdes.d4ssgk.su/o1/{stream_no}/playlist.m3u8"
        elif id_.startswith("androstreamlive"):
            baseurl = random.choice(self.baseurls)
            return f"{baseurl}{id_}.m3u8"
        else:
            return None

    def build_m3u8(self, referer_url):
        lines = ["#EXTM3U"]
        for cid in self.channel_ids:
            stream_url = self.resolve_stream_url(cid)
            if not stream_url:
                print(f"Stream URL bulunamadı: {cid}")
                continue
            channel_name = cid.replace("-", " ").title()
            lines.append(f'#EXTINF:-1 group-title="Berat ",{channel_name}')
            lines.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            lines.append(f'#EXTVLCOPT:http-referrer={referer_url}')
            lines.append(stream_url)
        return "\n".join(lines)

    def calistir(self):
        working_domain = self.find_working_domain()
        if not working_domain:
            raise RuntimeError("Çalışan domain bulunamadı!")
        m3u_content = self.build_m3u8(working_domain)
        with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        print(f"M3U dosyası oluşturuldu: {self.cikti_dosyasi}")

if __name__ == "__main__":
    XYZsportsManager("Osibusibiraz.m3u").calistir()
