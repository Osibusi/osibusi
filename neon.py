import asyncio
import aiohttp
import logging
import os
import re
from git import Repo

# ------------------- Ayarlar -------------------
START_DOMAIN = 523
DOMAIN_COUNT = 300
TIMEOUT = 3  # saniye
REPO_PATH = os.getenv('GITHUB_WORKSPACE', os.getcwd())
M3U8_PATH = os.path.join(REPO_PATH, 'M3U/Osispor.m3u8')
# ------------------------------------------------

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

active_baseurl = None  # Bulunan ilk aktif domainin baseurl'i
active_found_event = asyncio.Event()  # İlk aktif domain bulundu mu

async def fetch_baseurl(session, domain_number):
    global active_baseurl
    if active_found_event.is_set():
        return None

    url = f"https://monotv{domain_number}.com/channel?id=yayinzirve"
    logging.info(f"Domain {domain_number} kontrol ediliyor...")

    try:
        async with session.get(url, timeout=TIMEOUT) as resp:
            if resp.status == 200:
                text = await resp.text()
                scripts = re.findall(r"<script.*?>(.*?)</script>", text, re.DOTALL)
                for script in scripts:
                    split_pattern = r"'([^']+)'\.split\('\|'\)"
                    match = re.search(split_pattern, script)
                    if match:
                        parts = match.group(1).split('|')
                        if len(parts) > 3:
                            domain_php = f"https://{parts[3]}.com/domain.php"
                            try:
                                async with session.get(domain_php, timeout=TIMEOUT) as api_resp:
                                    if api_resp.status == 200:
                                        data = await api_resp.json()
                                        baseurl = data.get('baseurl', '').rstrip('/')
                                        if baseurl:
                                            logging.info(f"İlk aktif domain bulundu {domain_number}: {baseurl}")
                                            active_baseurl = baseurl
                                            active_found_event.set()  # Diğer task'lar iptal edilecek
                                            return baseurl
                            except Exception:
                                logging.warning(f"domain.php {parts[3]} yanıt vermedi.")
            return None
    except Exception:
        logging.warning(f"Domain {domain_number} yanıt vermedi, atlandı.")
        return None

async def main_async():
    global active_baseurl
    current_content = None
    try:
        with open(M3U8_PATH, 'r', encoding='utf-8') as f:
            current_content = f.read()
    except Exception as e:
        logging.error(f"M3U8 okunamadı: {e}")
        return

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_baseurl(session, i) for i in range(START_DOMAIN, START_DOMAIN + DOMAIN_COUNT)]
        await asyncio.gather(*tasks)

    if not active_baseurl:
        logging.info("Aktif domain bulunamadığı için güncelleme yapılmadı.")
        return

    # M3U8 güncelle
    pattern = r'https?://[^/]+/(?:.*yayin.*)'
    updated_content = re.sub(pattern, lambda m: m.group(0).replace(m.group(0).split('/')[2], active_baseurl.split('//')[1]), current_content)

    if updated_content != current_content:
        try:
            with open(M3U8_PATH, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            # Git commit & push
            repo = Repo(REPO_PATH)
            repo.index.add([M3U8_PATH])
            repo.index.commit("🛠️ Auto: Linkler Güncellendi")
            origin = repo.remote('origin')
            origin.push()
            logging.info("M3U8 güncellendi ve Git'e push edildi")
        except Exception as e:
            logging.error(f"Güncelleme veya Git işlemleri hatası: {e}")
    else:
        logging.info("Güncelleme gerekli değil")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
