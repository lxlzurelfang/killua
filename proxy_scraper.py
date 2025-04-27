import requests
import random

def get_proxies():
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=id,sg&ssl=all&anonymity=all"
    try:
        response = requests.get(url, timeout=10)
        proxy_list = response.text.strip().split('\n')
        return [proxy for proxy in proxy_list if proxy]
    except Exception as e:
        print(f"[ProxyScraper] Error fetching proxies: {e}")
        return []

def get_random_proxy(proxies):
    return random.choice(proxies) if proxies else None
