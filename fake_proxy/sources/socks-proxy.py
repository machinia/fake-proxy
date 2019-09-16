import requests
from bs4 import BeautifulSoup
from fake_proxy.core.proxysource import ProxySource


class SocksProxy(ProxySource):  # pragma: no cover
    metadata = {
        'name': 'socks-proxy.net',
        'url': 'https://www.socks-proxy.net/',
        'type': ['socks4']
    }

    def __init__(self):
        super().__init__()

    def _scrape(self):
        self.proxies = []

        res = requests.get(self.metadata['url'])
        soup = BeautifulSoup(res.text, 'html.parser')

        proxies_found = soup.select('table#proxylisttable tr')
        for p in proxies_found:
            row = p.find_all('td')
            if len(row):
                result = {}
                result['ip'] = row[0].text
                result['port'] = row[1].text
                result['country_code'] = row[2].text
                result['country'] = row[3].text
                result['type'] = row[4].text.lower()

                self.proxies.append(result)
