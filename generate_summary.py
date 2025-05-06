from google import genai
import os
import sqlite3
import pandas as pd

def generate_summary(article, client):
    prompt = f"""
    You are a professional news summarizer.
    Read the article below and produce a concise, three-bullet summary that captures its key facts, main events, and core takeaways. Nothing else.

    {article}

    Summary:
    • """

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    return response.text

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

        
    