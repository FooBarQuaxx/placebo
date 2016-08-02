import urlparse
from functools import wraps

from placebo import backends


class Placebo(object):
    """Base class for placebo mocks."""

    # Url that will be mocked
    url = NotImplemented
    body = NotImplemented
    headers = NotImplemented
    # Http method can be ('POST', 'GET', 'PUT', 'DELETE' etc.) default is 'GET'
    method = 'GET'
    # Http status code for response default is 200
    status = 200

    backend = None

    def get_body(self, url, headers, body):
        print('URL=%s, headers=%s, body=%s' % (url, headers, body))
        if self.body is NotImplemented:
            raise NotImplementedError('To use placebo, you need to either '
                                      'provide body attribute or '
                                      'overwrite get_body method in subclass.')
        else:
            return self.body

    def get_headers(self, url, headers, body):
        headers = self.headers
        if headers is NotImplemented:
            headers = {}
        return headers

    def get_url(self):
        if self.body is NotImplemented:
            raise NotImplementedError('To use placebo, you need to either '
                                      'provide url attribute or '
                                      'overwrite get_url method in subclass.')
        else:
            return urlparse.urlparse(self.url)

    def get_method(self):
        return self.method.upper()

    @classmethod
    def get_backend(cls):
        """If backend is provided on child,
        use that backend. if it is not provided,
        go over all backends to find one that can be used.
        """
        if cls.backend is None:
            backend = backends.get_backend()
        else:
            backend = cls.backend
        return backend

    @classmethod
    def mock(cls, f):
        # create a placebo instance for backend
        placebo = cls()
        # choose a backend
        backend = cls.get_backend()
        # ask backend for decorator for current placebo instance.
        decorator = backend(placebo)
        # wrap decorator around curent function.
        return wraps(f)(decorator(f))
