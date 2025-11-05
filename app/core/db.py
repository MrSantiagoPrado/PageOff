from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "pageoff.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"


engine = create_engine(DATABASE_URL, echo=False)

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    rating: float = 1200.0
    wins: int = 0
    losses: int = 0
    matches: int = 0
    cover_url: Optional[str] = None
    isbn: Optional[str] = None

def init_db(seed_books=None):
    SQLModel.metadata.create_all(engine)
    if seed_books:
        with Session(engine) as session:
            if not session.exec(select(Book)).first():
                session.add_all([Book(**b) for b in seed_books])
                session.commit()

def get_session():
    return Session(engine)
