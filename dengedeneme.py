import requests
from pathlib import Path

# Kontrol edilecek domain aralığı
start = 65
end = 160

baseurl = None

for i in range(start, end + 1):
    domain = f"https://dengetv{i}.live/"
    print(f"🔍 {domain} kontrol ediliyor...")
    try:
        # domain.php'nin JSON döndürdüğünü varsayalım
        r = requests.get(domain + "domain.php", timeout=5)
        r.raise_for_status()
        data = r.json()
        if "baseurl" in data and data["baseurl"]:
            baseurl = data["baseurl"]
            print(f"✅ Çalışan referer bulundu: {domain} → baseurl: {baseurl}")
            break
    except Exception as e:
        print(f"❌ Hata: {e}")

if not baseurl:
    print("❌ Hiçbir geçerli domain bulunamadı!")
    exit(1)

# Çıktı dosyası
m3u_file = Path("M3U/osibusideneme.m3u")
m3u_file.parent.mkdir(exist_ok=True)

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
        url = f"{baseurl}channe
