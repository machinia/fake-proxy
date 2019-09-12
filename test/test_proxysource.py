from unittest import TestCase
from test.sample_proxysources.no_metadata.no_metadata import NoMetadata
from test.sample_proxysources.valid_metadata.valid_metadata \
    import ValidMetadataSource
from test.sample_proxysources.incomplete_metadata.incomplete_metadata \
    import IncompleteMetadata
from test.sample_proxysources.missing_abstract_impl.missing_abstract_impl \
    import NotImplementedMethod
from fake_proxy.core.exceptions import ProxyTypeError


class TestProxySource(TestCase):

    def test_metadata_errors(self):
        """
        Test returned error messages when attempting to instantiate
        """
        test_data = [
            (NoMetadata, '"name" not defined in metadata'),
            (IncompleteMetadata, '"url" not defined in metadata'),
        ]

        for cls, expected_stdout in test_data:
            with self.assertRaises(AttributeError) as err:
                cls()
            self.assertEqual(expected_stdout, str(err.exception))

    def test_abstract_implementation(self):
        """
        Test class instantiation without the required abstract
        method implementation
        """
        expected = 'Can\'t instantiate abstract class NotImplementedMethod ' \
                   'with abstract methods _scrape'
        with self.assertRaises(TypeError) as err:
            NotImplementedMethod()
        self.assertEqual(expected, str(err.exception))

    def test_get_method(self):
        """
        Test class get method
        """
        test_data = [
            ('https', 82),
            ('http', 99),
            ('socks4', 80)
        ]

        s = ValidMetadataSource()

        self.assertEqual(len(s.proxies), 261)
        for proxy_type, amount in test_data:
            expected_length = amount
            self.assertEqual(expected_length,
                             len(s.proxies_by_type[proxy_type]))

            for i in range(amount):
                r = s.get(proxy_type)
                expected_length -= 1
                self.assertEqual(r['type'], proxy_type)
                self.assertEqual(len(s.proxies_by_type[proxy_type]),
                                 expected_length)

    def test_get_invalid_proxy_type(self):
        """
        Test class get method with an invalid proxy type
        """
        expected_stdout = 'The source doesn\'t manage this type'
        cls = ValidMetadataSource()
        with self.assertRaises(ProxyTypeError) as err:
            cls.get('invalid_proxy_type')
        self.assertEqual(expected_stdout, str(err.exception))
