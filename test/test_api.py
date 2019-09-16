import os
from unittest import TestCase
from fake_proxy.core import api
from fake_proxy.core.exceptions import ProxyTypeError


class TestApi(TestCase):

    def tearDown(self):
        if 'PROXY_PATH' in os.environ:
            del os.environ['PROXY_PATH']

    def setUp(self):
        path = 'test/sample_proxysources/valid_metadata'
        os.environ['PROXY_PATH'] = path
        api.reload()

    def test_api_proxy_sources(self):
        """
        Tests proxy sources api format
        """
        ps = api.proxy_sources()

        self.assertEqual(type(ps), dict)
        self.assertEqual(len(ps), 3)
        for k, v in ps.items():
            self.assertEqual(len(v), 1)

    def test_api_get_from_source_type_string(self):
        """
        Test get_from_source method with proxy_type parameter as a string
        """
        source = 'valid_metadata'
        data = [
            ('https', 82),
            ('http', 99),
            ('socks4', 80)
        ]

        for t, amount in data:
            r = api.get_from_source(
                source_name=source,
                amount=1000,
                proxy_type=t
            )
            self.assertEqual(len(r), amount)
            self.assertEqual(len(api.proxy_sources(t).get(t)), 0)

    def test_api_get_from_source_type_list(self):
        """
        Test get_from_source method with proxy_type parameter as a list
        """
        amount = 1000
        source = 'valid_metadata'
        types = ['https', 'http', 'socks4']

        r = api.get_from_source(
            source_name=source,
            amount=amount,
            proxy_type=types
        )
        self.assertEqual(len(r), 261)
        self.assertEqual(len(api.proxy_sources()), 3)
        for t in types:
            self.assertEqual(len(api.proxy_sources(t).get(t)), 0)

    def test_api_get(self):
        """
        Test get method
        """
        data = [
            ('https', 82),
            ('http', 99),
            ('socks4', 80)
        ]

        for t, amount in data:
            r = api.get(
                amount=1000,
                proxy_type=t)
            self.assertEqual(len(r), amount)
            self.assertEqual(len(api.proxy_sources(t).get(t)), 0)

    def test_api_invalid_proxy_type_format(self):
        """
        Test format_proxy_type method with invalid inputs
        """
        err_msgs = {
            TypeError: 'Invalid proxy_type type, must be a string or a list',
            ProxyTypeError: 'The library doesn\'t manage the required type. '
                            'Choose from [\'http\', \'https\', \'socks4\']'
        }

        data = [
            (1, TypeError),
            (0.1, TypeError),
            ([1, 2, 3], TypeError),
            ({'a': 1}, TypeError),
            ([1, 'b'], TypeError),
            ('anything', ProxyTypeError),
            (['a', 'b'], ProxyTypeError),
        ]

        for p_type, exc in data:
            with self.assertRaises(exc) as e:
                api.format_proxy_type(p_type)
            self.assertEqual(err_msgs[exc], str(e.exception))

    def test_api_proxy_type_format(self):
        """
        Test format_proxy_type method with valid inputs
        """
        data = [
            ('http', ['http']),
            (['http', 'https'], ['http', 'https']),
            ([], ['https', 'http', 'socks4']),
            (None, ['https', 'http', 'socks4'])
        ]

        for input, expected in data:
            output = api.format_proxy_type(input)
            self.assertEqual(set(output), set(expected))
