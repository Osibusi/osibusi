from playwright.sync_api import sync_playwright
import os
from datetime import datetime

M3U_DOSYA = "M3U/Osibusibirazfull.m3u"
os.makedirs(os.path.dirname(M3U_DOSYA), exist_ok=True)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Domain sayısı dinamik, en günceli bulmak için 27-150 arası deneyebiliriz
        latest_domain = None
        for i in range(27, 151):
            domain = f"https://birazcikspor{i}.xyz/"
            try:
                page.goto(domain, timeout=10000)
                if page.status == 200:
                    latest_domain = domain
                    print(f"✅ Geçerli domain bulundu: {domain}")
                    break
            except:
                continue
        
        if not latest_domain:
            print("⚠️ Geçerli domain bulunamadı.")
            return
        
        page.goto(latest_domain)
        page.wait_for_timeout(3000)  # JS’nin çalışması için bekle

        # ID'leri çek
        frame_ids = page.eval_on_selector_all(
            "iframe",
            "elements => elements.map(e => new URL(e.src).searchParams.get('id')).filter(id => id)"
        )

        # M3U içerik oluştur
        m3u_lines = ["#EXTM3U"]
        baseurls = [
            "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/",
            "https://wandering-pond-ff44.andorrmaid278.workers.dev/checklist/"
        ]
        import random

        for cid in frame_ids:
            if cid.startswith("androstreamlivechstream"):
                after = cid.replace("androstreamlivechstream", "")
                stream_url = f"https://bllovdes.d4ssgk.su/o1/{after}/playlist.m3u8"
            else:
                baseurl = random.choice(baseurls)
                stream_url = f"{baseurl}{cid}.m3u8"
            m3u_lines.append(f'#EXTINF:-1 group-title="Birazcikspor", {cid}')
            m3u_lines.append(stream_url)

        m3u_lines.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        with open(M3U_DOSYA, "w", encoding="utf-8") as f:
            f.write("\n".join(m3u_lines))
        
        print(f"✅ M3U dosyası '{M3U_DOSYA}' başarıyla oluşturuldu.")
        browser.close()

if __name__ == "__main__":
    main()
