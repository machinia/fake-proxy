class FakeProxyException(Exception):
    pass


class EmptyResultsException(FakeProxyException):
    pass


class InvalidProxySource(FakeProxyException):
    pass


class ProxyTypeError(FakeProxyException):
    pass
