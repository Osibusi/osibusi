import requests
import os

# M3U klasörü yoksa oluştur
os.makedirs("M3U", exist_ok=True)

# Kanal listesi
kanallar = {
    "yayinzirve": "Yayinzirve",
    "yayin1": "Yayin1",
    "yayininat": "Yayininat",
    "yayinb2": "Yayinb2",
    "yayinb3": "Yayinb3",
    "yayinb4": "Yayinb4",
    "yayinb5": "Yayinb5",
    "yayinbm1": "Yayinbm1",
    "yayinbm2": "Yayinbm2",
    "yayinss": "Yayinss",
    "yayinss2": "Yayinss2",
    "yayint1": "Yayint1",
    "yayint2": "Yayint2",
    "yayint3": "Yayint3",
    "yayinsmarts": "Yayinsmarts",
    "yayinsms2": "Yayinsms2",
    "yayintrtspor": "Yayintrtspor",
    "yayintrtspor2": "Yayintrtspor2",
    "yayintrt1": "Yayintrt1",
    "yayinas": "Yayinas",
    "yayinatv": "Yayinatv",
    "yayintv8": "Yayintv8",
    "yayintv85": "Yayintv85",
    "yayinf1": "Yayinf1",
    "yayinnbatv": "Yayinnbatv",
    "yayineu1": "Yayineu1",
    "yayineu2": "Yayineu2",
    "yayinex1": "Yayinex1",
    "yayinex2": "Yayinex2",
    "yayinex3": "Yayinex3",
    "yayinex4": "Yayinex4",
    "yayinex5": "Yayinex5",
    "yayinex6": "Yayinex6",
    "yayinex7": "Yayinex7",
    "yayinex8": "Yayinex8"
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
