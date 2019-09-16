import os
from unittest import TestCase
from fake_proxy.core.proxysourcemanager import ProxySourceManager
from test.sample_proxysources.valid_metadata.valid_metadata \
    import ValidMetadataSource
from fake_proxy.core.exceptions import InvalidProxySource


class TestProxySourceManager(TestCase):

    def tearDown(self):
        if 'PROXY_PATH' in os.environ:
            del os.environ['PROXY_PATH']

    def test_invalid_path(self):
        """
        Tests an invalid path as parameter
        """
        path = '/invalidpath'
        os.environ['PROXY_PATH'] = path
        self.assertRaises(AttributeError, ProxySourceManager)

    def test_several_folders(self):
        """
        Searches for sources in several folders with
        valid and invalid proxy source classes
        """
        source_path = 'test/sample_proxysources/'
        test_data = [
            ('valid_metadata', 1, 3),
            ('no_metadata', 0, 0),
            ('incomplete_metadata', 0, 0),
            ('two_classes_one_file', 0, 0),
            ('no_inheritance', 0, 0),
        ]

        for name, valid_classes, valid_types in test_data:
            path = source_path + name
            os.environ['PROXY_PATH'] = path

            m = ProxySourceManager()
            if valid_classes:
                inst = m.instance(name)
                types = inst.metadata['type']
                for t in types:
                    self.assertEqual(len(m.proxies_per_type[t]), valid_classes)

            self.assertEqual(type(m.proxies_per_type), dict)
            self.assertEqual(len(m.proxies_per_type), valid_types)

    def test_manager_instances_success(self):
        """
        Tests return of instance method when requesting a loaded source classes
        """
        source_name = 'valid_metadata'
        path = 'test/sample_proxysources/' + source_name
        os.environ['PROXY_PATH'] = path

        m = ProxySourceManager()
        inst = m.instance(source_name)
        self.assertEqual(inst.__class__.__name__, ValidMetadataSource.__name__)

    def test_manager_instances_not_found(self):
        """
        Tests response when requesting the instance of a source class
        that isn't loaded
        """
        source_name = 'no_metadata'
        path = 'test/sample_proxysources/' + source_name
        os.environ['PROXY_PATH'] = path
        expected_stdout = 'The source doesn\'t exist'

        m = ProxySourceManager()
        with self.assertRaises(InvalidProxySource) as err:
            m.instance(source_name)
        self.assertEqual(expected_stdout, str(err.exception))

    def test_remove_valid_source_valid_type(self):
        """
        Test source removal from manager memory, happy path
        """
        name = 'valid_metadata'
        path = 'test/sample_proxysources/valid_metadata'
        os.environ['PROXY_PATH'] = path
        types = ValidMetadataSource.metadata.get('type')

        m = ProxySourceManager()

        for t in types:
            m.remove_source(source_name=name, proxy_type=t)
            self.assertEqual(len(m.proxies_per_type.get(t)), 0)

    def test_remove_valid_source_invalid_type(self):
        """
        Test source removal from manager memory with an invalid proxy type and
        a valid source
        """
        name = 'valid_metadata'
        path = 'test/sample_proxysources/' + name
        os.environ['PROXY_PATH'] = path
        incorrect_type = 'invalid_proxy_type'
        correct_types = ValidMetadataSource.metadata.get('type')

        m = ProxySourceManager()
        m.remove_source(source_name=name, proxy_type=incorrect_type)
        for t in correct_types:
            self.assertEqual(len(m.proxies_per_type.get(t)), 1)

    def test_remove_invalid_source_valid_type(self):
        """
        Test source removal from manager memory with an invalid proxy source
        and a valid proxy type
        """
        path = 'test/sample_proxysources/valid_metadata'
        os.environ['PROXY_PATH'] = path
        types = ValidMetadataSource.metadata.get('type')

        m = ProxySourceManager()
        for t in types:
            m.remove_source(source_name='not_the_correct_name', proxy_type=t)
            self.assertEqual(len(m.proxies_per_type.get(t)), 1)

    def test_remove_invalid_source_invalid_type(self):
        """
        Test source removal from manager memory with an invalid proxy source
        and an invalid proxy type
        """
        path = 'test/sample_proxysources/valid_metadata'
        os.environ['PROXY_PATH'] = path
        correct_types = ValidMetadataSource.metadata.get('type')

        m = ProxySourceManager()
        m.remove_source(source_name='not_the_correct_name',
                        proxy_type='invalid_proxy_type')
        for t in correct_types:
            self.assertEqual(len(m.proxies_per_type.get(t)), 1)
