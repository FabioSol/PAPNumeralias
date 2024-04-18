from BIE.Nodes.abstract_node import Node
from BIE.fetcher import Fetcher


class Indicator(Node):
    def __init__(self,name, series_key,d):
        self.name=name
        self.series_key=series_key
        self.info = d

    def get_childs(self):
        return None

    @classmethod
    def from_dict(cls,d):
        return cls(d['indicador']['nombre'],d['indicador']['indicador'],d)

    def __repr__(self):
        return f" Indicador: {self.name}"

    def fetch(self):
        return Fetcher.get_series(self.series_key)
