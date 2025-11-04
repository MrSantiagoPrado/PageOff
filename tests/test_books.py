# tests/test_books.py

import os
from app.core import books

DATA_DIR = "data"
SEED_PATH = os.path.join(DATA_DIR, "books_seed.json")

def test_load_seed_returns_book_objects():
    result = books.load_seed(SEED_PATH)
    assert isinstance(result, dict)
    assert all(isinstance(b, books.Book) for b in result.values())
    assert len(result) > 0

def test_save_and_load_state(tmp_path):
    # Create dummy books
    dummy_books = {
        "1": books.Book(id="1", title="T1", author="A1"),
        "2": books.Book(id="2", title="T2", author="A2"),
    }
    path = tmp_path / "state.json"
    books.save_state(dummy_books, path)
    loaded = books.load_state(path)
    assert set(loaded.keys()) == set(dummy_books.keys())
    assert isinstance(loaded["1"], books.Book)

def test_select_pair_unique_ids():
    result = books.load_seed(SEED_PATH)
    a, b = books.select_pair(result)
    assert a.id != b.id

def test_select_pair_nearby_returns_two_books():
    result = books.load_seed(SEED_PATH)
    a, b = books.select_pair_nearby(result, window=500)
    assert isinstance(a, books.Book)
    assert isinstance(b, books.Book)
    assert a.id != b.id
