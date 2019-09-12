from fake_proxy.core.proxysource import ProxySource


class NoMetadata(ProxySource):

    def __init__(self):
        super().__init__()

    def _scrape(self):
        pass
