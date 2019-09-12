fake-proxy
==========

Open source library that finds public proxies from several sources.


Usage
-----

The package must be imported and used through it's API.


`get(amount, proxy_type)`
~~~~~~~~~~~~~~~~~~~~~~~~~

The main function is `get`, which receives 2 parameters:
- `amount` which specifies the amount of proxies required
- `proxy_type` which specifies the type of proxy (https, http, socks4)

.. code-block:: python

    >>> import fake_proxy
    >>> fake_proxy.get()
    [{'ip': '188.166.83.20', 'port': '3128', 'country_code': 'NL', 'country': 'Netherlands', 'type': 'http'}]
    >>> fake_proxy.get(amount=3)
    [{'ip': '89.20.135.204', 'port': '10000', 'country_code': 'RU', 'country': 'Russian Federation', 'type': 'http'},
    {'ip': '165.22.154.157', 'port': '3128', 'country_code': 'US', 'country': 'United States', 'type': 'http'},
    {'ip': '76.87.101.188', 'port': '38875', 'country_code': 'US', 'country': 'United States', 'type': 'http'},
    {'ip': '36.67.93.211', 'port': '4145', 'country_code': 'ID', 'country': 'Indonesia', 'type': 'socks4'},
    {'ip': '62.182.206.19', 'port': '37715', 'country_code': 'RU', 'country': 'Russian Federation', 'type': 'http'}]
    >>> fake_proxy.get(proxy_type='https')
    [{'ip': '36.92.108.150', 'port': '3128', 'country_code': 'ID', 'country': 'Indonesia', 'type': 'https'}]


`get_by_source(source_name, amount, proxy_type)`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Similar to `get()`, but lets you specify a particular source from which to obtain a proxy.
- `source_name`: name of the source from which to get a proxy
- `amount`: specifies the amount of proxies required
- `proxy_type`: specifies the type of proxy (https, http, socks4)

.. code-block:: python

    >>> import fake_proxy
    >>> fake_proxy.get_from_source(source_name='free-proxy-list.net', amount=2, proxy_type='http')
    [{'ip': '76.87.101.188', 'port': '38875', 'country_code': 'US', 'country': 'United States', 'type': 'http'},
    {'ip': '62.182.206.19', 'port': '37715', 'country_code': 'RU', 'country': 'Russian Federation', 'type': 'http'}]


`proxy_sources()`
~~~~~~~~~~~~~~~~~

Returns a list with the names of all the sources from which the library fetches proxies.

.. code-block:: python

    >>> import fake_proxy
    >>> fake_proxy.proxy_sources()
    {'https': ['free-proxy-list.net'],
    'socks4': ['socks-proxy.net'],
    'http': ['free-proxy-list.net']}


`reload()`
~~~~~~~~~~

Fetches new proxies from the proxy sources.


Sources
-------

For the moment, the library fetches the proxies from the following sources:

+------------------------------+-------------+
| Source URL                   | Proxy Types |
+==============================+=============+
| https://free-proxy-list.net/ | HTTP, HTTPS |
+------------------------------+-------------+
| https://www.sslproxies.org/  | HTTPS       |
+------------------------------+-------------+
| https://www.socks-proxy.net/ | SOCKS4      |
+------------------------------+-------------+


Installation
------------

Latest release through PyPI:

.. code-block:: sh

    $ pip install fake-proxy

Development version:

.. code-block:: sh

    $ git clone git@github.com:machinia/fake-proxy.git
    $ cd fake-proxy
    $ pip install -e .


Contribution
------------

Contributions are welcome! Feel free to report bugs or open an issue if you feel a new feature is needed. Pull requests are welcome!

