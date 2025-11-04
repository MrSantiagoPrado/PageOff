import pytest
from app.core import ranking

def test_expected_score_symmetry():
    ra, rb = 1200, 1200
    ea = ranking.expected_score(ra, rb)
    eb = ranking.expected_score(rb, ra)
    assert abs(ea + eb - 1.0) < 1e-9
    assert ea == pytest.approx(0.5)

def test_update_elo_winner_loser_directions():
    ra, rb = 1200, 1200
    ra_new, rb_new = ranking.update_elo(ra, rb, outcome_a=1)
    assert ra_new > ra
    assert rb_new < rb

def test_update_elo_conservation_of_sum():
    """Sum of ratings shouldn’t drift much; only K scaling."""
    ra, rb = 1300, 1100
    ra_new, rb_new = ranking.update_elo(ra, rb, outcome_a=0.5)
    diff = (ra_new + rb_new) - (ra + rb)
    assert abs(diff) < 1e-6
