import os

import requests

def save_db_file(response):
    """Save the downloaded SQLite database file to the data directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_dir = os.path.join(project_root, 'data')
    os.makedirs(data_dir, exist_ok=True)
    db_file_path = os.path.join(data_dir, 'articles_data.db')
    with open(db_file_path, 'wb') as f:
        f.write(response.content)

def get_db():
    """Download the SQLite database from the specified URL."""
    URL = 'https://github.com/asharmalik19/g_news_summarization/releases/download/daily-summary/articles_data.db'
    print("Downloading database...")
    response = requests.get(URL)
    save_db_file(response)
    print("Database downloaded successfully.")

if __name__ == "__main__":
    get_db()

