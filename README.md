## Google News Summarizer
This project aims to summarize google news articles using an LLM

### Features
- Extracts news articles from google news feeds
- Generates concise summaries of the articles using LLM
- Display the summaries along with the source link on HTML page
- Display news summaries by category

### Prerequisites
- **Python 3.12+**

### Installation
1. Clone the repo:
    ```bash
    git clone https://github.com/asharmalik19/g_news_summarization.git
    cd g_news_summarization
2. Create & activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate    # Windows: .venv\Scripts\activate
3. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
4. Download the updated database file
    ```bash
    python3 ./download_db.py

Now you have everything set up on your system. Everytime you need to run the application, you can use the command `uvicorn main:app`
    
After uvicorn is up and running, you can open your browser and Enter this address **http://127.0.0.1:8000** to see the output and interact with the app.

**Note:** You need to download the fresh copy of sqlite db file before running the application to get the fresh news articles.


