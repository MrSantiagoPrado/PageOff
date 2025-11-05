from app.core.db import Book, get_session
from sqlmodel import select
import random

def get_all_books():
    with get_session() as session:
        return session.exec(select(Book)).all()

def select_pair_nearby():
    books = get_all_books()
    return random.sample(books, 2)

def update_books(a: Book, b: Book):
    with get_session() as session:
        session.add(a)
        session.add(b)
        session.commit()



def skip_book(book_id: int) -> Book:
    """Increment skip count and return a replacement book."""
    with get_session() as session:
        book = session.get(Book, book_id)
        if not book:
            raise ValueError("Book not found")
        book.times_skipped += 1
        session.add(book)
        session.commit()

        # Get a replacement (avoiding the skipped one)
        all_books = session.exec(select(Book).where(Book.id != book_id)).all()
        return random.choice(all_books)