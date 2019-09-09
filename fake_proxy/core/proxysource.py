import random
from abc import ABC, abstractmethod


class ProxySource(ABC):
    __METADATA_KEYS = ('name', 'url', 'type')
    metadata = {}
    proxies = []

    def __init__(self):
        self.check_metadata(self.metadata)
        self._scrape()

    @abstractmethod
    def _scrape(self):
        pass

    def get(self, proxy_type=None):
        if not isinstance(proxy_type, list):
            proxy_type = [proxy_type]

        p = random.choice(self.proxies)
        if not proxy_type or p.get('type') in proxy_type:
            self.proxies.remove(p)
            return p

        return self.get(proxy_type)

    @staticmethod
    def check_metadata(metadata):
        for key in ProxySource.__METADATA_KEYS:
            if not metadata.get(key):
                msg = '"{}" not defined in metadata'.format(key)
                raise AttributeError(msg)
