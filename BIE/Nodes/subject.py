import urllib
import re
import json

import pandas as pd

from Explorer.Nodes.abstract_node import Node
from Explorer.Nodes.indicator import Indicator
from Explorer.fetcher import Fetcher
import concurrent.futures


class Subject(Node):
    def __init__(self, name, series_key,d):
        self.name=name
        self.series_key=series_key
        self.info = d

    def get_childs(self):
        js=Fetcher.get_children_nodes(self.series_key)
        childs = []
        for d in js:
            if d.get('tipoNodo')=='INDICADOR':
                childs+=[Indicator.from_dict(d)]
            elif  d.get('tipoNodo')=='TEMA':
                childs+=[Subject.from_dict(d)]
            else:
                print(d.get('tipoNodo'))
        return childs

    @classmethod
    def from_dict(cls,d):
        return cls(d['tema']['nombre'],d['claveSerie'],d)

    def __repr__(self):
        return f" Tema: {self.name}"

    def fetch(self):
        indicators = Fetcher.get_indicators_by_subject(self.series_key)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(Fetcher.get_series, indicator) for indicator in indicators]
            concurrent.futures.wait(futures)
            series_list = [future.result() for future in futures]

            # Concatenate the series into a single DataFrame
        df = pd.concat(series_list, axis=1)

        return df

