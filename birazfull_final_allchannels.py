from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os
import datetime
import random
from httpx import Client

OUTPUT_FILE = "M3U/Osibusibirazfull.m3u"
MAX_DOMAIN_CHECK = 200  # Denenecek domain sayısı
BASEURLS = [
    "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/",
    "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/"
]

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

def find_latest_domain(start_number=27):
    client = Client(timeout=10, verify=False)
    for i in range(MAX_DOMAIN_CHECK):
        number = start_number + i
        domain = f"https://birazcikspor{number}.xyz/"
        try:
            r = client.get(domain)
            if r.status_code == 200:
                print(f"✅ Geçerli domain bulundu: {domain}")
                return domain
        except:
            continue
    fallback = f"https://birazcikspor{start_number}.xyz/"
    print(f"⚠️ Domain bulunamadı, varsayılan kullanılıyor: {fallback}")
    return fallback

def extract_channel_ids(domain):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(domain, timeout=15000)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "lxml")
    channel_ids = []
    for iframe in soup.find_all("iframe", id="matchPlayer"):
        src = iframe.get("src")
        if src and "id=" in src:
            cid = src.split("id=")[1].split("&")[0]
            channel_ids.append(cid)
    return list(set(channel_ids))

def resolve_source(cid):
    if cid.startswith("androstreamlivechstream"):
        after = cid.replace("androstreamlivechstream", "")
        return f"https://bllovdes.d4ssgk.su/o1/stream{after}/playlist.m3u8"
    elif cid.startswith("androstreamlive"):
        baseurl = random.choice(BASEURLS)
        return f"{baseurl}{cid}.m3u8"
    else:
        return None

def build_m3u_file(channel_ids, domain):
    lines = ["#EXTM3U"]
    for cid in channel_ids:
        url = resolve_source(cid)
        if not url:
            continue
        lines.append(f'#EXTINF:-1 group-title="Birazcikspor", {cid}')
        lines.append("#EXTVLCOPT:http-user-agent=Mozilla/5.0")
        lines.append(url)

    lines.append(f'#EXTINF:-1 group-title="Birazcikspor", Güncel Domain')
    lines.append(domain)
    lines.append(f"# Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return "\n".join(lines)

def main():
    domain = find_latest_domain()
    channel_ids = extract_channel_ids(domain)
    print(f"✅ {len(channel_ids)} kanal bulundu.")

    if os.path.exists(OUTPUT_FILE):
        bak_name = OUTPUT_FILE + "." + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".bak"
        os.rename(OUTPUT_FILE, bak_name)
        print(f"💾 Mevcut M3U dosyası yedeklendi: {bak_name}")

    content = build_m3u_file(channel_ids, domain)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ M3U dosyası '{OUTPUT_FILE}' başarıyla oluşturuldu.")

if __name__ == "__main__":
    main()
