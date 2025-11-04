# app/core/books.py

import json
import os
import random
from dataclasses import dataclass, asdict
from typing import Dict, Tuple

ELO_START = 1200

@dataclass
class Book:
    id: str
    title: str
    author: str
    rating: float = ELO_START
    wins: int = 0
    losses: int = 0
    matches: int = 0

def load_seed(path: str) -> Dict[str, Book]:
    """Load initial book data from JSON seed file."""
    with open(path, "r", encoding="utf-8") as f:
        items = json.load(f)
    books = {
        x["id"]: Book(id=x["id"], title=x["title"], author=x["author"])
        for x in items
    }
    return books

def load_state(path: str) -> Dict[str, Book]:
    """Load current state (ratings, stats) from JSON."""
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return {k: Book(**v) for k, v in raw.items()}

def save_state(books: Dict[str, Book], path: str):
    """Write book state to JSON."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    payload = {k: asdict(v) for k, v in books.items()}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def select_pair(books: Dict[str, Book]) -> Tuple[Book, Book]:
    """Pick two distinct random books."""
    a, b = random.sample(list(books.values()), 2)
    return a, b

def select_pair_nearby(
    books: Dict[str, Book],
    window: int = 200
) -> Tuple[Book, Book]:
    """Pick two books with similar ratings (within window Elo points)."""
    pool = list(books.values())
    a = random.choice(pool)
    candidates = [
        x for x in pool if x.id != a.id and abs(x.rating - a.rating) <= window
    ]
    if not candidates:
        candidates = [x for x in pool if x.id != a.id]
    b = random.choice(candidates)
    return (a, b) if random.random() < 0.5 else (b, a)
