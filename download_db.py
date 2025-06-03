import requests

def get_db():
    """Download the SQLite database from the specified URL."""
    URL = 'https://github.com/asharmalik19/g_news_summarization/releases/download/daily-summary/articles_data.db'
    print("Downloading database...")
    response = requests.get(URL)
    with open('data/articles_data.db', 'wb') as file:
        file.write(response.content)
    print("Database downloaded successfully.")

if __name__ == "__main__":
    get_db()