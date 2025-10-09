import requests
import os

# M3U klasörü yoksa oluştur
os.makedirs("M3U", exist_ok=True)

# Kanal listesi
kanallar = {
    "yayinzirve": "BEIN SPORTS 1",
    "yayin1": "Bein 1 TRGOALS",
    "yayininat": "BEIN 1 İnatTv",
    "yayinb2": "BEIN Sports 2",
    "yayinb3": "BEIN Sports 3",
    "yayinb4": "BEIN Sports 4",
    "yayinb5": "BEIN Sports 5",
    "yayinbm1": "BEIN Sports Max 1",
    "yayinbm2": "BEIN Sports Max 2",
    "yayinss": "SSPORT 1",
    "yayinss2": "SSPORT 2",
    "yayint1": "TİVİBU SPOR 1",
    "yayint2": "TİVİBU SPOR 2",
    "yayint3": "TİVİBU SPOR 3",
    "yayinsmarts": "SMART SPOR ",
    "yayinsms2": "SMART SPOR 2",
    "yayintrtspor": "TRT SPOR",
    "yayintrtspor2": "TRT SPOR YILDIZ",
    "yayintrt1": "TRT 1 HD",
    "yayinas": "A SPOR HD",
    "yayinatv": "ATV",
    "yayintv8": "TV8 HD",
    "yayintv85": "TV8.5 HD",
    "yayinf1": "SKY SPORTS",
    "yayinnbatv": "NBA TV",
    "yayineu1": "EUROSPORT 1 HD",
    "yayineu2": "EUROSPORT 2 HD",
    "yayinex7": "TABİİ SPOR",
    "yayinex1": "TABİİ SPOR 1",
    "yayinex2": "TABİİ SPOR 2",
    "yayinex3": "TABİİ SPOR 3",
    "yayinex4": "TABİİ SPOR 4",
    "yayinex5": "TABİİ SPOR 5",
    "yayinex6": "TABİİ SPOR 6", 
    "yayinex8": "TABİİ SPOR 8"
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
        f.write(f"#EXTINF:-1 group-title=\"Osibusi_Beleştepe\",{kanal_name}\n")
        f.write("#EXTVLCOPT:http-user-agent=Mozilla/5.0\n")
        f.write(f"#EXTVLCOPT:http-referrer={working_domain}\n")
        f.write(f"{base_url}{kanal_id}.m3u8\n")

print(f"✅ M3U dosyası oluşturuldu: {m3u_path}")
