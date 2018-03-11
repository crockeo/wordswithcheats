import os.path
import os

###
# TrieNode
#
# A single node in a WordTrie. Contains its letter, a map to its children, and
# whether or not this is a 'terminal' node (that is, a node to which a letter is
# the terminus of some word).
class TrieNode:
    def __init__(self, letter, end=False):
        self.letter = letter
        self.end = end
        self.children = dict()

###
# WordTrie
#
# A trie built from the ENABLE database (if no other word database is provided).
class WordTrie:
    def __init__(self, src='words/ENABLE.txt'):
        self.root = TrieNode('')
        self.initialize(src)

    # Re-initializing the WordTrie from a database.
    def initialize(self, src):
        f = open(src, 'r')

        for line in f:
            line = line.strip()
            n = self.root
            for c in line:
                if c not in n.children:
                    n.children[c] = TrieNode(c)
                n = n.children[c]
            n.end = True
        f.close()

    # Checking if a word exists in the Trie.
    def has_word(self, word):
        n = self.root
        for c in word:
            if c not in n.children:
                return False
            n = n.children[c]
        return n.end
