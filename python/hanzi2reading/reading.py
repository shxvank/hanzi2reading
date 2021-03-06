import os
import sys
from enum import Enum
from hanzi2reading.serialize import read

class TrieNode:
    def __init__(self):
        self.val = None
        self.children = {}

class Trie:
    def __init__(self):
        self._t = TrieNode()

    def add(self,s,value):
        node = self._t
        for idx,c in enumerate(s):
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
            if idx == len(s)-1:
                node.val = value

    def get(self,s):
        reading = []
        i = 0
        while i < len(s):
            j = i
            node = self._t
            candidate = []
            candidate_depth = 0
            depth = 0
            if s[j] not in node.children:
                i = i + 1
                continue
            while j < len(s) and s[j] in node.children:
                node = node.children[s[j]]
                depth = depth + 1
                if node.val:
                    candidate_depth = depth
                    candidate = node.val
                j = j + 1

            reading = reading + candidate
            i = i + candidate_depth

        return reading

class Builtin(Enum):
    CEDICT = 1
    MOEDICT = 2
    UNIHAN = 3

class Reading:
    def __init__(self,fname=None):
        self._trie = Trie()

        if fname == Builtin.CEDICT:
            fname = os.path.join(os.path.dirname(__file__), 'data/cedict.h2r')
        elif fname == Builtin.MOEDICT or not fname:
            fname = os.path.join(os.path.dirname(__file__), 'data/moedict.h2r')
        elif fname == Builtin.UNIHAN:
            fname = os.path.join(os.path.dirname(__file__), 'data/unihan.h2r')
        elif fname == Builtin.UNIHAN_CEDICT:
            fname = os.path.join(os.path.dirname(__file__), 'data/unihan-cedict.h2r')


        with open(fname,'rb') as f:
            for headword, syllables in read(f):
                self._trie.add(headword,syllables)

    def get(self,hanzi):
        return self._trie.get(hanzi)

