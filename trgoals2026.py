import requests
import re
import sys
import random

# Terminal renkleri
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Güncel domain (senin verdiğin)
BASE_SITE = "https://www.trgoals53.top"

# Direkt çalışan m3u8'ler (HTML'den aldığımız resmi kanallar - bunlar stabil)
DIRECT_M3U8 = {
    "TRT 1": "https://d1u68oyra9spme.cloudfront.net/master.m3u8",
    "TRT 2": "https://tv-trt2.medya.trt.com.tr/master.m3u8",
    "TRT Spor": "https://tv-trtspor1.medya.trt.com.tr/master.m3u8",
    "TRT Yıldız": "https://tv-trtspor2.medya.trt.com.tr/master.m3u8",
    # İstersen daha fazla resmi açık kanal ekleyebilirsin
}

# viptv için olası embed pattern tahminleri (2025-2026 klonlarında sık görülenler)
VIPTV_PATTERNS = [
    "/embed/viptv/{id}",
    "/player.php?id={id}",
    "/embed.php?source={id}",
    "/viptv/{id}",
    "/player/viptv/{id}",
    "https://player.trgoals.top/embed/{id}",  # olası dış player
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
]

KANALLAR = [  # Senin orijinal listen (sadece örnek kısım, tam listeyi ekle)
    {"source_id": "100001", "kanal_adi": "Bein Sports 1 HD", "tvg_id": "BeinSports1.tr"},
    {"source_id": "100002", "kanal_adi": "Bein Sports 2 HD", "tvg_id": "BeinSports2.tr"},
    # ... kalan beIN, S Sport, Tivibu, Smart Spor vs. ekle
    # data-source değerlerini HTML'den alıyorsun
]

def get_headers(referer=BASE_SITE):
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": referer + "/",
        "Accept": "*/*",
    }

def try_viptv_embed(source_id):
    """viptv için olası embed linklerini dene"""
    for pattern in VIPTV_PATTERNS:
        url = pattern.format(id=source_id)
        if not url.startswith("http"):
            url = BASE_SITE.rstrip("/") + url
        
        try:
            r = requests.get(url, headers=get_headers(), timeout=10, allow_redirects=True)
            if r.status_code == 200:
                # iframe ara
                iframe_match = re.search(r'<iframe[^>]+src=["\'](.*?)["\']', r.text, re.IGNORECASE | re.DOTALL)
                if iframe_match:
                    embed_url = iframe_match.group(1)
                    if "http" in embed_url:
                        print(f"{GREEN}[+] viptv embed bulundu: {embed_url}{RESET}")
                        return embed_url
                # Direkt m3u8 varsa
                if ".m3u8" in r.text:
                    m3u8_match = re.search(r'(https?://[^\s"\')]+?\.m3u8[^\s"\')]*?)', r.text)
                    if m3u8_match:
                        print(f"{GREEN}[+] Direkt m3u8 bulundu: {m3u8_match.group(1)}{RESET}")
                        return m3u8_match.group(1)
        except Exception as e:
            print(f"{YELLOW}[-] {url} denendi ama hata: {str(e)}{RESET}")
    return None

def generate_playlist():
    lines = ["#EXTM3U"]
    
    # 1. Direkt m3u8'leri ekle (en garanti kısım)
    print(f"{GREEN}Direkt çalışan TRT kanalları ekleniyor...{RESET}")
    for name, url in DIRECT_M3U8.items():
        lines.append(f'#EXTINF:-1 tvg-name="{name}",{name} (Legal/Stable)')
        lines.append(f'#EXTVLCOPT:http-user-agent=Mozilla/5.0')
        lines.append(url)
    
    # 2. viptv kanallarını dene (başarı şansı düşük)
    print(f"\n{GREEN}viptv kanalları deneniyor (embed tahmin)...{RESET}")
    for kanal in KANALLAR:
        source_id = kanal["source_id"]
        name = kanal["kanal_adi"]
        embed = try_viptv_embed(source_id)
        
        if embed:
            lines.append(f'#EXTINF:-1 tvg-id="{kanal["tvg_id"]}" tvg-name="{name}",{name} (viptv)')
            lines.append(f'#EXTVLCOPT:http-referrer={BASE_SITE}/')
            lines.append(embed)  # embed url veya m3u8
        else:
            print(f"{YELLOW}[-] {name} için embed bulunamadı (ID: {source_id}){RESET}")
    
    return "\n".join(lines)

if __name__ == "__main__":
    print(f"{GREEN}[*] trgoals53.top için playlist oluşturuluyor...{RESET}")
    print(f"    Site: {BASE_SITE}\n")
    
    playlist = generate_playlist()
    
    if len(playlist.splitlines()) <= 3:
        print(f"{RED}[HATA] Hiç kanal eklenemedi. Muhtemel nedenler:{RESET}")
        print("  • Cloudflare koruması aktif")
        print("  • viptv sistemi değişmiş / token gerekiyor")
        print("  • Manuel Network sekmesinden m3u8 yakalamanız gerekiyor")
        sys.exit(1)
    
    filename = "trgoals53_viptv_2026.m3u"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(playlist)
    
    print(f"\n{GREEN}✓ Playlist oluşturuldu: {filename}{RESET}")
    print("   → TRT kanalları büyük ihtimal çalışır")
    print("   → beIN vb. için başarı şansı düşük → manuel deneme önerilir")
    print("   En garanti çözüm: VPN aç → siteye gir → F12 → Network → .m3u8 filtrele")
