import requests
import os

# M3U klasörü yoksa oluştur
os.makedirs("M3U", exist_ok=True)

# Kanal listesi
kanallar = {
    "yayinzirve": "Bein sports 1",
    "yayin1": "TRGOALS",
    "yayininat": "İnatTv",
    "yayinb2": "Bein Sports 2",
    "yayinb3": "Bein Sports 3",
    "yayinb4": "Bein Sports 4",
    "yayinb5": "Bein Sports 5",
    "yayinbm1": "Bein Sports Max 1",
    "yayinbm2": "Bein Sports Max 2",
    "yayinss": "SSPORT 1",
    "yayinss2": "SSPORT 2",
    "yayint1": "TİVİBU 1",
    "yayint2": "TİVİBU 2",
    "yayint3": "TİVİBU 3",
    "yayinsmarts": "SMART SPOR ",
    "yayinsms2": "SMART SPOR 2",
    "yayintrtspor": "TRT SPOR",
    "yayintrtspor2": "TRT SPOR 2",
    "yayintrt1": "TRT 1 ",
    "yayinas": "A SPOR",
    "yayinatv": "ATV",
    "yayintv8": "TV8",
    "yayintv85": "TV 8.5",
    "yayinf1": "SKY SPORTS",
    "yayinnbatv": "NBA TV",
    "yayineu1": "EUROSPORT 1",
    "yayineu2": "EUROSPORT 2",
    "yayinex1": "TABİ SPOR 1",
    "yayinex2": "TABİ SPOR 2",
    "yayinex3": "TABİ SPOR 3",
    "yayinex4": "TABİ SPOR 4",
    "yayinex5": "TABİ SPOR 5",
    "yayinex6": "TABİ SPOR 6",
    "yayinex7": "TABİ SPOR",
    "yayinex8": "TABİ SPOR 8"
}

# Gerçek M3U8 linklerinin base URL'si
base_url = "https://audi.zirvedesin19.sbs/"

# Çalışan domain bulma
working_domain = None
for i in range(66, 151):
    domain = f"https://dengetv{i}.live/"
    try:
        response = requests.get(domain, timeout=5)
        if response.status_code == 200:
            working_domain = domain
            print(f"✅ Çalışan domain bulundu: {domain}")
            break
        else:
            print(f"❌ {domain} çalışmıyor, status code: {response.status_code}")
    except Exception as e:
        print(f"❌ {domain} kontrol ediliyor... Hata: {e}")

if not working_domain:
    print("⚠️ Hiçbir domain çalışmıyor!")
    working_domain = "https://dengetv66.live/"  # fallback

# M3U dosyasını oluştur
m3u_path = "M3U/osibusidengedeneme.m3u"
with open(m3u_path, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for kanal_id, kanal_name in kanallar.items():
        f.write(f"#EXTINF:-1 group-title=\"Dengetv54\",{kanal_name}\n")
        f.write("#EXTVLCOPT:http-user-agent=Mozilla/5.0\n")
        f.write(f"#EXTVLCOPT:http-referrer={working_domain}\n")
        f.write(f"{base_url}{kanal_id}.m3u8\n")

print(f"✅ M3U dosyası oluşturuldu: {m3u_path}")
