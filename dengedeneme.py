from httpx import Client
from bs4 import BeautifulSoup
import os

class DengetvManager:
    def __init__(self, ana_m3u_dosyasi):
        self.ana_m3u_dosyasi = ana_m3u_dosyasi
        self.httpx = Client(timeout=10, verify=False)
        self.referer_url = None

        # M3U klasörünü oluştur
        os.makedirs(os.path.dirname(self.ana_m3u_dosyasi), exist_ok=True)

    # Referer taraması
    def find_working_domain(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        for i in range(65, 165):
            test_domain = f"https://dengetv{i}.live/"
            print(f"🔍 {test_domain} kontrol ediliyor...")
            try:
                r = self.httpx.get(test_domain, headers=headers)
                if r.status_code == 200 and r.text.strip():
                    print(f"✅ Çalışan referer bulundu: {test_domain}")
                    return test_domain
            except Exception as e:
                print(f"❌ Hata: {e}")
                continue
        print("❌ Hiçbir referer bulunamadı!")
        return None

    # Sayfadaki tüm kanal ID’lerini al
    def get_channel_ids(self, domain):
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            r = self.httpx.get(domain, headers=headers)
            if r.status_code != 200:
                print(f"❌ Sayfa yüklenemedi: {domain}")
                return []

            soup = BeautifulSoup(r.text, "html.parser")
            channel_ids = []

            # Tüm iframe ve a taglerini tara
            for tag in soup.find_all(['iframe', 'a']):
                for attr in ['src', 'href']:
                    val = tag.get(attr)
                    if val and 'channel?id=' in val:
                        channel_id = val.split('channel?id=')[-1].split('&')[0]
                        if channel_id not in channel_ids:
                            channel_ids.append(channel_id)

            print(f"✅ {len(channel_ids)} kanal bulundu: {channel_ids}")
            return channel_ids
        except Exception as e:
            print(f"❌ Hata: {e}")
            return []

    # M3U içeriği oluştur
    def build_m3u_content(self, channel_ids):
        m3u_content = ["#EXTM3U"]
        for channel_id in channel_ids:
            channel_name = channel_id.capitalize()
            m3u_content.append(f'#EXTINF:-1 group-title="Dengetv54",{channel_name}')
            m3u_content.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u_content.append(f'#EXTVLCOPT:http-referrer={self.referer_url}')
            m3u_content.append(f"{self.referer_url}channel?id={channel_id}")
        return "\n".join(m3u_content)

    # M3U dosyasını kaydet
    def save_m3u(self, content):
        with open(self.ana_m3u_dosyasi, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"💾 {self.ana_m3u_dosyasi} kaydedildi.")

    # Scripti çalıştır
    def calistir(self):
        self.referer_url = self.find_working_domain()
        if not self.referer_url:
            print("❌ Referer bulunamadı, M3U oluşturulamıyor.")
            return

        channel_ids = self.get_channel_ids(self.referer_url)
        if not channel_ids:
            print("❌ Kanal ID’si bulunamadı, M3U oluşturulamıyor.")
            return

        m3u_content = self.build_m3u_content(channel_ids)
        self.save_m3u(m3u_content)
        print("✅ Kanallar başarıyla M3U’ye eklendi.")


if __name__ == "__main__":
    manager = DengetvManager("M3U/osibusidengedeneme.m3u")
    manager.calistir()
