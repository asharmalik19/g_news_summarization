import os

import requests
import tarfile
import time

def save_db(response, db_name):
    """Save the downloaded SQLite database file to the data directory."""
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
            time.sleep(0.5)    # sleep for windows OS
            os.remove(db_file_path)

def get_db(url, db_name):
    """Download the SQLite database from the specified URL."""
    print(f"Downloading database {db_name}")
    response = requests.get(url)
    save_db(response, db_name)
    print(f"Database downloaded successfully {db_name}.")


if __name__ == "__main__":
    SQLITEDB_NAME = 'articles_data.db'
    CHROMADB_NAME = 'vector_db.tar.gz'
    SQLITEDB_URL = 'https://github.com/asharmalik19/g_news_summarization/releases/download/daily-summary/articles_data.db'
    CHROMADB_URL = 'https://github.com/asharmalik19/g_news_summarization/releases/download/daily-summary/vector_db.tar.gz'
    get_db(SQLITEDB_URL, SQLITEDB_NAME)
    get_db(CHROMADB_URL, CHROMADB_NAME)


