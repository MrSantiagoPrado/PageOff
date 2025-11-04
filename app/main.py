from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core import books, ranking
import os

app = FastAPI(title="PageOff")

# Directories
DATA_DIR = "data"
SEED_PATH = os.path.join(DATA_DIR, "books_seed.json")
STATE_PATH = os.path.join(DATA_DIR, "books_state.json")

templates = Jinja2Templates(directory="app/templates")

# Load initial state
if os.path.exists(STATE_PATH):
    BOOKS = books.load_state(STATE_PATH)
else:
    BOOKS = books.load_seed(SEED_PATH)
    books.save_state(BOOKS, STATE_PATH)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse(url="/compare")

@app.get("/compare", response_class=HTMLResponse)
async def compare_page(request: Request):
    a, b = books.select_pair_nearby(BOOKS)
    return templates.TemplateResponse(
        "compare.html", {"request": request, "a": a, "b": b}
    )

@app.post("/vote", response_class=HTMLResponse)
async def vote(request: Request, winner: str = Form(...), loser: str = Form(...)):
    ranking.apply_vote(BOOKS, winner_id=winner, loser_id=loser)
    books.save_state(BOOKS, STATE_PATH)
    a, b = books.select_pair_nearby(BOOKS)
    # Return fragment only (HTMX swap)
    return templates.TemplateResponse(
        "pair_fragment.html", {"request": request, "a": a, "b": b}
    )

@app.get("/ranking", response_class=HTMLResponse)
async def ranking_page(request: Request):
    top = sorted(BOOKS.values(), key=lambda x: x.rating, reverse=True)
    return templates.TemplateResponse(
        "ranking.html", {"request": request, "books": top}
    )
