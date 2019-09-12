import copy
from fake_proxy.core.proxysource import ProxySource
from test.sample_proxysources.sample_proxy_list import SAMPLE_PROXY_LIST


class ValidMetadataSource(ProxySource):
    metadata = {
            'name': 'valid_metadata',
            'url': 'https://www.valid-url.com',
            'type': ['http', 'https', 'socks4']
    }

    def __init__(self):
        super().__init__()

    def _scrape(self):
        self.proxies = []
        self.proxies = copy.deepcopy(SAMPLE_PROXY_LIST)
