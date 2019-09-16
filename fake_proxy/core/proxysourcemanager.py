import os
import re
import ast
import importlib.util
from fake_proxy.core.proxysource import ProxySource
from fake_proxy.core.exceptions import InvalidProxySource


HERE = os.path.abspath(os.path.dirname(__file__))
DEFAULT_PATH = os.path.join(HERE, os.path.pardir, 'sources')


class ProxySourceManager(object):
    VALID_FILE_REGEX = r'(([a-zA-Z0-9]+)|-|_)+[^__]\.py'

    def __init__(self):
        self.__source_info = {}
        self.load()

    def load(self):
        """
        Loads all the valid proxies found to memory
        :return: Nothing
        """
        path = os.getenv('PROXY_PATH', DEFAULT_PATH)
        if not os.path.isdir(path):
            raise AttributeError('Invalid path {}'.format(path))

        self.instances = {}
        self.__source_info = {}
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
                self.__source_info[sp.metadata['name']] = p

                for k in sp.metadata['type']:
                    if k not in self.proxies_per_type:
                        self.proxies_per_type[k] = []
                    self.proxies_per_type[k].append(p['name'])

            except (AttributeError, ImportError, TypeError) as e:
                print('Skipped {}: {}'.format(f, e))
                continue

    def __load_proxy_from_file(self, filename):
        """
        Loads a proxy from a certain file. The file must contain
        only one class, derived from ProxySource
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

        spec = importlib.util.spec_from_file_location(proxy_name, filename)
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
        sp = self.__source_info.get(name)
        if not sp:
            raise InvalidProxySource('The source doesn\'t exist')

        if name not in self.instances:
            self.instances[name] = sp.get('instance')()
        return self.instances[name]

    def remove_source(self, source_name, proxy_type):
        """
        Safely removes a proxy source from the loaded modules for a particular
        proxy type
        :param source_name: string, proxy source name
        :param proxy_type: string, proxy type from which to delete the source
        :return: Nothing
        """
        if proxy_type not in self.proxies_per_type or \
                source_name not in self.proxies_per_type[proxy_type]:
            return

        self.proxies_per_type[proxy_type].remove(source_name)
        for k, v in self.proxies_per_type.items():
            if source_name in v:
                return
        self.__source_info.pop(source_name)
