import os

import requests
import tarfile

"""This module downloads the required databases from the GitHub releases everytime the app runs."""

def find_project_root():
    """ 
    Finds the project root directory by looking for 'pyproject.toml'.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while True:
        parent_dir = os.path.dirname(current_dir)
        for file in os.listdir(parent_dir):
            if file == 'pyproject.toml':
                return parent_dir
        current_dir = parent_dir
        if current_dir == 'g-news-summarization':
            raise FileNotFoundError("Project root with 'pyproject.toml' not found.")

def save_db(response, db_name):
    """
    Saves the downloaded database file to the 'data/' directory
    at the project root. It is assumed that the script directory
    is stored under the project root.
    """
    project_root = find_project_root()
    data_dir = os.path.join(project_root, 'data')
    os.makedirs(data_dir, exist_ok=True)
    db_file_path = os.path.join(data_dir, db_name)
    with open(db_file_path, 'wb') as f:
        f.write(response.content)

    if db_name.endswith('.tar.gz'):
        with tarfile.open(db_file_path, 'r:gz') as tar:
            tar.extractall(path=data_dir)
    return db_file_path

def get_db(url, db_name):
    """
    Downloads the database file from the github release URL.
    """
    response = requests.get(url)
    db_file_path = save_db(response, db_name)
    print(f"Database stored at path {db_file_path}.")

def download_db():
    SQLITEDB_NAME = 'articles_data.db'
    CHROMADB_NAME = 'vector_db.tar.gz'
    SQLITEDB_URL = 'https://github.com/asharmalik19/g_news_summarization/releases/download/daily-summary/articles_data.db'
    CHROMADB_URL = 'https://github.com/asharmalik19/g_news_summarization/releases/download/daily-summary/vector_db.tar.gz'
    get_db(SQLITEDB_URL, SQLITEDB_NAME)
    get_db(CHROMADB_URL, CHROMADB_NAME)

if __name__ == "__main__":
    download_db()
    


