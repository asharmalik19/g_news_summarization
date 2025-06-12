# Google News Summarizer
A Python application that extracts news articles from Google News feeds and generates concise summaries using a Large Language Model (LLM), giving you daily fresh summaries by topics (i.e, Technology, Business etc).

## Features
- 📰 Extracts news articles from Google News RSS feeds
- 🤖 Generates concise summaries using LLM
- 🌐 Web interface to display summaries with source links
- 📂 Browse news summaries by category
- 🔄 Fresh news updates via downloadable database

## Prerequisites
- **Python 3.12+**
- Internet connection for downloading news database

## Setup guide
1. Clone the repo:
    ```bash
    git clone https://github.com/asharmalik19/g_news_summarization.git
    cd g_news_summarization
    ```
2. Create & activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate    # On Windows: venv\Scripts\activate
    ```
3. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Navigate to the folder `app` and download the updated database file by running
    ```bash
    python ./download_db.py
    ```

## Usage
1. **Navigate to the app folder**

2. **Start the application by running**
   ```bash
   uvicorn main:app --port 8000     # or any other free port
   ```

3. **Open your browser and navigate to**
   ```
   http://127.0.0.1:8000
   ```

**Note:** You need to download the fresh copy of sqlite db file before running the application to get the fresh news articles.

## Project Structure
```
├── .github
│   └── workflows
├── .gitignore
├── LICENSE
├── README.md
├── app
│   ├── download_db.py
│   └── main.py
├── data
│   └── articles_data.db
├── data_extraction_pipeline
│   ├── generate_summary.py
│   └── get_data.py
├── requirements.txt
├── static
│   └── index.html
└── venv
```

## Data Extraction 
A github actions workflow is set to run the data extraction pipeline daily which contains `get_data.py` and `generate_summary.py` scripts. The final output of this pipeline is a `sqlite` database file. The workflow adds this database file to the release of this repo replacing previous file. 
This is how the database containing news articles and their generated summaries is updated daily but if you want the most recent articles, then you can run the workflow manually to get the most recent articles.






