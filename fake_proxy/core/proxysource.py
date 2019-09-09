from abc import ABC, abstractmethod
from fake_proxy.core.exceptions import EmptyResultsException
from fake_proxy.core.exceptions import ProxyTypeError


class ProxySource(ABC):
    __METADATA_KEYS = ('name', 'url', 'type')
    __REQUIRED_RESULT_KEYS = ('url', 'port', 'type')
    metadata = {}
    proxies_by_type = {}

    def __init__(self):
        self.proxies = []
        self.check_metadata(self.metadata)
        self._scrape()
        for t in self.metadata['type']:
            self.proxies_by_type[t] = []
        for p in self.proxies:
            self.proxies_by_type[p['type']].append(p)

    @abstractmethod
    def _scrape(self):
        """This method should implement the scrape from the url, and
        fill the proxies list"""

    def get(self, proxy_type):
        if proxy_type not in self.metadata['type']:
            raise ProxyTypeError('The source doesn\'t manage this type')

        try:
            p = self.proxies_by_type[proxy_type].pop()
            return p
        except IndexError:
            msg = 'The source doesn\'t have more {} proxies'.format(proxy_type)
            raise EmptyResultsException(msg)

    @staticmethod
    def check_metadata(metadata):
        for key in ProxySource.__METADATA_KEYS:
            if not metadata.get(key):
                msg = '"{}" not defined in metadata'.format(key)
                raise AttributeError(msg)
