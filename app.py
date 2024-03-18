#!/usr/bin/env python3
"""
Spellchecker app
"""
import os
import re
import traceback
from flask import Flask, render_template, session, redirect, url_for, request

from src.exceptions import SearchMiss
from src.trie import Trie


app = Flask(__name__)
app.secret_key = re.sub(r"[a-z\d]", "", os.path.realpath(__file__))


@app.route("/")
def index():
    """
    Index page
    """
    if 'file' not in session:
        session['file'] = 'frequency.txt'

    return render_template('index.html')


@app.route('/check_word', methods=['GET', 'POST'])
def check_word():
    """
    Check if a word exists in the trie.
    """
    if request.method == 'POST':
        word = request.form.get('word')
        file_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(file_dir, session['file'])
        trie = Trie.create_from_file(file_path)
        for removed_word in session.get('removed_words', []):
            trie.remove(removed_word)
        try:
            exists = trie.search(word)
        except SearchMiss:
            exists = False
        return render_template('check_word.html', word=word, exists=exists)
    return render_template('check_word.html', word='', exists=None)


@app.route('/prefix_search', methods=['GET', 'POST'])
def prefix_search():
    """
    Search for words with a specific prefix.
    """
    if request.method == 'POST':
        prefix = request.form.get('prefix')
        file_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(file_dir, session['file'])
        trie = Trie.create_from_file(file_path)
        for removed_word in session.get('removed_words', []):
            trie.remove(removed_word)
        words = trie.prefix_search(prefix)
        return render_template('prefix_search.html', prefix=prefix, words=words)
    return render_template('prefix_search.html', prefix='', words=[])


@app.route('/suffix_search', methods=['GET', 'POST'])
def suffix_search():
    """
    Search for words with a specific suffix.
    """
    if request.method == 'POST':
        suffix = request.form.get('suffix')
        file_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(file_dir, session['file'])
        trie = Trie.create_from_file(file_path)
        for removed_word in session.get('removed_words', []):
            trie.remove(removed_word)
        words = trie.suffix_search(suffix)
        return render_template('suffix_search.html', suffix=suffix, words=words)
    return render_template('suffix_search.html', suffix='', words=[])


@app.route('/correct_spelling', methods=['GET', 'POST'])
def correct_spelling():
    """
    Suggest/correct the spelling of a word.
    """
    if request.method == 'POST':
        word = request.form.get('word')
        file_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(file_dir, session['file'])
        trie = Trie.create_from_file(file_path)
        for removed_word in session.get('removed_words', []):
            trie.remove(removed_word)
        words = trie.correct_spelling(word)
        return render_template('correct_spelling.html', word=word, words=words)
    return render_template('correct_spelling.html', word='', correction='')


@app.route('/all_words')
def all_words():
    """
    Get all words in the trie.
    """
    file_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(file_dir, session['file'])
    trie = Trie.create_from_file(file_path)
    if 'removed_words' in session:
        for removed_word in session['removed_words']:
            trie.remove(removed_word)
    words = trie.get_words()
    words_by_letter = {letter: [] for letter in 'abcdefghijklmnopqrstuvwxyz'}
    for word in words:
        words_by_letter[word[0][0]].append(word[0])
    return render_template('all_words.html',
                           words_by_letter=words_by_letter, total_words=len(words))


@app.route('/remove_word', methods=['GET', 'POST'])
def remove_word():
    """
    Remove a word.
    """
    if request.method == 'POST':
        word = request.form.get('word')
        file_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(file_dir, session['file'])
        trie = Trie.create_from_file(file_path)
        try:
            trie.remove(word)
            if 'removed_words' not in session:
                session['removed_words'] = []
            session['removed_words'].append(word)
            session.modified = True
            result = f"'{word}' is removed."
        except SearchMiss:
            result = f"{word}' does not exist in the dictionary."
        return render_template('remove_word.html', result=result)
    return render_template('remove_word.html', result='')


@app.route('/change_file', methods=['GET', 'POST'])
def change_file():
    """
    Change the file.
    """
    if request.method == 'POST':
        file = request.form.get('file')
        session['file'] = file
        session.pop('removed_words', None)
        return redirect(url_for('index'))
    file_dir = os.path.dirname(os.path.realpath(__file__))
    files = [f for f in os.listdir(file_dir) if f.endswith('.txt')]
    return render_template('change_file.html', files=files)


@app.route('/clear_session')
def clear_session():
    """
    Clear the session.
    """
    session.clear()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    """
    Handler for page not found 404
    """
    # pylint: disable=unused-argument
    return "Flask 404 here, but not the page you requested."


@app.errorhandler(500)
def internal_server_error(e):
    """
    Handler for internal server error 500
    """
    # pylint: disable=unused-argument
    return "<p>Flask 500<pre>" + traceback.format_exc()


if __name__ == "__main__":
    app.run(debug=True)
