from chromadb import Documents, EmbeddingFunction, Embeddings
from google.api_core import retry
from google.genai import types
from google import genai
import chromadb
from dotenv import load_dotenv
import os


load_dotenv()

# Define a helper to retry when per-minute quota is reached.
is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})


class GeminiEmbeddingFunction(EmbeddingFunction):
    # Specify whether to generate embeddings for documents, or queries
    document_mode = True

    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=GEMINI_API_KEY)

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
    chroma_client = chromadb.Client()
    embedding_fn = GeminiEmbeddingFunction()
    chroma_client.create_collection(name='my_collection', embedding_function=embedding_fn)
