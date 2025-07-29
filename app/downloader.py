import os

import requests
import tarfile

"""This module downloads the required databases from the GitHub releases everytime the app runs."""

def save_db(response, db_name):
    """
    Saves the downloaded database file to the 'data/' directory
    at the project root.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_dir = os.path.join(project_root, 'data')
    os.makedirs(data_dir, exist_ok=True)
    db_file_path = os.path.join(data_dir, db_name)
    with open(db_file_path, 'wb') as f:
        f.write(response.content)

    if db_name.endswith('.tar.gz'):
        with tarfile.open(db_file_path, 'r:gz') as tar:
            tar.extractall(path=data_dir)

def get_db(url, db_name):
    """
    Downloads the database file from the github release URL.
    """
    print(f"Downloading database {db_name}")
    response = requests.get(url)
    save_db(response, db_name)
    print(f"Database downloaded successfully {db_name}.")

def download_db():
    SQLITEDB_NAME = 'articles_data.db'
    CHROMADB_NAME = 'vector_db.tar.gz'
    SQLITEDB_URL = 'https://github.com/asharmalik19/g_news_summarization/releases/download/daily-summary/articles_data.db'
    CHROMADB_URL = 'https://github.com/asharmalik19/g_news_summarization/releases/download/daily-summary/vector_db.tar.gz'
    get_db(SQLITEDB_URL, SQLITEDB_NAME)
    get_db(CHROMADB_URL, CHROMADB_NAME)

if __name__ == "__main__":
    download_db()
    


