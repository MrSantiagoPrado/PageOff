import pytest
from sqlmodel import SQLModel, Session, create_engine, select
from app.core.db import Book
from app.core import ranking

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all([
            Book(title="Book A", author="Author A", rating=1200),
            Book(title="Book B", author="Author B", rating=1200),
        ])
        session.commit()
        yield session

def test_expected_score_symmetry():
    ea = ranking.expected_score(1200, 1200)
    assert abs(ea - 0.5) < 1e-9

def test_update_elo_correctness():
    ra_new, rb_new = ranking.update_elo(1200, 1200, outcome_a=1)
    assert ra_new > 1200
    assert rb_new < 1200

def test_apply_vote_updates_rating(session, monkeypatch):
    monkeypatch.setattr(ranking, "get_session", lambda: session)
    all_books = session.exec(select(Book)).all()
    a, b = all_books[:2]
    a_id, b_id = a.id, b.id
    old_a_rating, old_b_rating = a.rating, b.rating

    ranking.apply_vote(a_id, b_id)

    updated_a = session.get(Book, a_id)
    updated_b = session.get(Book, b_id)

    assert updated_a.rating > old_a_rating
    assert updated_b.rating < old_b_rating
    assert updated_a.wins == 1
    assert updated_b.losses == 1
