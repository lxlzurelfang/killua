import requests
import threading
import time
import json
import random

# Load keywords
with open('keywords.json', 'r') as f:
    keywords_data = json.load(f)
KEYWORDS = keywords_data['games']

def get_random_keywords(n=5):
    """Ambil n random keywords"""
    return random.sample(KEYWORDS, n)

def scrape_links(keyword):
    """Scrape function dummy (ganti dengan scrape site sesungguhnya)"""
    try:
        print(f"[Scraping] Keyword: {keyword}")
        # simulasi scraping
        time.sleep(1)  # fake delay scraping
        print(f"[Success] Fetched data for: {keyword}")
    except Exception as e:
        print(f"[Error] {keyword} - {str(e)}")

def scrape_cycle():
    keywords_to_use = get_random_keywords(10)
    threads = []

    print(f"[+] Selected keywords this cycle: {keywords_to_use}")

    # Auto log keywords
    with open('keyword_log.txt', 'a') as log_file:
        for keyword in keywords_to_use:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {keyword}\n")

    # Create thread per keyword
    for keyword in keywords_to_use:
        t = threading.Thread(target=scrape_links, args=(keyword,))
        t.start()
        threads.append(t)

    # Wait semua thread selesai
    for t in threads:
        t.join()

def main():
    while True:
        print("[*] Starting scrape cycle...")
        scrape_cycle()
        print("[*] Sleeping for 15 minutes...\n")
        time.sleep(900)  # 15 menit

if __name__ == "__main__":
    main()
