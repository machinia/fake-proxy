import random
from fake_proxy.core.proxysourcemanager import ProxySourceManager
from fake_proxy.core.exceptions import EmptyResultsException
from fake_proxy.core.exceptions import ProxyTypeError


m = ProxySourceManager()


def proxy_sources(proxy_type=[]):
    """
    Returns a list with the names of the sources from where the library can
    fetch proxies
    : param proxy_type: string or list of strings with the type of proxy
    : return: list with the names of the proxy sources the library can handle
    """
    proxy_type = format_proxy_type(proxy_type)
    sources = {}
    for t in proxy_type:
        if t in m.proxies_per_type:
            sources[t] = m.proxies_per_type[t]
    return sources


def get(amount=1, proxy_type=[]):
    """
    Returns a certain amount of proxies of the given type. If no type is given,
    returns of random types.
    : param amount: integer, amount of proxies to request
    : param proxy_type: string or list of strings with types of
    proxies to return
    :return: list with proxies
    """
    proxy_type = format_proxy_type(proxy_type)
    results = []
    for i in range(int(amount)):
        try:
            p_type = random.choice(proxy_type)

            available_sources = proxy_sources(p_type)
            if not len(available_sources[p_type]):
                msg = 'There are no sources with {} proxies'.format(p_type)
                print(msg)
                proxy_type.remove(p_type)
                continue
            source_name = random.choice(available_sources[p_type])

            r = get_from_source(source_name=source_name, proxy_type=p_type)
            results += r
        except IndexError:
            break
    return results


def get_from_source(source_name, amount=1, proxy_type=[]):
    """
    Returns a proxy from a particular source
    : param source_name: string with the name of a source
    : param amount: integer, amount of proxies to request
    : param proxy_type: string or list of strings with types of
    proxies to return
    : return: list with proxies from the given source
    """
    p = m.instance(source_name)
    proxy_type = format_proxy_type(proxy_type)
    results = []
    for i in range(int(amount)):
        try:
            p_type = random.choice(proxy_type)
            results.append(p.get(p_type))
        except EmptyResultsException as e:
            print(e)
            m.remove_source(source_name, p_type)
            proxy_type.remove(p_type)
        except IndexError:
            break
    return results


def reload():
    m.load()


def format_proxy_type(proxy_type):
    """
    Checks and formats the received proxy_type into a list, to be used
    by the library
    : param proxy_type: proxy type expected by the user
    : return: list of strings with the proxy types requested by
    the user; raises ProxyTypeError or TypeError on errors
    """
    if isinstance(proxy_type, str):
        types = m.proxies_per_type.keys()
        if proxy_type not in types:
            msg = 'The library doesn\'t manage the required type. '\
                    'Choose from {}'.format(list(types))
            raise ProxyTypeError(msg)
        proxy_type = [proxy_type]
    elif proxy_type and isinstance(proxy_type, list):
        all(format_proxy_type(elem) for elem in proxy_type)
    elif proxy_type and not isinstance(proxy_type, list):
        raise TypeError('Invalid proxy_type type, must be a string or a list')
    else:
        proxy_type = list(m.proxies_per_type.keys())
    return proxy_type
