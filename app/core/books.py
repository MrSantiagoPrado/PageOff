from app.core.db import Book, get_session
from sqlmodel import select
import random
from typing import Sequence

def get_all_books() -> Sequence[Book]:
    """
    Retrieve all books from the database.
    """
    with get_session() as session:
        return session.exec(select(Book)).all()

def select_pair_nearby() -> list[Book]:
    """Select two books with similar ratings."""
    books = get_all_books()
    return random.sample(books, 2)

def update_books(a: Book, b: Book) -> None:
    """Update book records in the database."""
    with get_session() as session:
        session.add(a)
        session.add(b)
        session.commit()



def skip_book(book_id: int) -> Book:
    """Increment skip count and return a new random replacement book."""
    with get_session() as session:
        book = session.get(Book, book_id)
        if book:
            book.times_skipped = getattr(book, "times_skipped", 0) + 1
            session.add(book)
            session.commit()

        # Select a random replacement
        all_books = session.exec(select(Book)).all()
        replacement = random.choice([b for b in all_books if b.id != book_id])
        return replacement