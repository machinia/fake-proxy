from fake_proxy.core.proxysource import ProxySource


class NotImplementedMethod(ProxySource):
    metadata = {
            'name': 'non_implemented_method',
            'url': 'https://www.abs.com',
            'type': 'http'
    }

    def __init__(self):
        super().__init__()
