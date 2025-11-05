import requests
from sqlmodel import select
from app.core.db import get_session, Book


def fetch_isbn(title: str, author: str) -> str | None:
    url = "https://openlibrary.org/search.json"
    params = {"title": title, "author": author}
    r = requests.get(url, params=params, timeout=10)
    if r.status_code != 200:
        return None
    docs = r.json().get("docs", [])
    if not docs:
        return None
    isbn_list = docs[0].get("isbn", [])
    return isbn_list[0] if isbn_list else None


def cover_from_isbn(isbn: str) -> str | None:
    if not isbn:
        return None
    return f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"


def cover_from_title_author(title: str, author: str) -> str | None:
    url = "https://openlibrary.org/search.json"
    params = {"title": title, "author": author}
    r = requests.get(url, params=params, timeout=10)
    if r.status_code != 200:
        return None
    docs = r.json().get("docs", [])
    if not docs:
        return None
    cover_id = docs[0].get("cover_i")
    if cover_id:
        return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
    return None


def populate_metadata():
    """Fill missing ISBNs and covers for books."""
    with get_session() as session:
        books = session.exec(select(Book)).all()
        updated = 0
        for b in books:
            changed = False

            if not b.isbn:
                b.isbn = fetch_isbn(b.title, b.author)
                changed = True

            if not b.cover_url:
                b.cover_url = (
                    cover_from_isbn(b.isbn) if b.isbn else None
                    or cover_from_title_author(b.title, b.author)
                )
                changed = True

            if changed:
                updated += 1
                session.add(b)

        if updated:
            session.commit()
            print(f"📚 Enriched {updated} books with metadata.")
        else:
            print("✅ No enrichment needed — all books have ISBNs and covers.")
