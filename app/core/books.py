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
