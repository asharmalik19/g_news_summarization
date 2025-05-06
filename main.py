from fastapi import FastAPI
import sqlite3

app = FastAPI(title="Google news Summary API",)

@app.get("/")
def read_item():
    return {
        "summary": "This is a summary of the API.",
        "description": "This API provides endpoints for various functionalities.",
        "version": "1.0.0",
        "author": "Ashar Khan"
    }

@app.get("/summary")
def read_articles():
    with sqlite3.connect('articles_data.db') as con:
        cur = con.cursor()
        all_summaries = cur.execute("SELECT summary FROM article").fetchall()
        return {
            "summaries": [row[0] for row in all_summaries]
        }



