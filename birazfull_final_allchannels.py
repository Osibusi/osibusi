from playwright.sync_api import sync_playwright
import os
import re
from datetime import datetime
import random

OUTPUT_FILE = "M3U/Osibusibirazfull.m3u"
BASE_URLS = [
    "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/",
    "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/"
]

# Klasör ve yedekleme
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
if os.path.exists(OUTPUT_FILE):
    bak_name = f"{OUTPUT_FILE}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    os.rename(OUTPUT_FILE, bak_name)
    print(f"💾 Mevcut M3U dosyası yedeklendi: {bak_name}")

def resolve_source_from_id(cid):
    if cid.startswith("androstreamlivechstream"):
        after = cid.replace("androstreamlivechstream", "")
        return f"https://bllovdes.d4ssgk.su/o1/{after}/playlist.m3u8"
    elif cid.startswith("androstreamlive"):
        baseurl = random.choice(BASE_URLS)
        return f"{baseurl}{cid}.m3u8"
    return None

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Dinamik domain tespiti
    start_number = 27
    max_attempts = 100
    for i in range(max_attempts):
        domain_number = start_number + i
        domain = f"https://birazcikspor{domain_number}.xyz/"
        try:
            page.goto(domain, timeout=15000)
            page.wait_for_timeout(5000)  # JS render için bekle
            if page.title():
                print(f"✅ Geçerli domain bulundu: {domain}")
                break
        except:
            continue
    else:
        domain = f"https://birazcikspor{start_number}.xyz/"
        print(f"⚠️ Güncel domain bulunamadı, varsayılan kullanılıyor: {domain}")
        page.goto(domain)
        page.wait_for_timeout(5000)
    
    # iframe ve script tarama
    ids = set()

    frames = page.query_selector_all("iframe")
    for f in frames:
        src = f.get_attribute("src") or ""
        match = re.search(r"id=(androstreamlive[\w\d]+)", src)
        if match:
            ids.add(match.group(1))

    scripts = page.query_selector_all("script")
    for s in scripts:
        text = s.text_content() or ""
        matches = re.findall(r"id=(androstreamlive[\w\d]+)", text)
        for m in matches:
            ids.add(m)

    browser.close()

print(f"✅ {len(ids)} kanal bulundu.")

# M3U içeriği oluştur
m3u_lines = ["#EXTM3U"]
for cid in sorted(ids):
    stream_url = resolve_source_from_id(cid)
    if not stream_url:
        continue
    channel_name = cid.replace("-", " ").title()
    m3u_lines.append(f'#EXTINF:-1 group-title="Birazcikspor", {channel_name}')
    m3u_lines.append("#EXTVLCOPT:http-user-agent=Mozilla/5.0")
    m3u_lines.append(stream_url)

# Tarih damgası ekle
m3u_lines.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(m3u_lines))

print(f"✅ M3U dosyası '{OUTPUT_FILE}' başarıyla oluşturuldu.")
