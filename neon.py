import requests
import logging
import os
import re
from git import Repo

# ------------------- Ayarlar -------------------
START_DOMAIN = 523
DOMAIN_COUNT = 300
REPO_PATH = os.getenv('GITHUB_WORKSPACE', os.getcwd())
M3U8_PATH = os.path.join(REPO_PATH, 'M3U/Osispor.m3u8')
# ------------------------------------------------

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://monotv523.com/'
})

def extract_baseurl_from_script(script_content):
    try:
        split_pattern = r"'([^']+)'\.split\('\|'\)"
        match = re.search(split_pattern, script_content)
        if match:
            parts = match.group(1).split('|')
            if len(parts) > 3:
                domain_php = f"https://{parts[3]}.com/domain.php"
                try:
                    resp = session.get(domain_php, timeout=3)
                    if resp.status_code == 200:
                        data = resp.json()
                        return data.get('baseurl', '').rstrip('/')
                except requests.RequestException:
                    logging.warning(f"domain.php {parts[3]} yanıt vermedi.")
        return None
    except Exception as e:
        logging.warning(f"Baseurl alınamadı: {e}")
        return None

def find_first_active_domain():
    for domain_number in range(START_DOMAIN, START_DOMAIN + DOMAIN_COUNT):
        url = f"https://monotv{domain_number}.com/channel?id=yayinzirve"
        logging.info(f"Domain {domain_number} kontrol ediliyor...")
        try:
            response = session.get(url, timeout=3)
            if response.status_code == 200:
                scripts = re.findall(r"<script.*?>(.*?)</script>", response.text, re.DOTALL)
                for script in scripts:
                    baseurl = extract_baseurl_from_script(script)
                    if baseurl:
                        logging.info(f"İlk aktif domain bulundu {domain_number}: {baseurl}")
                        return baseurl
        except requests.RequestException:
            logging.warning(f"Domain {domain_number} yanıt vermedi, atlandı.")
    logging.info("Hiçbir aktif domain bulunamadı.")
    return None

def read_m3u8():
    try:
        with open(M3U8_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logging.error(f"M3U8 okunamadı: {e}")
        return None

def update_m3u8(content, new_baseurl):
    pattern = r'https?://[^/]+/(?:.*yayin.*)'
    updated = re.sub(pattern, lambda m: m.group(0).replace(m.group(0).split('/')[2], new_baseurl.split('//')[1]), content)
    return updated

def commit_changes():
    try:
        repo = Repo(REPO_PATH)
        repo.index.add([M3U8_PATH])
        repo.index.commit("🛠️ Auto: Linkler Güncellendi")
        origin = repo.remote('origin')
        origin.push()
        logging.info("Değişiklikler Git'e push edildi")
    except Exception as e:
        logging.error(f"Git işlemleri hatası: {e}")

def main():
    current_content = read_m3u8()
    if not current_content:
        return

    new_baseurl = find_first_active_domain()
    if not new_baseurl:
        logging.info("Aktif domain bulunamadığı için güncelleme yapılmadı.")
        return

    updated_content = update_m3u8(current_content, new_baseurl)

    if updated_content != current_content:
        try:
            with open(M3U8_PATH, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            commit_changes()
            logging.info("M3U8 güncellendi")
        except Exception as e:
            logging.error(f"M3U8 yazma hatası: {e}")
    else:
        logging.info("Güncelleme gerekli değil")

if __name__ == "__main__":
    main()
