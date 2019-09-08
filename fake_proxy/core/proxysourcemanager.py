import os
import re
import ast
import random
import importlib.util
from fake_proxy.core.proxysource import ProxySource

HERE = os.path.abspath(os.path.dirname(__file__))
DEFAULT_PATH = os.path.join(HERE, os.path.pardir, 'sources')


class ProxySourceManager(object):
    VALID_FILE_REGEX = r'(([a-zA-Z0-9]+)|-|_)+[^__]\.py'
    instances = {}

    def __init__(self):
        path = os.getenv('PROXY_PATH', DEFAULT_PATH)
        if not os.path.isdir(path):
            raise AttributeError('Invalid path {}'.format(path))

        self.proxies = {}
        self.load(path)

    def load(self, path):
        """
        Loads all the valid proxies found in the path received
        :param path: string with the path to a folder where proxies are stored
        :return: Nothing
        """
        self.proxies = {}
        self.proxies_per_type = {}
        for f in os.listdir(path):
            if not re.match(self.VALID_FILE_REGEX, f):
                continue

            proxy_file = os.path.join(path, f)
            try:
                sp = self.__load_proxy_from_file(proxy_file)
                p = {}
                for k in sp.metadata.keys():
                    p[k] = sp.metadata[k]
                p['instance'] = sp

                self.proxies[sp.metadata['name']] = p

                for k in sp.metadata['type']:
                    if k not in self.proxies_per_type:
                        self.proxies_per_type[k] = []
                    self.proxies_per_type[k].append(p['name'])

            except (AttributeError, ImportError) as e:
                print('Skipped {}: {}'.format(f, e))
                continue

    def __load_proxy_from_file(self, filename):
        """
        Loads a proxy from a certain file. The file must contain
        only one class, derived from BaseSpider
        :param filename: string containing the path to the definition
        of a proxy
        :return: constructor of the class if it was properly loaded,
        None otherwise
        """
        with open(filename) as f:
            node = ast.parse(f.read())

        classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
        if len(classes) > 1:
            raise AttributeError('File can\'t contain more than one class')
        proxy_name = classes[0].name

        spec = importlib.util.spec_from_file_location(
            proxy_name, filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.__validate_module(module, proxy_name)

        return getattr(module, proxy_name)

    def __validate_module(self, module, classname):
        """
        Validates that the module received is a valid proxy definition
        :param module: python module
        :return: Nothing. Raises exception on failure.
        """
        cls = getattr(module, classname)
        ProxySource.check_metadata(cls.metadata)

        if not issubclass(cls, ProxySource):
            msg = '{} found doesn\'t derive from Proxy'.format(classname)
            raise ImportError(msg)

    def instance(self, name):
        """
        Returns an instance of a class with the given name.
        :param name: string with the proxy name
        : return: constructor of the desired class. None on error.
        """
        sp = self.proxies.get(name)
        if not sp:
            return None

        if name not in self.instances:
            self.instances[name] = sp.get('instance')()
        return self.instances[name]
