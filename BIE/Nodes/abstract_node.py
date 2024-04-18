from abc import ABC, abstractmethod
from BIE.fetcher import Fetcher


class Node(ABC):
    name: str
    series_key: str
    info : dict

    @abstractmethod
    def get_childs(self):
        pass

    @abstractmethod
    def fetch(self):
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls,d):
        return cls()

    def request(self, url):
        return Fetcher.request_url(url)

