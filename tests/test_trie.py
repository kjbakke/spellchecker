#!/usr/bin/env python3
"""
Tests for the Trie class.
"""

import unittest
from src.trie import Trie
from src.exceptions import SearchMiss


class TestTrie(unittest.TestCase):
    """
    Test case for the Trie class.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.trie = Trie()

    def test_add_word(self):
        """
        Test the add_word method.
        """
        self.trie.add_word("test")
        self.assertEqual(self.trie.word_count, 1)

    def test_search_word_exists(self):
        """
        Test the search method with a word that exists.
        """
        self.trie.add_word("test")
        self.assertTrue(self.trie.search("test"))

    def test_search_word_does_not_exist(self):
        """
        Test the search method with a word that does not exist.
        """
        with self.assertRaises(SearchMiss):
            self.trie.search("test")

    def test_remove_word_exists(self):
        """
        Test the remove method with a word that exists.
        """
        self.trie.add_word("test")
        self.trie.remove("test")
        self.assertEqual(self.trie.word_count, 0)

    def test_remove_word_does_not_exist(self):
        """
        Test the remove method with a word that does not exist.
        """
        with self.assertRaises(SearchMiss):
            self.trie.remove("test")

    def test_count_words(self):
        """
        Test the count_words method.
        """
        self.trie.add_word("test")
        self.trie.add_word("example")
        self.assertEqual(self.trie.word_count, 2)

    def test_prefix_search(self):
        """
        Test the prefix_search method.
        """
        self.trie.add_word("test")
        self.trie.add_word("testing")
        self.assertEqual(self.trie.prefix_search("test"), [("test", 1), ("testing", 1)])

    def test_get_words(self):
        """
        Test the get_words method.
        """
        self.trie.add_word("test")
        self.trie.add_word("testing")
        self.assertEqual(self.trie.get_words(), [("test", 1), ("testing", 1)])


if __name__ == "__main__":
    unittest.main()
