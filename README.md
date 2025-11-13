# 📚 PageOff

**PageOff** is a lightweight, interactive web app that helps readers discover which books they truly love — by making them *vote* between two books at a time.*  
Each vote updates an **ELO-style ranking**, surfacing the best books through real preferences, not star ratings.

---

## 🚀 MVP 1.0 – Core Features

- **FastAPI + Jinja2 + HTMX architecture** — simple, reactive frontend with no heavy JS.
- **ELO-based ranking system** — books gain/lose rating points based on real pairwise preferences.
- **SQLite database (SQLModel)** — persistent, structured storage.
- **Automatic metadata enrichment** at startup:
  - ISBN retrieval (OpenLibrary)
  - Cover URLs
  - Future-ready for work-level mappings
- **“I haven’t read it” skipping** — tracked via `times_skipped` for future smart pairing logic.
- **Seamless voting UX** — HTMX swaps book pairs without refreshing.
- **Ranking page** — books sorted by current ELO score.
- **Debug-ready environment** — VS Code launch config + Conda env (`pageoff_312`).

---

## 🧱 Stack Overview

| Layer | Tech |
|-------|------|
| Backend | FastAPI |
| Database | SQLite + SQLModel |
| Frontend | Jinja2, HTMX, Tailwind |
| Metadata | OpenLibrary API |
| Environment | Python 3.12 (Conda) |
| Debugging | VS Code |

---

## 🧩 Project Structure

The project follows a clean modular layout:

- `app/core/` — database, book logic, ELO ranking logic  
- `app/templates/` — HTML templates (Jinja2 + HTMX)  
- `app/notebooks/` — metadata enrichment tools  
- `app/main.py` — FastAPI entrypoint  
- `data/pageoff.db` — SQLite database  
- `tests/` — pytest suite with coverage  

---

## 🧭 Next Steps – MVP 2.0 (“Personal Edition”)

Goal: make PageOff useful for one real reader (you).

Planned additions:

- Goodreads CSV import  
- Global baseline rankings (Goodreads avg + rating count)  
- Smarter pair selection using skip counts  
- Work-level grouping of editions  
- Minor UI polish  

---

## 🌍 Long-Term Vision

| Version | Focus |
|----------|--------|
| **Beta 1** | Host a small demo for feedback |
| **Beta 2** | Supabase auth — user accounts + shared rankings |
| **Beta 3** | Global & personalized ELO rankings |
| **v1.0** | Full launch: reading lists, recommendations, discovery |

---

## ▶️ Local Development

### **1. Clone the repo**

```
git clone https://github.com/yourusername/PageOff.git
cd PageOff
```

### **2. Set up the Conda environment**

```
conda create -n pageoff_312 python=3.12
conda activate pageoff_312
pip install -r requirements.txt
```

### **3. Run the app (custom port 8010)**

```
uvicorn app.main:app --reload --port 8010
```

Now visit:

```
http://localhost:8010
```

### **4. Run tests**

```
pytest --cov
```

### **5. VS Code debugging**

A `.vscode/launch.json` is included.  
Just press **F5** to launch the debugger.

---



## ✨ License

MIT

---
