from BIE.Nodes.abstract_node import Node
from BIE.Nodes.subject import Subject
from BIE.fetcher import Fetcher

#https://www.inegi.org.mx/app/indicadores/?tm=0#D444557_10000080018000700110

class Explorer:
    def __init__(self, node:Node=Subject("Origen","999999999999",{}),visualization_level:int = 2,vl=None):
        if vl:
            self.vl=vl
        else:
            self.vl=visualization_level
        self.visualization_level=visualization_level
        self.node = node
        self.children = self.node.get_childs()

    def __repr__(self):
        try:
            indent = '\n'+'    '*(self.vl-self.visualization_level+1)
            return self.node.__repr__() + indent+ indent.\
                join(Explorer(child,
                              self.visualization_level-1,self.vl).__repr__() if self.visualization_level > 2 else child.__repr__()
                              for child in self.children)
        except TypeError:
            return self.node.__repr__()


    def __getitem__(self, item):
        if isinstance(item,int):
            return Explorer(self.children[item],visualization_level=self.visualization_level)
        elif isinstance(item, str):
            if item.isnumeric():
                for child in self.children:
                    if child.info['claveSerie'] == item:
                        return Explorer(child,visualization_level=self.visualization_level)
                raise KeyError(f"No child found with the Series id '{item}'")
            else:
                for child in self.children:
                    if child.name == item:
                        return Explorer(child,visualization_level=self.visualization_level)
                raise KeyError(f"No child found with the name '{item}'")

    def __eq__(self, other):
        if isinstance(other, Explorer):
            if self.info == other.info and self.series_key==other.series_key and self.name == self.name:
                return True
            else:
                return False
        else:
            return False

    @property
    def info(self):
        return self.node.info

    @property
    def series_key(self):
        return self.node.series_key

    @property
    def name(self):
        return self.node.series_key

    @classmethod
    def from_key(cls,key:str,visualization_level:int=2):
        if len(key)>4:
            parent_key = key[:-4]
        else:
            parent_key = "999999999999"
        return cls(Subject("", parent_key,{}),visualization_level)[key]

    @classmethod
    def from_indicator_key(cls, key:str):
        return Fetcher.get_series(key,True)


    def fetch(self):
        return self.node.fetch()


if __name__ == '__main__':
    e = Explorer()
    d1=e[2]
    print(d1)
    print(d1.info)
    print(d1.series_key)
    sk=d1.series_key
    d2 = Explorer.from_key(sk)
    data =d2
    print(d2)


