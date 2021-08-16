from abc import abstractmethod, abstractproperty
from requests.auth import HTTPBasicAuth
from enum import Enum
import requests, random, threading

class ProxyPolicy(Enum):
    RANDOM = 1
    ROUND_ROBIN = 2

class ProxyPicker:
    get_proxy_list = None

    def __init__(self, get_proxy_list) -> None:
        self.get_proxy_list = get_proxy_list

    @abstractmethod
    def next(self):
        pass

class RandomProxyPicker(ProxyPicker):
    def __init__(self, get_proxy_list) -> None:
        super().__init__(get_proxy_list)

    def next(self):
        return self.get_proxy_list()[random.randint(0, len(self.get_proxy_list())-1)]

class RoundRobinProxyPicker(ProxyPicker):
    def __init__(self, get_proxy_list) -> None:
        super().__init__(get_proxy_list)
        self._current_index = 0
        self._lock = threading.Lock()

    def next(self):
        with self._lock:
            ret = self.get_proxy_list()[self._current_index]
            self._current_index+=1
            self._current_index%=len(self.get_proxy_list())
            return ret

class ProxyPickerFactory:
    @classmethod
    def get_proxy_picker(cls, proxy_policy, get_proxy_list)->ProxyPicker:
        if proxy_policy == ProxyPolicy.RANDOM:
            return RandomProxyPicker(get_proxy_list)
        elif proxy_policy == ProxyPolicy.ROUND_ROBIN:
            return RoundRobinProxyPicker(get_proxy_list)

class ProxyManager:
    _proxy_list = []

    def __init__(self, url, username, password, proxy_policy = ProxyPolicy.RANDOM):
        self._username = username
        self._password = password
        self._url = url
        self._proxy_picker = ProxyPickerFactory.get_proxy_picker(proxy_policy, self._get_proxy_list)

    def refresh_proxy_list(self):
        print('Looking for list of available proxy')
        self._proxy_list = ProxyManager.fetch_proxy_list(self._url, self._username, self._password)
        print('New list of proxies:')
        print(self._proxy_list)
        print(len(self._proxy_list), 'proxy servers found')

    def next(self):
        url = self._proxy_picker.next()
        credential = self._username + ':' + self._password
        return {
            'https': 'http://' + credential + '@' + url,
            'http': 'http://' + credential + '@' + url
        }

    @classmethod
    def fetch_proxy_list(cls, url, username, password):
        res = requests.get(url, auth=HTTPBasicAuth(username, password))
        if res.status_code == 200:
            return res.json()['proxies']

    def _get_proxy_list(self):
        return self._proxy_list

if __name__ == "__main__":
    pm = ProxyManager("", "", "")
    pm.refresh_proxy_list()