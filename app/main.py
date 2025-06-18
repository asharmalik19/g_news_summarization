import sqlite3

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from rag.rag_search import search

app = FastAPI(title="Google News Summary API")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')
    
@app.get("/summaries")
def read_summaries():
    with sqlite3.connect('data/articles_data.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        rows = cur.execute("SELECT title, summary, url FROM article").fetchall()
        articles = [dict(row) for row in rows]
        return {'articles': articles}
    
@app.get("/summaries/{category}")
def read_summaries_by_category(category):
    with sqlite3.connect('data/articles_data.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        rows = cur.execute("SELECT title, summary, url FROM article WHERE Category = ?", (category, )).fetchall()
        articles = [dict(row) for row in rows]
        return {'articles': articles}
    
@app.get("/search")
def rag_search(query):
    result = search(query)
    return result












