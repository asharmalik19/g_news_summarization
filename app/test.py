from chromadb import Documents, EmbeddingFunction, Embeddings
from google.api_core import retry
from google.genai import types
from google import genai
import chromadb
from dotenv import load_dotenv
import os

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
    
if __name__=='__main__':
    embedding_fn = GeminiEmbeddingFunction()
    embedding_fn.document_mode = False
    chroma_client = chromadb.PersistentClient(path='./data/chroma_db')
    db = chroma_client.get_collection(name='my_db', embedding_function=embedding_fn)

    query = 'apple'
    result = db.query(
        query_texts=query,
        n_results=2
    )

    retrieved_articles = result['documents'][0]
    articles_combined = ','.join(retrieved_articles)

    prompt = f"""
    You are an expert assistant. Based on the following user query and the related articles retrieved from a knowledge base, generate a clear and concise summary that directly answers the query.
    Query: {query}

    Retrieved Articles: {articles_combined}
    """

    response = client.models.generate_content(
        model="gemma-3-27b-it",
        contents=prompt
    )
    print(response.text)


        