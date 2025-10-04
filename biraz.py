from httpx import Client
import re
import random

class XYZsportsManager:
    def __init__(self, cikti_dosyasi):
        self.cikti_dosyasi = cikti_dosyasi
        self.httpx = Client(timeout=10, verify=False)
        self.channel_ids = [
            "bein-sports-1", "bein-sports-2", "bein-sports-3",
            "bein-sports-4", "bein-sports-5", "bein-sports-max-1",
            "bein-sports-max-2", "smart-spor", "smart-spor-2",
            "trt-spor", "trt-spor-2", "aspor", "s-sport",
            "s-sport-2", "s-sport-plus-1", "s-sport-plus-2", 
            "androstreamlivebs1",
            "androstreamlivechstream233"
        ]
        self.baseurls = [
            "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/",
            "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/"
        ]

    def find_working_domain(self, start=1, end=500):
        headers = {"User-Agent": "Mozilla/5.0"}
        for i in range(start, end + 1):
            url = f"https://birazcikspor{i}.xyz/"
            try:
                print(f"Deniyor: {url}")
                r = self.httpx.get(url, headers=headers)
                if r.status_code == 200 and "clappr.min.js" in r.text:
                    print(f"Çalışan domain bulundu: {url}")
                    return r.text, url
            except Exception as e:
                print(f"Hata: {e}")
                continue
        return None, None

    def resolve_source_from_id(self, id_):
        if not id_ or not isinstance(id_, str):
            return None
        if id_.startswith("androstreamlivech"):
            after_ch = id_.replace("androstreamlivech", "")
            return f"https://bllovdes.d4ssgk.su/o1/{after_ch}/playlist.m3u8"
        if id_.startswith("androstreamlive"):
            baseurl = random.choice(self.baseurls)
            return f"{baseurl}{id_}.m3u8"
        return None

    def build_m3u8_content(self, referer_url):
        m3u = ["#EXTM3U"]
        for cid in self.channel_ids:
            stream_url = self.resolve_source_from_id(cid)
            if not stream_url:
                print(f"Stream URL bulunamadı: {cid}")
                continue
            channel_name = cid.replace("-", " ").title()
            m3u.append(f'#EXTINF:-1 group-title="Berat ",{channel_name}')
            m3u.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u.append(f'#EXTVLCOPT:http-referrer={referer_url}')
            m3u.append(stream_url)
        return "\n".join(m3u)

    def calistir(self):
        html, referer_url = self.find_working_domain()
        if not html:
            raise RuntimeError("Çalışan domain bulunamadı!")
        m3u_icerik = self.build_m3u8_content(referer_url)
        with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
            f.write(m3u_icerik)
        print(f"Çıktı dosyası oluşturuldu: {self.cikti_dosyasi}")

if __name__ == "__main__":
    XYZsportsManager("Osibusibiraz.m3u").calistir()
