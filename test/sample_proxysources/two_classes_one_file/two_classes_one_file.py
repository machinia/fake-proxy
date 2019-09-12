from fake_proxy.core.proxysource import ProxySource


class Class1(ProxySource):
    metadata = {
            'name': 'valid_metadata__1',
            'url': 'https://www.valid-url-1.com',
            'type': 'http'
    }

    def __init__(self):
        super().__init__()

    def _scrape(self):
        pass


class Class2(ProxySource):
    metadata = {
            'name': 'valid_metadata__2',
            'url': 'https://www.valid-url-2.com',
            'type': 'http'
    }

    def __init__(self):
        super().__init__()

    def _scrape(self):
        pass
