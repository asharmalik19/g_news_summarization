import os

from google import genai
import chromadb
from dotenv import load_dotenv

from rag.embedding_function import GeminiEmbeddingFunction

# TODO: this design can be definitely improved

def search(query):
    load_dotenv()
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=GEMINI_API_KEY)

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')
    chroma_db_path = os.path.join(data_dir, 'chroma_db')

    embedding_fn = GeminiEmbeddingFunction(client=client)
    embedding_fn.document_mode = False
    chroma_client = chromadb.PersistentClient(path=chroma_db_path)
    db = chroma_client.get_collection(name='my_db', embedding_function=embedding_fn)

    result = db.query(
        query_texts=query,
        n_results=2,
        include=['documents', 'metadatas']
    )
    retrieved_articles = result['documents'][0]
    articles_combined = ','.join(retrieved_articles)
    retrieved_urls = result['metadatas'][0]
    retrieved_urls = [url['url'] for url in retrieved_urls]

    prompt = f"""
    You are an expert assistant. Based on the following user query and the related articles retrieved from a knowledge base, generate a clear and concise summary that directly answers the query.
    Query: {query}

    Retrieved Articles: {articles_combined}
    """
    response = client.models.generate_content(
        model='gemma-3-27b-it',
        contents=prompt
    )
    return {
        'summary': response.text,
        'retrieved_urls': retrieved_urls
    }


        