import os
import sqlite3
import json

from google import genai
import pandas as pd
from dotenv import load_dotenv
from google.api_core import retry
from pydantic import BaseModel

from .downloader import find_project_root

class ArticleSummary(BaseModel):
    summary: list[str]

is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})

@retry.Retry(predicate=is_retriable)
def generate_summary(article, client):
    prompt = f"""
    You are a professional news‑summarizer.
    Read the article below and generate its summary in 3 concise points covering key ideas.

    Rules:
    - Plain sentences, no leading bullets, dashes, asterisks, or numbering. 

    Article:
    {article}
    """

    response = client.models.generate_content(
        # model='gemma-3-27b-it',
        model='gemini-2.0-flash-lite',
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': ArticleSummary
        }
    )  
    return response.parsed

def store_articles_in_db(data_dir, articles_df):
    with sqlite3.connect(f'{data_dir}/articles_data.db') as con:
        articles_df['summary'] = articles_df['summary'].apply(json.dumps)
        articles_df.to_sql('article', con, if_exists='replace')
    return
    
if __name__ == '__main__':
    load_dotenv()
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=GEMINI_API_KEY)

    project_root = find_project_root()
    data_dir = os.path.join(project_root, 'data')
    file_path = os.path.join(data_dir, 'articles.csv')
    df = pd.read_csv(filepath_or_buffer=file_path)
    summaries = []
    for i, row in df.iterrows():
        article_with_title = f"{row['title']}\n\n{row['text']}"
        article_summary = generate_summary(article_with_title, client)
        print(article_summary.summary)
        summaries.append(article_summary.summary)
    df['summary'] = summaries
        
    store_articles_in_db(data_dir, df)

        
    