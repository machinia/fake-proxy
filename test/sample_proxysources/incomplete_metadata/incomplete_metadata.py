from fake_proxy.core.proxysource import ProxySource


class IncompleteMetadata(ProxySource):
    metadata = {
        'name': 'incomplete_metadata',
        'type': 'http'
    }

    def __init__(self):
        super().__init__()

    def _scrape(self):
        pass
