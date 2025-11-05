from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select, desc

from app.core.db import init_db, get_session, Book
from app.core import books, ranking

app = FastAPI(title="PageOff")
templates = Jinja2Templates(directory="app/templates")

# Seed on startup
seed_books = [
    {"title": "The Hobbit", "author": "J.R.R. Tolkien"},
    {"title": "1984", "author": "George Orwell"},
    {"title": "Pride and Prejudice", "author": "Jane Austen"},
    {"title": "Dune", "author": "Frank Herbert"},
]
init_db(seed_books)

@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="/compare")

@app.get("/compare", response_class=HTMLResponse)
async def compare_page(request: Request):
    a, b = books.select_pair_nearby()
    return templates.TemplateResponse("compare.html", {"request": request, "a": a, "b": b})

@app.post("/vote", response_class=HTMLResponse)
async def vote(request: Request, winner: int = Form(...), loser: int = Form(...)):
    ranking.apply_vote(winner, loser)
    a, b = books.select_pair_nearby()
    return templates.TemplateResponse("pair_fragment.html", {"request": request, "a": a, "b": b})



@app.get("/ranking", response_class=HTMLResponse)
async def ranking_page(request: Request):
    with get_session() as session:
        top_books = session.exec(select(Book).order_by(desc(Book.rating))).all()
    return templates.TemplateResponse("ranking.html", {"request": request, "books": top_books})



@app.post("/skip")
async def skip_book_view(request: Request, skipped_id: int = Form(...), keep_id: int = Form(...)):
    """Handle 'I haven't read it' for one of the books."""
    from app.core.books import skip_book
    replacement = skip_book(skipped_id)

    # Determine which book stays in place
    with get_session() as session:
        keep_book = session.get(Book, keep_id)

    # Always return two fresh objects
    return templates.TemplateResponse(
        "pair_fragment.html",
        {"request": request, "a": keep_book, "b": replacement}
    )
