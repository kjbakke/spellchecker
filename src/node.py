#!/usr/bin/env python3
"""
A trie data structure.
"""


class Node:
    """
    A node class for the trie.
    """
    def __init__(self, char):
        self.char = char.lower()
        self.children = {}
        self.is_end = False
        self.frequency = 1
