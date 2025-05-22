from google import genai
import os
import sqlite3
import pandas as pd
import time
from google.genai.errors import ClientError

def generate_summary(article, client):
    prompt = f"""
    You are a professional news‑summarizer.
    Read the article below and generate its summary in 3 concise points covering key ideas.

    Article:
    {article}

    Output format:
    3 sentences of summary. No other text. Just the summary.
    """
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                # model="gemma-3-27b-it",
                model="gemini-2.0-flash-lite",
                contents=prompt
            )
            break
        except ClientError as e:
            if attempt == 2:
                raise e
            delay_time = e.details['error']['details'][2]['retryDelay']
            delay_time_int = int(delay_time[:-1])
            print(f"Rate limit exceeded. Retrying in {delay_time_int} seconds...")
            time.sleep(delay_time_int + 30)   
    return response.text

def store_articles_in_db(articles_df):
    with sqlite3.connect('data/articles_data.db') as con:
        articles_df.to_sql('article', con, if_exists='replace')
    return
    
if __name__ == '__main__':
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=GEMINI_API_KEY)

    df = pd.read_csv('data/articles.csv')
    for i, row in df.iterrows():
        article_with_title = f"{row['title']}\n\n{row['text']}"
        summary = generate_summary(article_with_title, client)
        df.loc[i, 'summary'] = summary
        print(summary)
        
    store_articles_in_db(df)

        
    