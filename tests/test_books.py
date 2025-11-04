import pytest
from sqlmodel import SQLModel, Session, create_engine, select
from app.core.db import Book
from app.core import books

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all([
            Book(title="Book A", author="Author A", rating=1200),
            Book(title="Book B", author="Author B", rating=1200),
            Book(title="Book C", author="Author C", rating=1200),
        ])
        session.commit()
        yield session

def test_get_all_books(session, monkeypatch):
    monkeypatch.setattr(books, "get_session", lambda: session)
    all_books = books.get_all_books()
    assert len(all_books) == 3

def test_select_pair_nearby(session, monkeypatch):
    monkeypatch.setattr(books, "get_session", lambda: session)
    a, b = books.select_pair_nearby()
    assert a.id != b.id

def test_update_books(session, monkeypatch):
    monkeypatch.setattr(books, "get_session", lambda: session)
    all_books = session.exec(select(Book)).all()
    book_a, book_b = all_books[:2]
    book_a.rating = 1300
    book_a_id = book_a.id  # store ID before commit

    books.update_books(book_a, book_b)

    refreshed = session.get(Book, book_a_id)
    assert refreshed.rating == 1300
