from google import genai
import os
import sqlite3
import pandas as pd
import json

def generate_summary(article, client):
    prompt = f"""
    You are a professional news‑summarizer.
    Read the article below and output ONLY valid JSON with one key, "summary", whose value is a single string.
    That string should contain three short key points, separated by newline characters.

    Article:
    {article}

    Example output:
    {{
    "summary": "Point 1..\\n\\npoint 2..\\n\\npoint 3.."
    }}
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    raw = response.text.strip()
    return raw

def store_articles_in_db(articles_df):
    with sqlite3.connect('articles_data.db') as con:
        articles_df.to_sql('article', con, if_exists='replace')
    return
    
if __name__ == '__main__':
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=GEMINI_API_KEY)

    df = pd.read_csv('articles.csv')
    for i, row in df.iterrows():
        article_with_title = f"{row['title']}\n\n{row['text']}"
        summary = generate_summary(article_with_title, client)
        df.loc[i, 'summary'] = summary
        print(summary)
 
    store_articles_in_db(df)

        
    