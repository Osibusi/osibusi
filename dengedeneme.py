import requests
from pathlib import Path

start = 65  # Dengetv65'ten başla
end = 160   # İstersen üst sınır koy
kanallar = [
    "yayinzirve","yayin1","yayininat","yayinb2","yayinb3","yayinb4","yayinb5",
    "yayinbm1","yayinbm2","yayinss","yayinss2","yayint1","yayint2","yayint3",
    "yayinsmarts","yayinsms2","yayintrtspor","yayintrtspor2","yayintrt1","yayinas",
    "yayinatv","yayintv8","yayintv85","yayinf1","yayinnbatv","yayineu1","yayineu2",
    "yayinex1","yayinex2","yayinex3","yayinex4","yayinex5","yayinex6","yayinex7","yayinex8"
]

m3u_folder = Path("M3U")
m3u_folder.mkdir(exist_ok=True)
m3u_file = m3u_folder / "osibusidengedeneme.m3u"

baseurl = None

# Domainleri sırayla dene
for i in range(start, end+1):
    domain = f"https://dengetv{i}.live/"
    try:
        r = requests.get(f"{domain}domain.php", timeout=5)
        r.raise_for_status()
        data = r.json()
        baseurl = data.get("baseurl")
        if baseurl:
            print(f"✅ Geçerli domain bulundu: {domain}")
            break
    except Exception as e:
        print(f"❌ {domain} kontrol ediliyor... Hata: {e}")

if not baseurl:
    print("❌ Hiçbir geçerli domain bulunamadı.")
    exit(1)

# M3U oluştur
with open(m3u_file, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for kanal in kanallar:
        url = f"{baseurl}channel?id={kanal}"
        f.write(f"#EXTINF:-1 group-title=\"Dengetv{start}\",{kanal}\n")
        f.write("#EXTVLCOPT:http-user-agent=Mozilla/5.0\n")
        f.write(f"#EXTVLCOPT:http-referrer={baseurl}\n")
        f.write(url + "\n")

print(f"💾 {m3u_file} kaydedildi.")
