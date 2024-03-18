#!/usr/bin/env python3
"""
Tests for the Trie spelling method.
"""
import unittest
from src.trie import Trie


class TestCorrectSpelling(unittest.TestCase):
    """
    Test case for the Trie correct_spelling method.
    """
    def test_multiple_possible_matches(self):
        """
        Test the correct_spelling method with multiple possible matches.
        """
        trie = Trie()
        words = ['frake', 'great', 'flore', 'glare', 'fnate', 'frami', 'fldre']
        for word in words:
            trie.add_word(word)
        result = trie.correct_spelling('flare')
        self.assertEqual(result, ['fldre', 'flore', 'fnate', 'frake', 'glare'])

    def test_possible_matches(self):
        """
        Test the correct_spelling method with possible matches.
        """
        trie = Trie.create_from_file()
        result = trie.correct_spelling('xlare')
        expected = ['blade', 'blame', 'blate', 'blaze', 'flake', 'flame', 'flare',
                    'glade', 'glare', 'glaze', 'place', 'plane', 'plate', 'slate', 'slave']
        self.assertEqual(result, expected)

    def test_possible_matches_2(self):
        """
        Test the correct_spelling method with possible matches.
        """
        trie = Trie.create_from_file()
        result = trie.correct_spelling('hillo')
        expected = ['bilbo', 'hallo', 'hello', 'hullo']
        self.assertEqual(result, expected)

    def test_misplaced_letter(self):
        """
        Test the correct_spelling method with a misplaced letter.
        """
        trie = Trie()
        words = ['flare', 'flake', 'fxary', 'glare', 'xare']
        for word in words:
            trie.add_word(word)
        result = trie.correct_spelling('fxare')
        self.assertEqual(result, ['flake', 'flare'])

    def test_existing_word(self):
        """
        Test the correct_spelling method with an existing word.
        """
        trie = Trie()
        words = ['hej', 'hoj', 'haj', 'dej']
        for word in words:
            trie.add_word(word)
        result = trie.correct_spelling('hej')
        self.assertEqual(result, ['hej'])


if __name__ == '__main__':
    unittest.main()
