class TrieNode(object):
    __slots__ = "_char", "_val", "_parent", "_children"

    def __init__(self, char, value=None, parent=None):
        self._char = char
        self._val = value
        if parent is not None:
            self._parent = parent
        else:
            self._parent = None
        self._children = {}

    def is_leaf(self):
        return len(self.children) == 0

    def has_children(self):
        return len(self.children) != 0

    @property
    def char(self):
        return self._char

    @char.setter
    def char(self, value):
        self._char = value

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._val = value

