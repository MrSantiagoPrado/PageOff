from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os


from app.core import books, ranking

app = FastAPI(title="PageOff")

# --- Directories ---
DATA_DIR = "data"
SEED_PATH = os.path.join(DATA_DIR, "books_seed.json")
STATE_PATH = os.path.join(DATA_DIR, "books_state.json")

templates = Jinja2Templates(directory="app/templates")

# --- Load books ---
if os.path.exists(STATE_PATH):
    BOOKS = books.load_state(STATE_PATH)
else:
    BOOKS = books.load_seed(SEED_PATH)
    books.save_state(BOOKS, STATE_PATH)


# --- Routes ---
@app.get("/", response_class=HTMLResponse)
async def root():
    # Redirect root to compare
    return RedirectResponse(url="/compare")


@app.get("/compare", response_class=HTMLResponse)
async def compare_page(request: Request):
    a, b = books.select_pair_nearby(BOOKS)
    return templates.TemplateResponse(
        "compare.html", {"request": request, "a": a, "b": b}
    )


@app.post("/vote", response_class=HTMLResponse)
async def vote(request: Request, winner: str = Form(...), loser: str = Form(...)):
    # Update ratings
    ranking.apply_vote(BOOKS, winner_id=winner, loser_id=loser)
    books.save_state(BOOKS, STATE_PATH)

    # Pick a new pair
    a, b = books.select_pair_nearby(BOOKS)

    # Return *only the fragment* (no base.html)
    return templates.TemplateResponse(
        "pair_fragment.html", {"request": request, "a": a, "b": b}
    )


@app.get("/ranking", response_class=HTMLResponse)
async def ranking_page(request: Request):
    # Sort descending by rating
    top_books = sorted(BOOKS.values(), key=lambda x: x.rating, reverse=True)
    return templates.TemplateResponse(
        "ranking.html", {"request": request, "books": top_books}
    )
