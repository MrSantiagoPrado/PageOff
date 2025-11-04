from sqlmodel import SQLModel, Session, create_engine, select
from app.core import db

def test_init_db_creates_and_seeds(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path}/test.db")
    db.engine = engine  # temporarily patch the engine

    seed = [
        {"title": "Test Book", "author": "Tester"},
        {"title": "Another Book", "author": "Someone"},
    ]

    db.init_db(seed)
    with Session(engine) as session:
        rows = session.exec(select(db.Book)).all()
        assert len(rows) == 2
        assert rows[0].title == "Test Book"

def test_get_session_returns_session(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path}/test2.db")
    db.engine = engine
    SQLModel.metadata.create_all(engine)

    session = db.get_session()
    try:
        assert isinstance(session, Session)
    finally:
        session.close()
