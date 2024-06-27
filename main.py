import requests
import json
import time
from config import TOKEN, COUNTRY, COUNT, PROXY_FORMAT

headers = {
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'Authorization': f'Bearer {TOKEN}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://ru.dashboard.proxy.market/',
    'X-Lang': 'ru',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'country': f'{COUNTRY}',
    'rotation': -1,
    'region_id': None,
    'city_id': None,
    'package_id': 7162,
}


def main():
    proxies = []

    for _ in range(COUNT):
        response = requests.post('https://api.dashboard.proxy.market/user/proxies/generate', headers=headers, json=json_data)
        if response.status_code == 200:
            proxy_data = response.json()
            ip = proxy_data.get("proxy", {}).get('ip')
            port = proxy_data.get("proxy", {}).get('http_port').split('-')[0]
            login = proxy_data.get("proxy", {}).get('login')
            password = proxy_data.get("proxy", {}).get('password')
            proxy_str = PROXY_FORMAT.format(ip=ip, port=port, login=login, password=password)
            proxies.append(proxy_str)
            print(f'Proxy: {proxy_str} | added')
        else:
            print(f"Request failed with status code {response.status_code}")
        time.sleep(1)

    with open('proxies.txt', 'w', encoding='utf-8') as f:
        for proxy in proxies:
            f.write(f"{proxy}\n")


if __name__ == '__main__':
    main()

