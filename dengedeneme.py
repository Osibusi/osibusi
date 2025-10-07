import requests
import os

# M3U klasörü hazırla
os.makedirs("M3U", exist_ok=True)

# Domainleri sırayla dene
for i in range(65, 161):
    domain = f"https://dengetv{i}.live/"
    try:
        r = requests.get(f"{domain}domain.php", timeout=5)
        r.raise_for_status()
        # Yanıt JSON mu kontrol et
        if r.headers.get("Content-Type", "").startswith("application/json"):
            data = r.json()
            baseurl = data.get("baseurl")
            if baseurl:
                print(f"✅ Geçerli domain bulundu: {domain}")
                break
            else:
                print(f"❌ {domain} JSON geldi ama baseurl yok, atlanıyor.")
        else:
            print(f"❌ {domain} JSON dönmedi, atlanıyor.")
    except Exception as e:
        print(f"❌ {domain} kontrol ediliyor... Hata: {e}")
else:
    print("⚠️ Hiçbir geçerli domain bulunamadı.")
    exit(1)

# Kanal listesi (sabit)
kanallar = [
    "yayinzirve","yayin1","yayininat","yayinb2","yayinb3","yayinb4","yayinb5",
    "yayinbm1","yayinbm2","yayinss","yayinss2","yayint1","yayint2","yayint3",
    "yayinsmarts","yayinsms2","yayintrtspor","yayintrtspor2","yayintrt1",
    "yayinas","yayinatv","yayintv8","yayintv85","yayinf1","yayinnbatv",
    "yayineu1","yayineu2","yayinex1","yayinex2","yayinex3","yayinex4",
    "yayinex5","yayinex6","yayinex7","yayinex8"
]

m3u_content = "#EXTM3U\n"
for kanal in kanallar:
    m3u_content += f"#EXTINF:-1 group-title=\"Dengetv{i}\",{kanal}\n"
    m3u_content += "#EXTVLCOPT:http-user-agent=Mozilla/5.0\n"
    m3u_content += f"#EXTVLCOPT:http-referrer={domain}\n"
    m3u_content += f"{domain}channel?id={kanal}\n"

# Dosyayı kaydet
m3u_path = "M3U/osibusidengedeneme.m3u"
with open(m3u_path, "w", encoding="utf-8") as f:
    f.write(m3u_content)

print(f"✅ M3U kaydedildi: {m3u_path}")
