import requests
import json
from pathlib import Path

# Çıktı dosyası
m3u_file = Path("M3U/osibusideneme.m3u")
m3u_file.parent.mkdir(exist_ok=True)

# Çalışan referer siteleri (denge66’dan başlıyor)
sites = [f"https://dengetv{i}.live/" for i in range(66, 170)]

baseurl = None
for site in sites:
    try:
        # domain.php veya baseurl endpoint'i
        r = requests.get(site + "domain.php", timeout=5)
        if r.status_code == 200:
            data = r.json()
            baseurl = data.get("baseurl")
            if baseurl:
                print(f"✅ Çalışan referer bulundu: {site}")
                break
    except Exception as e:
        print(f"❌ {site} kontrol ediliyor... Hata: {e}")

if not baseurl:
    print("❌ Hiçbir baseurl bulunamadı. Script durdu.")
    exit(1)

# Kanal id’leri
kanallar = [
    "yayinzirve", "yayin1", "yayininat", "yayinb2", "yayinb3", "yayinb4",
    "yayinb5", "yayinbm1", "yayinbm2", "yayinss", "yayinss2", "yayint1",
    "yayint2", "yayint3", "yayinsmarts", "yayinsms2", "yayintrtspor",
    "yayintrtspor2", "yayintrt1", "yayinas", "yayinatv", "yayintv8",
    "yayintv85", "yayinf1", "yayinnbatv", "yayineu1", "yayineu2",
    "yayinex1", "yayinex2", "yayinex3", "yayinex4", "yayinex5",
    "yayinex6", "yayinex7", "yayinex8"
]

# M3U yazma
with open(m3u_file, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for kanal in kanallar:
        url = f"{baseurl}{kanal}.m3u8"
        f.write(f"#EXTINF:-1 group-title=\"Dengetv54\", {kanal}\n")
        f.write("#EXTVLCOPT:http-user-agent=Mozilla/5.0\n")
        f.write(f"#EXTVLCOPT:http-referrer={baseurl}\n")
        f.write(url + "\n")

print(f"💾 M3U dosyası kaydedildi: {m3u_file}")
