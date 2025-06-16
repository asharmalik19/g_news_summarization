from chromadb import Documents, EmbeddingFunction, Embeddings
from google.api_core import retry
from google.genai import types
from google import genai
import chromadb
from dotenv import load_dotenv
import os
import sqlite3
import pandas as pd
import shutil

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=GEMINI_API_KEY)

# Define a helper to retry when per-minute quota is reached.
is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})

class GeminiEmbeddingFunction(EmbeddingFunction):
    # Specify whether to generate embeddings for documents, or queries
    document_mode = True  
    def __init__(self):
        pass

    @retry.Retry(predicate=is_retriable)
    def __call__(self, input: Documents) -> Embeddings:
        if self.document_mode:
            embedding_task = "retrieval_document"
        else:
            embedding_task = "retrieval_query"

        response = client.models.embed_content(
            model="models/text-embedding-004",
            contents=input,
            config=types.EmbedContentConfig(
                task_type=embedding_task,
            ),
        )
        return [e.values for e in response.embeddings]
    
def read_articles():
    with sqlite3.connect('../data/articles_data.db') as conn:
        df = pd.read_sql("SELECT text FROM article", conn)
        articles_texts = df['text'].tolist()[:5]  # temp limit to 10 articles for testing
    return articles_texts
    
if __name__=='__main__':
    shutil.rmtree(path='../data/chroma_db', ignore_errors=True)
    chroma_client = chromadb.PersistentClient(path='../data/chroma_db')
    embedding_fn = GeminiEmbeddingFunction()
    db = chroma_client.create_collection(name='my_db', embedding_function=embedding_fn)

    articles = read_articles()
    db.add(
        documents=articles, 
        ids=[str(i) for i in range(len(articles))]
    )




    
    

