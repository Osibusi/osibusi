from httpx import Client
import re

class XYZsportsManager:
    def __init__(self, cikti_dosyasi):
        self.cikti_dosyasi = cikti_dosyasi
        self.httpx = Client(timeout=10, verify=False)
        self.domain_bilgileri = []
        self.channel_ids = [
            "bein-sports-1", "bein-sports-2", "bein-sports-3",
            "bein-sports-4", "bein-sports-5", "bein-sports-max-1",
            "bein-sports-max-2", "smart-spor", "smart-spor-2",
            "trt-spor", "trt-spor-2", "aspor", "s-sport",
            "s-sport-2", "s-sport-plus-1", "s-sport-plus-2", 
            "androstreamlivebiraz1"
        ]

    def find_working_domain(self, start=25, end=360):
        headers = {"User-Agent": "Mozilla/5.0"}
        for i in range(start, end + 1):
            url = f"https://birazcikspor{i}.xyz/event.html?id=androstreamlivebiraz1"
            try:
                print(f"🕵️‍♂️ Deneniyor: {url}")
                r = self.httpx.get(url, headers=headers)
                if r.status_code == 200 and "uxsyplayer" in r.text:
                    print(f"✅ Çalışan domain bulundu: {url}")
                    return r.text, url
            except:
                continue
        return None, None

    def find_dynamic_player_domain(self, html):
        m = re.search(r'https?://([a-z0-9\-]+\.[0-9a-z]+\.click)', html)
        return f"https://{m.group(1)}" if m else None

    def extract_base_stream_url(self, html):
        m = re.search(r'this\.baseStreamUrl\s*=\s*[\'"]([^\'"]+)', html)
        return m.group(1) if m else None

    def build_m3u8_content(self, base_stream_url, referer_url):
        m3u = ["#EXTM3U"]
        for cid in self.channel_ids:
            channel_name = cid.replace("-", " ").title()
            m3u.append(f'#EXTINF:-1 group-title="Berat", {channel_name}')
            m3u.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u.append(f'#EXTVLCOPT:http-referrer={referer_url}')
            m3u.append(f'{base_stream_url}{cid}/playlist.m3u8')
        return "\n".join(m3u)

    def calistir(self):
        html, referer_url = self.find_working_domain()
        if not html:
            raise RuntimeError("❌ Çalışan domain bulunamadı!")

        player_domain = self.find_dynamic_player_domain(html)
        if not player_domain:
            raise RuntimeError("❌ Player domain bulunamadı!")

        r = self.httpx.get(f"{player_domain}/index.php?id={self.channel_ids[0]}", headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": referer_url
        })

        base_url = self.extract_base_stream_url(r.text)
        if not base_url:
            raise RuntimeError("❌ Base stream URL bulunamadı!")

        m3u_icerik = self.build_m3u8_content(base_url, referer_url)

        with open(self.cikti_dosyasi, "w", encoding="utf-8") as f:
            f.write(m3u_icerik)
        print(f"✅ M3U dosyası oluşturuldu: {self.cikti_dosyasi}")

if __name__ == "__main__":
    XYZsportsManager("Osibusibiraz.m3u").calistir()
