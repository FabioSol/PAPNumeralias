from BIE.Nodes.abstract_node import Node
from BIE.Nodes.subject import Subject

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
            for child in self.children:
                if child.name == item:
                    return Explorer(child,visualization_level=self.visualization_level)
            raise KeyError(f"No child found with the name '{item}'")

    def fetch(self):
        return self.node.fetch()


