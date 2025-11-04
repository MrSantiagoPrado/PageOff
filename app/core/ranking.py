from app.core.db import Book, get_session
from sqlmodel import select

K_FACTOR_DEFAULT = 32

def expected_score(ra, rb):
    return 1.0 / (1.0 + 10 ** ((rb - ra) / 400.0))

def update_elo(ra, rb, outcome_a, k=K_FACTOR_DEFAULT):
    ea = expected_score(ra, rb)
    ra_new = ra + k * (outcome_a - ea)
    rb_new = rb + k * ((1 - outcome_a) - (1 - ea))
    return ra_new, rb_new

def apply_vote(winner_id: int, loser_id: int):
    with get_session() as session:
        winner = session.get(Book, winner_id)
        loser = session.get(Book, loser_id)
        
        if winner is None or loser is None:
            raise ValueError("One or both books not found")
        
        ra_new, rb_new = update_elo(winner.rating, loser.rating, 1)
        winner.rating, loser.rating = ra_new, rb_new
        winner.wins += 1
        winner.matches += 1
        loser.losses += 1
        loser.matches += 1
        session.add(winner)
        session.add(loser)
        session.commit()
