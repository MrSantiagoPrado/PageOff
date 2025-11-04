# app/core/ranking.py


from typing import Tuple

K_FACTOR_DEFAULT = 32

def expected_score(ra: float, rb: float) -> float:
    """Return the probability that player/book A beats B."""
    return 1.0 / (1.0 + 10 ** ((rb - ra) / 400.0))

def update_elo(
    ra: float,
    rb: float,
    outcome_a: float,
    k: float = K_FACTOR_DEFAULT
) -> Tuple[float, float]:
    """
    Compute new Elo ratings for A and B.
    outcome_a = 1 if A wins, 0 if A loses, 0.5 for draw.
    """
    ea = expected_score(ra, rb)
    eb = 1.0 - ea
    ra_new = ra + k * (outcome_a - ea)
    rb_new = rb + k * ((1.0 - outcome_a) - eb)
    return ra_new, rb_new

def apply_vote(
    books: dict,
    winner_id: str,
    loser_id: str,
    k: float = K_FACTOR_DEFAULT
):
    """
    Update ratings and stats for a single comparison.
    books: mapping of id -> Book dataclass
    """
    a = books[winner_id]
    b = books[loser_id]
    ra_new, rb_new = update_elo(a.rating, b.rating, outcome_a=1, k=k)
    a.rating, b.rating = ra_new, rb_new
    a.wins += 1
    a.matches += 1
    b.losses += 1
    b.matches += 1
