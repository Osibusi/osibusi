from httpx import Client
import os

class DengetvManager:
    def __init__(self, ana_m3u_dosyasi):
        self.ana_m3u_dosyasi = ana_m3u_dosyasi
        self.httpx = Client(timeout=10, verify=False)
        self.referer_url = None

        # Kanal ID'leri
        self.channel_ids = [
            "zirve", "1", "inat", "b2", "b3",
            "b4", "b5", "bm1", "bm2", "ss",
            "ss2", "t1", "t2", "t3", "smarts",
            "sms2", "trtspor", "trtspor2", "trt1",
            "as", "atv", "tv8", "tv85", "f1",
            "nbatv", "eu1", "eu2", "ex1", "ex2",
            "ex3", "ex4", "ex5", "ex6", "ex7",
            "ex8"
        ]

        os.makedirs(os.path.dirname(self.ana_m3u_dosyasi), exist_ok=True)

    def find_working_denge(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        for i in range(66, 161):
            test_domain = f"https://dengetv{i}.live/"
            print(f"🔍 {test_domain} kontrol ediliyor...")
            try:
                r = self.httpx.get(test_domain, headers=headers)
                if r.status_code == 200 and r.text.strip():
                    print(f"✅ Çalışan referer bulundu: {test_domain}")
                    return test_domain
            except:
                continue
        print("❌ Hiçbir dengetv domain bulunamadı!")
        return None

    def build_m3u8_content(self):
        base_url = "https://audi.zirvedesin19.sbs/"  # Zirvedesin sabit
        m3u_content = ["#EXTM3U"]
        for channel_id in self.channel_ids:
            m3u_content.append(f'#EXTINF:-1 group-title="Dengetv54",Yayin{channel_id.capitalize()}')
            m3u_content.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u_content.append(f'#EXTVLCOPT:http-referrer={self.referer_url}')
            m3u_content.append(f'{base_url}yayin{channel_id}.m3u8')
        return "\n".join(m3u_content)

    def save_m3u(self, content):
        with open(self.ana_m3u_dosyasi, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"💾 {self.ana_m3u_dosyasi} kaydedildi.")

    def run(self):
        self.referer_url = self.find_working_denge()
        if not self.referer_url:
            print("❌ Denge referer bulunamadığı için işlem iptal edildi.")
            return
        m3u_content = self.build_m3u8_content()
        self.save_m3u(m3u_content)
        print("✅ Kanallar başarıyla M3U’ye eklendi.")


if __name__ == "__main__":
    manager = DengetvManager("M3U/osibusidengedeneme.m3u")
    manager.run()
