from httpx import Client

class XYZsportsManager:
    def __init__(self, cikti_dosyasi):
        self.cikti_dosyasi = cikti_dosyasi
        self.httpx = Client(timeout=10, verify=False)
        self.headers = {"User-Agent": "Mozilla/5.0"}

    def find_working_domain(self):
        url = "https://birazcikspor27.xyz/"
        print(f"Deniyor: {url}")
        try:
            r = self.httpx.get(url, headers=self.headers)
            if r.status_code == 200:
                print("Sayfa başarıyla açıldı.")
                snippet = r.text[:500]
                print(f"Sayfa içeriği başlangıcı (500 karakter):\n{snippet}\n---")
                if "clappr.min.js" in r.text or "androstreamlive" in r.text:
                    print(f"Beklenen içerik bulundu.")
                    return url
                else:
                    print(f"Domain erişildi ama beklenen içerik bulunamadı.")
            else:
                print(f"HTTP Durumu: {r.status_code}")
        except Exception as e:
            print(f"Bağlantı hatası: {e}")
        return None

    def calistir(self):
        domain = self.find_working_domain()
        if not domain:
            raise RuntimeError("Çalışan domain bulunamadı!")
        print(f"Çalışan domain: {domain}")

if __name__ == "__main__":
    XYZsportsManager("Osibusibiraz.m3u").calistir()
