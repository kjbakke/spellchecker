#!/usr/bin/env python3
"""
A trie data structure.
"""
from src.node import Node
from src.exceptions import SearchMiss


class Trie:
    """
    A trie data structure class.
    """
    def __init__(self):
        self.root = Node("")
        self.word_count = 0

    def add_word(self, word, frequency=1):
        """
        Add a word to the trie.
        """
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = Node(char)
            node = node.children[char]
        if not node.is_end:
            node.is_end = True
            node.frequency = float(frequency)
            self.word_count += 1

    def search(self, word):
        """
        Search for a word in the trie.
        """
        node = self.root
        for char in word.lower():
            if char not in node.children:
                raise SearchMiss(f"The word '{word}' does not exist in the Trie.")
            node = node.children[char]
        if not node.is_end:
            raise SearchMiss(f"The word '{word}' does not exist in the Trie.")
        return True

    def remove(self, word, node=None, depth=0):
        """
        Remove a word from the trie.
        """
        if node is None:
            node = self.root
        if depth == len(word):
            if not node.is_end:
                raise SearchMiss(f"The word '{word}' does not exist in the Trie.")
            node.is_end = False
            self.word_count -= 1
            return len(node.children) == 0
        char = word[depth].lower()
        if char in node.children:
            delete_this_node = self.remove(word, node.children[char], depth + 1)
            if delete_this_node:
                del node.children[char]
                return len(node.children) == 0
        else:
            raise SearchMiss(f"The word '{word}' does not exist in the Trie.")
        return False

    def count_words(self):
        """
        Get the number of words in the trie.
        """
        return self.word_count

    def get_words(self, node=None, prefix='', words=None):
        """
        Get all words in the trie.
        """
        if words is None:
            words = []
        if node is None:
            node = self.root
        if node.is_end:
            words.append((prefix, node.frequency))
        for char, child_node in node.children.items():
            words.extend(self.get_words(child_node, prefix + char))
        return words

    def prefix_search(self, prefix):
        """
        Search for words with a specific prefix.
        """
        node = self.root
        for char in prefix.lower():
            if char in node.children:
                node = node.children[char]
            else:
                return []
        words = self.get_words(node, prefix)
        words.sort(key=lambda x: x[1], reverse=True)
        return words[:10]

    def correct_spelling(self, word):
        """
        Find words that are spelled similarly to the given word.
        """
        def search(node, word, index, prev_matched, prefix):
            if index == len(word):
                if node.is_end and prev_matched:
                    return [prefix]
                return []

            results = []
            for char, child_node in node.children.items():
                if char == word[index]:
                    results.extend(search(child_node, word, index + 1, True, prefix + char))
                elif prev_matched:
                    results.extend(search(child_node, word, index + 1, False, prefix + char))

            return results

        try:
            if self.search(word):
                return [word]
        except SearchMiss:
            pass

        return sorted(search(self.root, word, 0, True, ''))

    def suffix_search(self, suffix, node=None, prefix='', words=None):
        """
        Search for words with a specific suffix.
        """
        if words is None:
            words = []
        if node is None:
            node = self.root

        if node.is_end and prefix.endswith(suffix):
            words.append(prefix)

        for char, child_node in node.children.items():
            self.suffix_search(suffix, child_node, prefix + char, words)

        return sorted(words) if node == self.root else words

    @classmethod
    def create_from_file(cls, file_path='frequency.txt'):
        """
        Create a trie from a file.
        """
        trie = cls()
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                word, frequency = line.strip().split()
                trie.add_word(word, frequency)
        return trie
