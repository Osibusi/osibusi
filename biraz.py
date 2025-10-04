from httpx import Client
import re

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
            "androstreamlivebiraz1"
        ]
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def find_working_domain(self):
        url = "https://birazcikspor27.xyz/"
        print(f"Deniyor: {url}")
        try:
            r = self.httpx.get(url, headers=self.headers)
            if r.status_code == 200 and "clappr.min.js" in r.text:
                print(f"Çalışan domain bulundu: {url}")
                return url
            else:
                print(f"Domain erişildi ama beklenen içerik bulunamadı.")
        except Exception as e:
            print(f"Bağlantı hatası: {e}")
        return None

    def build_m3u8_content(self, referer_url):
        # Burada sayfadaki javascript yapısına göre m3u8 linki oluşturuluyor
        baseurls = [
            "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/",
            "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/"
        ]

        m3u = ["#EXTM3U"]
        for cid in self.channel_ids:
            if cid.startswith("androstreamlivech"):
                after_ch = cid.replace("androstreamlivech", "")
                if not after_ch:
                    continue
                stream_url = f"https://bllovdes.d4ssgk.su/o1/{after_ch}/playlist.m3u8"
            elif cid.startswith("androstreamlive"):
                import random
                baseurl = random.choice(baseurls)
                stream_url = f"{baseurl}{cid}.m3u8"
            else:
                # Normal kanallar için örnek bir yapı, eğer farklıysa güncellemeniz gerekir
                stream_url = f"{referer_url}play/{cid}.m3u8"
            
            channel_name = cid.replace("-", " ").title()
            m3u.append(f'#EXTINF:-1 group-title="Berat", {channel_name}')
            m3u.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u.append(f'#EXTVLCOPT:http-referrer={referer_url}')
            m3u.append(stream_url)
        
        return "\n".join(m3u)

    def calistir(self):
        referer_url = self.find_working_domain()
        if not referer_url:
            raise RuntimeError("Çalışan domain bulunamadı!")

        m3u_content = self.build_m3u8_content(referer_url)

        with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
            f.write(m3u_content)

        print(f"M3U dosyası başarıyla oluşturuldu: {self.cikti_dosyasi}")

if __name__ == "__main__":
    XYZsportsManager("Osibusibiraz.m3u").calistir()
