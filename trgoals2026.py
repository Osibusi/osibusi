import requests
import re
import sys
import random
from time import sleep

# Terminal renkleri
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Güncel bilinen / olası domainler (Ocak 2026 başı popüler olanlardan seçki)
POSSIBLE_DOMAINS = [
    "trgoals1491.xyz",
    "trgoals1490.xyz",
    "trgoals1480.xyz",
    "trgoals1477.xyz",
    "trgoals1459.xyz",
    "trgoals.tr",               # bazen yönlendirme olur
    "trgoals4.top",
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
]

KANALLAR = [   # senin orijinal listen aynı kaldı
    {"dosya": "yayinzirve.m3u8", "tvg_id": "BeinSports1.tr", "kanal_adi": "Bein Sports 1 HD (VIP)"},
    {"dosya": "yayin1.m3u8", "tvg_id": "BeinSports1.tr", "kanal_adi": "Bein Sports 1 HD"},
    # ... kalanları da buraya ekle, kısalttım
]

def get_headers(referer=""):
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": referer,
        "Accept": "*/*",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    }

def find_working_site():
    print(f"\n{GREEN}[*] Güncel domain aranıyor...{RESET}")
    
    for domain in POSSIBLE_DOMAINS:
        for proto in ["https", "http"]:
            url = f"{proto}://{domain}/"
            try:
                r = requests.get(url, headers=get_headers(), timeout=8, allow_redirects=True)
                if r.status_code == 200 and "maç izle" in r.text.lower():
                    print(f"{GREEN}[+] Çalışıyor → {url}{RESET}")
                    return url.rstrip("/")
                else:
                    print(f"{YELLOW}[-] {url} → status {r.status_code}{RESET}")
            except Exception as e:
                print(f"{RED}[-] {url} → {str(e).splitlines()[0]}{RESET}")
            sleep(1.3)
    return None

def search_m3u8_base(site_url):
    print(f"\n{GREEN}[*] {site_url} içinde m3u8 aranıyor...{RESET}")
    
    possible_test_paths = [
        "",                             # ana sayfa
        "/bein-sports-1-izle/",
        "/bein-sports-2-izle/",
        "/mac/yayin/",
        "/canli/",
    ]
    
    found_bases = set()
    
    for path in possible_test_paths:
        test_url = site_url + path
        try:
            headers = get_headers(site_url + "/")
            r = requests.get(test_url, headers=headers, timeout=10)
            if r.status_code != 200:
                continue
                
            # 1. Direkt .m3u8 pattern'leri
            m3u8s = re.findall(r'(https?://[^"\')\s<>{}]+?\.m3u8(?:\?[^"\')\s<>{}]*)?)', r.text)
            for m in m3u8s:
                base = "/".join(m.split("/")[:-1]) + "/"
                if "trgoal" in base.lower() or "hls" in base.lower():
                    found_bases.add(base)
                    print(f"  {GREEN}✓ Potansiyel base bulundu:{RESET} {base}")
            
            # 2. JS dosyalarını da tara (çok yaygın yöntem)
            js_files = re.findall(r'src=["\']([^"\']+\.js)["\']', r.text)
            for js_rel in js_files[:4]:  # ilk 4 js'i dene
                if not js_rel.startswith(('http', '//')):
                    js_url = site_url.rstrip('/') + '/' + js_rel.lstrip('/')
                else:
                    js_url = js_rel
                
                try:
                    js_r = requests.get(js_url, headers=headers, timeout=6)
                    js_m3u8 = re.findall(r'(https?://[^"\')\s]+?\.m3u8[^"\')]*?)', js_r.text)
                    for jm in js_m3u8:
                        base = "/".join(jm.split("/")[:-1]) + "/"
                        if any(x in base for x in ["trgoal", "hls", "yayin"]):
                            found_bases.add(base)
                            print(f"  {GREEN}JS içinde bulundu:{RESET} {base}")
                except:
                    pass
                    
        except Exception as e:
            print(f"  {YELLOW}Hata {path}: {str(e).splitlines()[0]}{RESET}")
    
    return list(found_bases) if found_bases else None

def generate_m3u(base_url, referer):
    lines = ["#EXTM3U"]
    for idx, k in enumerate(KANALLAR, 1):
        name = f"TRG {k['kanal_adi']}"
        full_url = base_url.rstrip('/') + '/' + k['dosya'].lstrip('/')
        lines.append(f'#EXTINF:-1 tvg-id="{k["tvg_id"]}" tvg-name="{name}",{name}')
        lines.append(f'#EXTVLCOPT:http-user-agent=Mozilla/5.0')
        lines.append(f'#EXTVLCOPT:http-referrer={referer}')
        lines.append(full_url)
        print(f"  {idx:2d}. {name}")
    return "\n".join(lines)

# =====================================
if __name__ == "__main__":
    site = find_working_site()
    if not site:
        print(f"\n{RED}[×] Hiçbir domain çalışmadı. Telegram veya twitter'dan güncel adres bakmalısın.{RESET}")
        sys.exit(1)

    print(f"\n{GREEN}Kullanılan site:{RESET} {site}")
    
    bases = search_m3u8_base(site)
    if not bases:
        print(f"{RED}[×] Hiç m3u8 base'i tespit edilemedi :({RESET}")
        print("  Alternatif: telegram gruplarından günlük link al (en garanti yol)")
        sys.exit(2)
    
    # İlk bulunan base'i kullanalım (genelde en iyisi ilk olur)
    chosen_base = bases[0]
    print(f"\n{GREEN}[OK] Kullanılacak base:{RESET} {chosen_base}")
    
    playlist = generate_m3u(chosen_base, site)
    
    filename = "trgoals_guncel_2026.m3u"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(playlist)
    
    print(f"\n{GREEN}✓ Playlist hazır: {filename}{RESET}")
    print("   VLC veya benzeri oynatıcıda dene")
    print(f"   Not: Linkler 1-3 gün içinde bozulabilir, düzenli güncelle")
