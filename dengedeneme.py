import os

class ZirvedesinM3U:
    def __init__(self, ana_m3u_dosyasi):
        self.ana_m3u_dosyasi = ana_m3u_dosyasi
        self.baseurl = "https://audi.zirvedesin19.sbs/"
        self.channels = [
            "yayinzirve","yayinb2","yayinb3","yayinb4","yayinb5",
            "yayinbm1","yayinbm2","yayinss","yayinss2","yayint1",
            "yayint2","yayint3","yayint4","yayinsmarts","yayineu1",
            "yayineu2","yayinex1","yayinex2","yayinex3","yayinex4",
            "yayinex5","yayinex6","yayinex7","yayinex8","yayintrtspor",
            "yayintrtspor2","yayintrt1","yayinf1","yayinas","yayinsms2",
            "yayinatv","yayintv8","yayintv85","yayinnbatv"
        ]
        os.makedirs(os.path.dirname(self.ana_m3u_dosyasi), exist_ok=True)

    def build_m3u(self):
        m3u = ["#EXTM3U"]
        for ch in self.channels:
            m3u.append(f'#EXTINF:-1 group-title="Zirvedesin",{ch.capitalize()}')
            m3u.append('#EXTVLCOPT:http-user-agent=Mozilla/5.0')
            m3u.append(f'#EXTVLCOPT:http-referrer={self.baseurl}')
            m3u.append(f'{self.baseurl}{ch}.m3u8')
        return "\n".join(m3u)

    def save_m3u(self):
        content = self.build_m3u()
        with open(self.ana_m3u_dosyasi, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ {self.ana_m3u_dosyasi} kaydedildi.")

if __name__ == "__main__":
    manager = ZirvedesinM3U("M3U/osibusidengedeneme.m3u")
    manager.save_m3u()
