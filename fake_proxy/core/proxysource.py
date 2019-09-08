import random
from abc import ABC, abstractmethod


class ProxySource(ABC):
    __METADATA_KEYS = ('name', 'url')
    metadata = {}
    proxies = []

    def __init__(self):
        self.check_metadata(self.metadata)
        self._scrape()

    @abstractmethod
    def _scrape(self):
        pass

    def get(self):
        return random.choice(self.proxies)

    @staticmethod
    def check_metadata(metadata):
        for key in ProxySource.__METADATA_KEYS:
            if not metadata.get(key):
                msg = '"{}" not defined in metadata'.format(key)
                raise AttributeError(msg)

