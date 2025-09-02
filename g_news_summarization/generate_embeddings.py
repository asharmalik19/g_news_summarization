import os
import shutil
import sqlite3

from google import genai
import chromadb
from dotenv import load_dotenv
import pandas as pd

from .embedding_function import GeminiEmbeddingFunction

def read_articles(data_dir):
    articles_db_path = os.path.join(data_dir, 'articles_data.db')
    with sqlite3.connect(articles_db_path) as conn:
        df = pd.read_sql("SELECT text, url FROM article", conn)
    return df
    
if __name__=='__main__':
    load_dotenv()
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=GEMINI_API_KEY)

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')
    chroma_db_path = os.path.join(data_dir, 'chroma_db')

    shutil.rmtree(path=chroma_db_path, ignore_errors=True)
    chroma_client = chromadb.PersistentClient(path=chroma_db_path)
    embedding_fn = GeminiEmbeddingFunction(client=client)
    db = chroma_client.create_collection(name='my_db', embedding_function=embedding_fn)

    articles = read_articles(data_dir) 
    for batch in range(0, len(articles), 100):
        batch_articles = articles.iloc[batch:batch + 100]
        print(f'generating embeddings for batch {batch // 100 + 1}')
        
        db.add(
            documents=batch_articles['text'].tolist(), 
            ids=[str(i) for i in range(len(batch_articles))],
            metadatas=[{'url': url} for url in batch_articles['url'].tolist()]
        )




    
    

