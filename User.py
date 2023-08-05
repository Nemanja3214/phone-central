class User(object):
    __slots__ = "_name", "_surname", "_number", "_vertex", "_trie_node"

    def __init__(self, name, surname, number, vertex=None, trie_node=None):
        self._name = name
        self._surname = surname
        self._number = number
        self._vertex = vertex
        self._trie_node = trie_node

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        self._surname = value

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value

    @property
    def vertex(self):
        return self._vertex

    @vertex.setter
    def vertex(self, value):
        self._vertex = value

    @property
    def trie_node(self):
        return self._trie_node

    @trie_node.setter
    def trie_node(self, value):
        self._trie_node = value

    def __str__(self):
        return self._name + " " + self._surname + " with number " + self._number
