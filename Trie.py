from TrieNode import TrieNode


class Trie(object):
    __slots__ = "_root"

    def __init__(self):
        self._root = TrieNode("")

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root = value

    def insert(self, word, value, node=None):
        word = word.lower()
        if node is None:
            node = self._root
        next = node

        for char in word:
            if next.children.get(char) is None:
                next.children[char] = TrieNode(char, None, next)
            next = next.children[char]
        next.val = value
        return next

    def find(self, word, node=None):
        word = word.lower()
        if node is None:
            node = self._root
        next = node

        for char in word:
            if next.children.get(char) is not None:
                next = next.children[char]
            else:
                return None
        return next.val

    def _find_node(self, word, node=None):
        word = word.lower()
        if node is None:
            node = self._root
        next = node

        for char in word:
            if next.children.get(char) is not None:
                next = next.children[char]
            else:
                return None
        return next

    def prefix_words(self, prefix="", node=None, ret_func=None):
        if ret_func is None:
            ret_func = ret_val

        prefix = prefix.lower()
        if node is None:
            next = self._root
        else:
            next = node

        if prefix != "":
            prefix_node = self._find_node(prefix, node)
        else:
            prefix_node = self._root
        if prefix_node is None:
            return []

        suggestions = []
        prefix = prefix[:-1]
        self.collect_prefix_list(prefix_node, prefix, suggestions, ret_func)

        return suggestions

    def collect_prefix_list(self, node, prefix, suggestions, ret_func):
        prefix += node.char

        if node.is_leaf():
            suggestions.append(ret_func(node))
            return None

        for child_char in node.children:
            self.collect_prefix_list(node.children.get(child_char), prefix, suggestions, ret_func)


def ret_val(node):
    return node.val


if __name__ == '__main__':
    tr = Trie()
    tr.insert('bear', "bear")
    tr.insert('bell', "bell")
    tr.insert('bely', "bely")
    tr.insert('beckah', "beckah")
    tr.insert('becky', "becky")
    # print(tr._find_node("bear").is_leaf())
    # print(find_best("bel",tr))
    # print(tr.visit_leafs(tr.root, []))
    # traverse(tr.root, result_list, "bel")
    # print(traverse(tr.root, result_list, "bea"))

    # print(tr.find("bear"))
    # print(tr.prefix_word("be"))
