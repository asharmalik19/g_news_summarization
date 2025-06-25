import os
import sqlite3
import time

from google import genai
import pandas as pd
from google.genai.errors import ClientError
from dotenv import load_dotenv
from google.api_core import retry


is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})

@retry.Retry(predicate=is_retriable)
def generate_summary(article, client):
    prompt = f"""
    You are a professional news‑summarizer.
    Read the article below and generate its summary in 3 concise points covering key ideas.

    Article:
    {article}

    Output format:
    3 sentences of summary. No other text. Just the summary.
    """

    response = client.models.generate_content(
        model='gemma-3-27b-it',
        contents=prompt
    )  
    return response.text

def store_articles_in_db(articles_df):
    with sqlite3.connect('data/articles_data.db') as con:
        articles_df.to_sql('article', con, if_exists='replace')
    return
    
if __name__ == '__main__':
    load_dotenv()
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=GEMINI_API_KEY)

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')
    file_path = os.path.join(data_dir, 'articles.csv')
    df = pd.read_csv(filepath_or_buffer=file_path)
    for i, row in df.iterrows():
        article_with_title = f"{row['title']}\n\n{row['text']}"
        summary = generate_summary(article_with_title, client)
        df.loc[i, 'summary'] = summary
        print(summary)
        
    store_articles_in_db(df)

        
    